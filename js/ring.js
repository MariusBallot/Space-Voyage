class Ring {


    constructor(initDist_) {
        let mesh = new THREE.TorusGeometry(1, 0.1, 5, 40);
        let material = new THREE.MeshLambertMaterial({
            color: 0x9999FF,
        });
        this.theRing = new THREE.Mesh(mesh, material);
        this.theRing.position.set(Math.random() * 3, Math.random() * 3, initDist_);
    }

    move(zCamPos_, posBack_, speed_) {
        this.theRing.position.z -= speed_;
        if (this.theRing.position.z < zCamPos_ - 2) {
            this.theRing.position.set(Math.random() * 3, Math.random() * 3, posBack_);

        }
    }

}