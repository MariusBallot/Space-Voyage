let playerForm = document.querySelector('#addPlayer')

//SAVING DATA

playerForm.addEventListener('submit', (e) => {
    e.preventDefault();
    db.collection('players').add({
        name: playerForm.name.value,
        gates: score,
        time: timeIG.toFixed(2),
        force: displaySpeed
    });
    playerForm.classList.add('finished');
    document.querySelector('.loseScreen .leaderBoard').classList.add('on');
})

console.log(document.querySelector('.leaderBoard'))

document.querySelector('.leaderBoard').addEventListener('click', function () {
    document.querySelector('#rideau2').classList.add('on');
    setTimeout(function () {
        window.location.href = 'leaderBoard.html'
    }, 1000)
})
