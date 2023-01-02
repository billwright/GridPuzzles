console.log('running javascript');


// Can use promise chaining or use async (research more on this)
// Some references:
//      https://javascript.info/promise-error-handling
//      https://www.javascripttutorial.net/javascript-fetch-api/
//      https://afteracademy.com/blog/migrating-from-promise-chains-to-async-await/
//      https://afteracademy.com/blog/migrating-from-promise-chains-to-async-await/
//      https://maximorlov.com/async-await-better-than-chaining-promises/
//      https://mockend.com/

function onSubmitGivenPuzzle()  {
    console.log('In onSubmitGivenPuzzle')
    fetch('https://jsonplaceholder.typicode.com/todos/1')
      .then(response => response.json())
      .catch(error => console.log('Error was', error))
      .then(json => console.log(json))
}

function onClickExample()  {
        // API for get requests
        console.log('Running onClickExample...')
        let fetchRes = fetch("https://jsonplaceholder.typicode.com/todos/1");
        // fetchRes is the promise to resolve it by using.then() method
        fetchRes.then(res =>
            res.json()).then(d => {
                console.log('Data returned: ', d)
            })
}
function onClickPuzzleServer()  {
        // API for get requests
        console.log('Running onClickPuzzleServer...')
        const puzzle_def = collectGivenData()
        console.log('Puzzle def is', puzzle_def)

        const puzzle_type = document.getElementById('puzzle_type').value.toLowerCase()

        url = `http://127.0.0.1:5000/solve/${puzzle_type}?definition=${puzzle_def}`
        console.log('Hitting this URL:', url)

        let fetchRes = fetch(url);
        // fetchRes is the promise to resolve it by using.then() method
        fetchRes
            .then(response => {
                if (response.ok) {
                    response.json().then(
                        puzzle_solution => {
                            console.log('Puzzled returned: ', puzzle_solution)
                            populateTableWithSolution(puzzle_solution.solution)
                        }
                    )
                } else {
                    alert(`HTTP return code: ${response.status}`)
                    throw new Error('rethrowing error...')
                }
            })
            .catch(error => console.error(error))   // 400 Error did got go here... Why not?
            // See: https://javascript.plainenglish.io/js-fetch-are-you-handling-responses-correctly-1df3246b85af
}

function collectGivenData() {
    const cells = document.querySelectorAll('.cell');

    let puzzle_def = ''
    cells.forEach(cell => {
        puzzle_def += cell.value + ','
    })
    return puzzle_def;
}

function populateTableWithSolution(solution_dictionary) {
    Object.entries(solution_dictionary).forEach(addressValueArray => {
        cell = document.querySelector(`#${addressValueArray[0]}`)
        cell.value = addressValueArray[1]
    })
}

function onPuzzleTypeChange(event) {
    console.debug('In onPuzzleTypeChange. event is', event)
}

function onDimensionChange(event) {
    console.debug('In onPuzzleTypeChange. event is', event)
}

const selectDimensionElement = document.getElementById('dimension');

selectDimensionElement.addEventListener('change', (event) => {
    console.debug('In onPuzzleTypeChange event listener. new value is', event.srcElement.value)
    const newDimension = event.srcElement.value
    const puzzle_size = Number(newDimension[0])

    const puzzle_table = document.getElementById('puzzleTable')
    puzzle_table.innerHTML = ''
    for (let row = 1; row <= puzzle_size; row++) {
        const newRowElement = document.createElement('tr')
        for (let col = 0; col < puzzle_size; col++) {
            colLetter = String.fromCharCode(65 + col)   // 65 is character 'A'
            const newCellElement = document.createElement('td')
            const newInputBox = document.createElement('input')
            newInputBox.setAttribute('type', 'number')
            newInputBox.setAttribute('min', '1')
            newInputBox.setAttribute('max', puzzle_size*puzzle_size)
            newInputBox.setAttribute('class', 'cell')
            newInputBox.setAttribute('id', colLetter+row)
            newCellElement.appendChild(newInputBox)
            newRowElement.appendChild(newCellElement)
        }
        puzzle_table.appendChild(newRowElement)
    }
});
