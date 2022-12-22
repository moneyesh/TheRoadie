// this click event creates new lines for more to-dos once the button is clicked "+"
document.querySelector("#to-do-list-button").addEventListener('click', (event) => {
    
    const toDoList = document.querySelector("#to-do-list");
    const toDoContainer = document.createElement('div')
    toDoContainer.setAttribute('class', 'to-do-container')
    const newToDoItem = document.createElement("input");
    newToDoItem.setAttribute('class', 'to-do-list-item');
    toDoList.appendChild(toDoContainer);
    toDoContainer.appendChild(newToDoItem)
    console.log(newToDoItem)

    //need something to prevent lines being blank when saving the trip

    // this is to remove an input box if it's not needed
    const removeButton = document.createElement("button");
    toDoContainer.appendChild(removeButton)
    removeButton.innerHTML = "- remove";
    removeButton.setAttribute('class', 'remove-to-do');

    removeButton.addEventListener('click', (event) => {
        console.log('button clicked')
        toDoList.removeChild(toDoContainer)
    }) 


    // Maybe this can be something that will show when reviewing the to-do list after saving it
    // const checkbox = document.createElement("input");
    // checkbox.type = 'checkbox';
    // checkbox.id = 'completed_chkbox';
    // checkbox.name = 'completed_chkbox';
    // checkbox.value = 'completed';
    // toDoList.appendChild(checkbox);
    // console.log(checkbox)
});


document.querySelector("#create-trip").addEventListener('submit', (event) => {
    event.preventDefault();
    const departDate = document.querySelector("#leave_date").value;
    const returnDate = document.querySelector("#return_date").value;
    const toDest = document.querySelector("#to").value;
    const fromDest = document.querySelector("#from").value;
    const toDoListInputs = document.querySelectorAll(".to-do-list-item");
    const toDoListItems = [];
    for (const toDoListInput of toDoListInputs) {
        toDoListItems.push(toDoListInput.value);
    }

    const data = {
        depart_date:departDate,
        return_date:returnDate,
        to:toDest,
        from:fromDest,
        to_do_list_items:toDoListItems

    };

    fetch("/my-trips/create-trip", {
        method:"POST",
        body:JSON.stringify(data),
        headers:{'Content-Type': 'application/json'}
    })
    .then((response) => console.log(response))
    ;

});

// this click event removes the hidden class on the to-do-form  div which lets users create a list of to-dos for their trip  
document.querySelector("#create_list").addEventListener('click', (event) => {
    const toDoListButton = document.querySelector("#to-do-form");
    toDoListButton.classList.remove("hidden");
});


