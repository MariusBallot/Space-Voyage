//VARIABLE SETUP ****************************************************************
let scene, camera, started, fScore, renderer, movingSpeed, impact, passedRing, speedUp, gotIt, xpos, ypos, score, scoreHolder, play, ringSpeed, passingThresh, earth, losingVerif, displaySpeed, backMusic, force, timePlaceholder, timeIG;
scoreHolder = document.querySelector('h2.score')
ringSpeed = 0.1;
displaySpeed = (ringSpeed * 1000).toFixed(2);
xpos = 0;
ypos = 0;
score = 0;
fScore = 0;
movingSpeed = 0.3;
passingThresh = 0.1;
losingVerif = false;
gotIt = document.querySelector('.instructions .gotIt');
speedUp = new Audio('assets/speedUp.mp3')
impact = new Audio('assets/impact.mp3')
passedRing = new Audio('assets/passedRing.mp3')
passedRing.volume = 0.1;
backMusic = new Audio('assets/droidBishopNightland.mp3');
timeIG = 0;
started = false;
play = false;

gotIt.addEventListener('click', startGame);

function interfaceToggle() {
    document.querySelector('.interface .bottom').classList.toggle('lose');
    scoreHolder.classList.toggle('lose');
}



timePlaceholder = document.querySelector('.interface .bottom .timeIG');

force = document.querySelector('.interface .bottom .force');
force.innerHTML = `Force : ${displaySpeed}N`


window.setInterval(function () {
    if (timeIG > 5 && timeIG < 9) score = 0;
    if (!losingVerif && play) timeIG += 0.01;
    timePlaceholder.innerHTML = `Time: ${timeIG.toFixed(2)}s`
}, 10)



scene = new THREE.Scene();

camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 0.1, 1000);
camera.position.set(0, 0, -10);
camera.lookAt(scene.position);
camera.rotation.x = Math.PI / 2;

renderer = new THREE.WebGLRenderer({ alpha: true });
renderer.setSize(window.innerWidth, window.innerHeight);

let light = new THREE.AmbientLight({ color: 0xffffff });
light.intensity = 0.2;
scene.add(light);

let pointLight = new THREE.PointLight({ color: 0xffffff });
pointLight.position.set(10, 10, 0);
scene.add(pointLight);

function earthCreate() {
    earth = new THREE.Group();
    let center = new THREE.Mesh(new THREE.IcosahedronGeometry(10, 1), new THREE.MeshLambertMaterial({
        color: 0xff4455
    }));
    earth.add(center);

    let earthRing = new THREE.Mesh(new THREE.TorusGeometry(15, 2, 3, 20), new THREE.MeshLambertMaterial({
        color: 0x232323,
    }));
    earthRing.rotation.set(Math.PI / 2, 0, Math.PI / 3);
    earth.add(earthRing);

    earth.position.z = 200;
    scene.add(earth);
}
earthCreate();

function earthRotation() {
    earth.rotation.x += 0.005;
    earth.rotation.z += 0.005;

}





function cameraMovingStart() {
    TweenLite.to(camera.rotation, 3, {
        x: Math.PI,
        ease: Power1.easeInOut
    });
}

function startGame() {
    play = true;
    document.querySelector('#mobileTouch').classList.add('on')
    document.querySelector('.instructions').classList.add('off')
    backMusic.play();
    interfaceToggle();
    cameraMovingStart();
}


let rings = []
for (let i = 0; i < 10; i++) {
    rings[i] = new Ring(50 + i * 10);
    scene.add(rings[i].theRing);
}
TweenLite.ticker.addEventListener("tick", animate);

function scoreBoard() {
    document.querySelector('.loseScreen').classList.add('lose');
    document.querySelector('.loseScreen .gate').innerHTML = `Gates: ${score}`;
    document.querySelector('.loseScreen .time').innerHTML = `Time: ${timeIG.toFixed(2)}s`;
    document.querySelector('.loseScreen .force').innerHTML = `Force: ${displaySpeed}N`;

}




