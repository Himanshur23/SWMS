document.addEventListener("DOMContentLoaded", function() {
  fetch('/user_home')
    .then(response => response.json())
    .then(user_data => {
      for (let i = 1; i <= 31; i++) {
        let day_data = user_data['d' + i];
        if (day_data) {
          let day_cell = document.querySelector('.day-' + i);
          day_cell.style.background = 'red';
        }
      }
    })
    .catch(error => console.error(error));
});