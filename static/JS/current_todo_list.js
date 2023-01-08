document.querySelector("#view-to-dos").addEventListener('click', (event) => {
    const list = document.querySelector("#view-to-dos-container");
    const listContainer = document.createElement('div')
    listContainer.setAttribute('class', 'list-container')
    list.classList.remove("hidden");
   
    console.log(newToDoItem)
}
)