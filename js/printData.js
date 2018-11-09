let board = document.querySelector('.board .list');

db.collection('players').orderBy('gates', 'desc').limit(50).get().then((snapshot) => {
    document.querySelector('#rideau').classList.add('on');
    for (let i = 0; i < snapshot.docs.length; i++) {
        console.log(snapshot.docs[i].data())
        let ul = document.createElement('ul');

        let name = document.createElement('li');
        if (snapshot.docs[i].data().name == "") {
            name.innerHTML = i + 1 + ' - ' + '__';
        } else {
            name.innerHTML = i + 1 + ' - ' + snapshot.docs[i].data().name;
        }

        let gates = document.createElement('li');
        gates.innerHTML = snapshot.docs[i].data().gates;
        let time = document.createElement('li');
        time.innerHTML = snapshot.docs[i].data().time;

        ul.appendChild(name);
        ul.appendChild(gates);
        ul.appendChild(time);
        board.appendChild(ul);
    }
})
