document.querySelector("#to-do-list-button").addEventListener('click', (event) => {
    const toDoList = document.querySelector("#to-do-list");
    const newToDoItem = document.createElement('input');
    newToDoItem.setAttribute('class', 'to-do-list-item');
    toDoList.appendChild(newToDoItem);
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