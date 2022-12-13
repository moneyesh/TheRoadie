'use strict';

document.querySelector('#gas-form').addEventListener('submit', (evt) => {
  evt.preventDefault();

  // Get user input from a form
  const distance = document.querySelector('#distance_mi').value
  const mpg = document.querySelector('#mpg').value
  const price = document.querySelector('#price').value
  const total = mpg * distance * price
  console.log(total)

  document.querySelector('#gas_total').value = total;


});