function losing() {
    fScore = score;
    losingVerif = true;
    cameraFall();
    document.querySelector('.flasherRed').classList.add('on');
    setTimeout(function () {
        document.querySelector('.flasherRed').classList.remove('on');
    }, 1000)
    interfaceToggle();
    scoreBoard();
    backMusic.pause();
    impact.play();
}

function cameraFall() {
    TweenLite.fromTo(camera.position, 0.3,
        { x: -3 },
        { x: 3, ease: RoughEase.ease })

    TweenLite.to(camera.position, 10, {
        ease: Power1.easeIn,
        y: -500
    });
    TweenLite.to(camera.rotation, 10, {
        ease: Power1.easeIn,
        z: -100
    });
}

function flasher() {

    document.querySelector('.flasher').classList.add('on');
    setTimeout(function () {
        document.querySelector('.flasher').classList.remove('on');
    }, 1000)
}

function speedUpSoundEffect() {
    speedUp.play();
}

function passingVerif() {
    for (let i = 0; i < rings.length; i++) {

        if (rings[i].theRing.position.z < camera.position.z && rings[i].theRing.position.z > camera.position.z - passingThresh) {
            if (camera.position.x > rings[i].theRing.position.x - 0.9 && camera.position.x < rings[i].theRing.position.x + 0.9) {
                if (camera.position.y > rings[i].theRing.position.y - 0.9 && camera.position.y < rings[i].theRing.position.y + 0.9) {
                    if (!started) { score = 0; }
                    score++;
                    scoreHolder.innerHTML = score;
                    passedRing.play();
                    started = true
                    if (score % 10 === 0) {
                        ringSpeed *= 1.05;
                        displaySpeed = (ringSpeed * 1000).toFixed(2);
                        passingThresh *= 1.05;
                        force.innerHTML = `Gravitational force : ${displaySpeed}N`
                        flasher();
                        speedUpSoundEffect();
                    }
                } else { losing() }
            } else { losing() }
        }
    }
}

function ringMoving() {
    for (let i = 0; i < rings.length; i++) {
        rings[i].move(camera.position.z, 100, ringSpeed);
    }
}


//RENDERER WEBGL **************************************************************
//RENDERER WEBGL **************************************************************
//RENDERER WEBGL **************************************************************

function animate() {
    renderer.render(scene, camera);
    if (losingVerif === false) {
        if (play) {
            ringMoving();
            passingVerif();
        }
    }
    earthRotation();
}

animate();
document.querySelector('#container').appendChild(renderer.domElement);

window.addEventListener('resize', onWindowResize, false);

function onWindowResize() {

    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();

    renderer.setSize(window.innerWidth, window.innerHeight);

}



//CONTROLS ***********************************************************************
//CONTROLS ***********************************************************************
//CONTROLS ***********************************************************************

let touches = document.querySelectorAll('#mobileTouch div');

for (let i = 0; i < touches.length; i++) {
    touches[i].addEventListener('click', camControle);
}

function camControle() {
    if (this.classList == 'touchTop') {
        // up arrow
        ypos += movingSpeed;
        TweenLite.to(camera.position, 0.1, {
            y: ypos,
            ease: Power0.easeNone
        });

    }
    else if (this.classList == 'touchBottom') {
        // down arrow
        console.log('okpe')
        ypos -= movingSpeed;
        TweenLite.to(camera.position, 0.1, {
            y: ypos,
            ease: Power0.easeNone
        });

    }
    else if (this.classList == 'touchLeft') {
        // left arrow
        xpos += movingSpeed;
        TweenLite.to(camera.position, 0.1, {
            x: xpos,
            ease: Power0.easeNone
        });

    }
    else if (this.classList == 'touchRight') {
        // right arrow
        xpos -= movingSpeed;
        TweenLite.to(camera.position, 0.1, {
            x: xpos,
            ease: Power0.easeNone
        });

    }
}





