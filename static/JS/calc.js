'use strict';


document.querySelector('#gas-form').addEventListener('submit', (evt) => {
  evt.preventDefault();

  // Get user input from a form
  const distance = document.querySelector('#distance_mi').value
  const mpg = document.querySelector('#mpg').value
  const price = document.querySelector('#price').value
  const total = (distance/mpg) * price
  const total_gallons = (distance/mpg)
  console.log(total)
  console.log(total_gallons)
  const money_total = total.toFixed(2);
  const total_gallons_formatted =  total_gallons.toFixed(2)

  document.querySelector('#gas_total').value = ('$'+money_total);
  document.querySelector('#gallons_needed').value = total_gallons_formatted;

});