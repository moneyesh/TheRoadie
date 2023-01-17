const headers = {
    'Content-Type': 'application/json'
}

document.querySelector("#view-to-dos").addEventListener('click', (event) => {
    const list = document.querySelector("#view-to-dos-container");
    const listContainer = document.createElement('div')
    listContainer.setAttribute('class', 'list-container')
    list.classList.remove("hidden");
   

    const checkbox = document.createElement("input");
    checkbox.type = 'checkbox';
    checkbox.id = 'completed_chkbox';
    checkbox.name = 'completed_chkbox';
    checkbox.value = 'completed';

}
)


    // select checkbox and do .check if equal to 

function completeToDo() {

    const checkboxes = document.querySelectorAll(".chkbox")
    let body = []
    for (let box of checkboxes) {
        console.log(box.checked, box.id)
        let boxObj = {
            task_id:box.id,
            completed:box.checked
        }
        body.push(boxObj)
    }
    console.log(body)
    // let body={
    //     task_id:to_do_id,
    //     checkbox:checkbox
    // }
    fetch(`/checkboxes`, {
        method:'POST',
        body:JSON.stringify(body), //change to json to send to server
        headers:headers //required in fetch. it tells what the format of the dictionary will represent. On line 1
    })
    .then(response => response.text()) //the response that we will get back from server.py
    .then(data => console.log(data))
    
    
    }
