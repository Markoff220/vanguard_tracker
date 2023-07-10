const btn_choice_color = document.querySelectorAll('.btn_choice_color');
const form_color = document.querySelector('.form_color');
const color = document.querySelectorAll('.btn_color');

for (var i = 0, len = color.length; i < len; i++) {
    color[i].addEventListener('click', () => {
    form_color.showModal();
  });
};

btn_choice_color.forEach((item) => {
    item.addEventListener('click', () => {
    document.querySelector('#YN_data_input_color').value = item.style.background;
    document.querySelector('#HM_data_input_color').value = item.style.background;
    color[0].style.background = item.style.background;
    color[1].style.background = item.style.background;
    form_color.close();

  });
});


form_color.addEventListener('click', (e) => {
    if (e.target == form_color) {
     form_color.close();
  }
  });