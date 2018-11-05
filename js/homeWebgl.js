(function () {
    let scene, camera, woosh, ting, impact, spaceMusic, renderer, t;
    woosh = new Audio('assets/wooshIntro.mp3')
    spaceMusic = new Audio('assets/spaceMusic.mp3')
    impact = new Audio('assets/impact.mp3')
    ting = new Audio('assets/passedRing.mp3')
    t = 0;
    scene = new THREE.Scene();

    camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 0.1, 1000);
    camera.position.set(0, 2, -10);
    camera.lookAt(0, 2, 10);

    renderer = new THREE.WebGLRenderer();
    renderer.setSize(window.innerWidth, window.innerHeight);

    let light = new THREE.AmbientLight({ color: 0xffffff });
    light.intensity = 0.2;
    scene.add(light);

    let pointLight = new THREE.PointLight({ color: 0xffffff });
    pointLight.position.set(10, 10, 0);
    scene.add(pointLight);



    let core = new THREE.Mesh(new THREE.IcosahedronGeometry(2, 2), new THREE.MeshLambertMaterial({
        color: 0xff4455,
    }))
    scene.add(core)

    let ring = new THREE.Mesh(new THREE.TorusGeometry(3, 0.2, 10, 40), new THREE.MeshLambertMaterial({
        color: 0x232323
    }))
    scene.add(ring)

    let moon = new THREE.Mesh(new THREE.IcosahedronGeometry(0.3, 2), new THREE.MeshBasicMaterial());
    scene.add(moon);

    function moonMove() {
        moon.position.x = Math.cos(t / 200) * 4
        moon.position.y = Math.sin(t / 200) * 4
    }


    let stars = []
    for (let i = 0; i < 100; i++) {
        stars[i] = new THREE.Mesh(new THREE.SphereGeometry(0.01), new THREE.MeshBasicMaterial());
        stars[i].position.set((Math.random() - 0.5) * 10, (Math.random() - 0.5) * 10, (Math.random() - 0.5) * 10);
        scene.add(stars[i]);
    }



    function planetRotation() {
        ring.rotation.z += 0.01
        ring.rotation.x = Math.PI / 3
        ring.rotation.y = Math.PI / 5

        core.rotation.x += 0.01;
        core.rotation.y += 0.01;
    }

    function camRotation() {
        camera.position.x = Math.cos(t / 300) * 10;
        camera.position.z = Math.sin(t / 300) * 10;
        camera.lookAt(scene.position);
    }

    TweenLite.ticker.addEventListener("tick", animate);

    function cameraArrive() {

        TweenLite.fromTo(camera.position, 5, { z: -100 },
            {
                z: -6,
                ease: Power3.easeInOut
            });
    }



    function animate() {
        renderer.render(scene, camera);
        planetRotation();
        scene.rotation.y += 0.001;
        moonMove();
        t++;
    }

    animate();
    document.querySelector('#container').appendChild(renderer.domElement);

    window.addEventListener('resize', onWindowResize, false);

    function onWindowResize() {

        camera.aspect = window.innerWidth / window.innerHeight;
        camera.updateProjectionMatrix();

        renderer.setSize(window.innerWidth, window.innerHeight);

    }

    function letsGo() {
        impact.play();
        spaceMusic.pause();
        TweenLite.to(camera.position, 5,
            {
                z: -100,
                ease: Power3.easeInOut
            });
        document.querySelector('.graphisme').classList.add('on')
        document.querySelector('.intro').classList.add('off');
    }


    //INTERACTIONS DOM*************************************************************
    //INTERACTIONS DOM*************************************************************
    //INTERACTIONS DOM*************************************************************

    let ok = document.querySelector('.welcomeScreen button.content');
    let rideau = document.querySelector('#rideau');

    ok.addEventListener('click', function () {
        ting.play();
        document.querySelector('.welcomeScreen').classList.add('off');
        cameraArrive();
        document.querySelector('.intro').classList.add('on');
        setTimeout(function () {
            woosh.play();
            spaceMusic.play();
        }, 2000);
    })

    document.querySelector('.intro button#letsGo').addEventListener('click', letsGo)

    document.querySelector('.graphisme ul li.low').addEventListener('click', function () {
        rideau.classList.add('on');
        ting.play();
        setTimeout(function () { window.location.href = 'low.html' }, 2000)
    })

    document.querySelector('.graphisme ul li.medium').addEventListener('click', function () {
        rideau.classList.add('on');
        ting.play();
        setTimeout(function () { window.location.href = 'medium.html' }, 2000)
    })

    document.querySelector('.graphisme ul li.high').addEventListener('click', function () {
        rideau.classList.add('on');
        ting.play();
        setTimeout(function () { window.location.href = 'high.html' }, 2000)
    })
}());
