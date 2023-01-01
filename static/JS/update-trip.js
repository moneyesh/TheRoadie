const headers = {
    'Content-Type': 'application/json'
}

function updateToDo(to_do_id) {
    console.log(to_do_id)
    const task = document.getElementsByName(to_do_id)[0].value;
    let body = {task_id:to_do_id, task:task};
    fetch(`/update/to-do`, {
        method:'POST',
        body:JSON.stringify(body),
        headers:headers
    })
    .then(response => response.text())
    .then(data => console.log(data))
    
}

function removeToDo(to_do_id) {
    console.log(to_do_id)
    let body = {task_id:to_do_id};
    fetch(`/remove/to-do`, {
        method:'POST',
        body:JSON.stringify(body),
        headers:headers
    })
    .then(response => response.text())
    .then(data => console.log(data))
    document.getElementById("container-"+to_do_id).remove();
}

document.querySelector("#add-to-do-button").addEventListener('click', (event) => {
    
    const updatedToDoList = document.querySelector("#updated-to-do");
    // const toDoContainer = document.createElement('div')
    // toDoContainer.setAttribute('class', 'to-do-container')
    const newToDoItem = document.createElement("input");
    newToDoItem.setAttribute('required','')
    newToDoItem.setAttribute('class', 'new-updated-to-do-item');
    updatedToDoList.appendChild(newToDoItem);
    console.log(newToDoItem)

});

function addToDo(list_id) {
    console.log(list_id)
}
