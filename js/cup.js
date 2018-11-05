(function () {
    let scene, camera, renderer, cup, exist, mouseX, mouseY;
    exist = false
    scene = new THREE.Scene();

    mouseX = 0;
    mouseY = 0;

    camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 0.1, 1000);
    camera.position.set(0, 0, 10);
    camera.lookAt(scene.position);

    renderer = new THREE.WebGLRenderer({ alpha: true });
    renderer.setSize(window.innerWidth, window.innerHeight);

    let light = new THREE.AmbientLight({ color: 0xffffff });
    light.intensity = 0.2;
    scene.add(light);

    let pointLight = new THREE.PointLight({ color: 0xffffff });
    pointLight.position.set(10, 10, 0);
    scene.add(pointLight);





    new THREE.MTLLoader()
        .setPath('assets/')
        .load('cup.mtl', function (materials) {

            materials.preload();

            new THREE.OBJLoader()
                .setMaterials(materials)
                .setPath('assets/')
                .load('cup.obj', function (object) {

                    object.position.y = -2.8
                    let s = 0.05
                    object.scale.set(s, s, s);
                    cup = object
                    scene.add(cup);
                    exist = true
                });

        });


    function animate() {
        renderer.render(scene, camera);
        requestAnimationFrame(animate);
        cameraMovesMouse();
        if (exist) cup.rotation.y += 0.01;
    }

    animate();
    document.querySelector('#container').appendChild(renderer.domElement);

    window.addEventListener('resize', onWindowResize, false);

    function onWindowResize() {

        camera.aspect = window.innerWidth / window.innerHeight;
        camera.updateProjectionMatrix();

        renderer.setSize(window.innerWidth, window.innerHeight);

    }

    function onDocumentMouseMove(event) {
        mouseX = (event.clientX - window.innerWidth / 2) / 150;
        mouseY = (event.clientY - window.innerHeight / 2) / 150;

    }

    document.addEventListener('mousemove', onDocumentMouseMove, false);


    function cameraMovesMouse() {
        camera.position.x += (mouseX - camera.position.x) * .05;
        camera.position.y += (- mouseY - camera.position.y) * .05;

        camera.lookAt(scene.position);
    }


}());
