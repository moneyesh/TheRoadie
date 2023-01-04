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


function addToDo(list_id) {
    console.log(list_id)
    const newUpdatedToDoItem = document.getElementById('new-updated-to-do-item');
    let body = {list_id:list_id, new_updated_to_do_item:newUpdatedToDoItem.value};
    newUpdatedToDoItem.value = " "
    fetch(`/add/new-to-do`, {
        method:'POST',
        body:JSON.stringify(body),
        headers:headers
    })
    .then(response => response.json())
    .then(data => {
        console.log(data)
        const updatedToDoList = document.querySelector("#updated-to-do");
        const containerDiv = document.createElement("div");
        containerDiv.setAttribute('id', `container-${data.task_id}`);
        containerDiv.setAttribute('class', 'to-do-container');
        updatedToDoList.appendChild(containerDiv);

        const newToDoItem = document.createElement("input");
        newToDoItem.setAttribute('required','')
        newToDoItem.setAttribute('class', 'update_to_do');
        newToDoItem.setAttribute('name', data.task_id);
        newToDoItem.value = data.to_do
        containerDiv.appendChild(newToDoItem)
        console.log(newToDoItem)

        const newUpdateButton = document.createElement('button');
        newUpdateButton.setAttribute('name', data.task_id);
        newUpdateButton.setAttribute('onclick', 'updateToDo(name)');
        newUpdateButton.innerHTML = "Update";
        containerDiv.appendChild(newUpdateButton);


        const newRemoveButton = document.createElement('button');
        newRemoveButton.setAttribute('name', data.task_id);
        newRemoveButton.setAttribute('onclick', 'removeToDo(name)');
        newRemoveButton.innerHTML = "Remove"
        containerDiv.appendChild(newRemoveButton);
     })

}