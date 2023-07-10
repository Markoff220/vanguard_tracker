document.querySelectorAll('.data_input_frequency').forEach((item) => {
    item.addEventListener('click', () => {
        document.querySelector('.form_frequency').showModal();
        });
        });



//Добавление нового элементы
const myDialog = document.querySelector('#addWindows');

document.querySelector('#bt_add').addEventListener('click', () => {

    myDialog.showModal();
  });

//Проверка на клик вне поля
myDialog.addEventListener('click', (e) => {
  if (e.target == myDialog) {
     myDialog.close();
  }
});
//



// Новая привычка да / нет
document.querySelector('#BtnYN').addEventListener('click', () => {
    document.querySelector('#addHabitYN').showModal();
  });

// Новая измеримая привычка
document.querySelector('#BtnHM').addEventListener('click', () => {
    document.querySelector('#addHabitHM').showModal();
  });


// Изменение количественной привычки
const EditValueHabitForm = document.querySelector('.edit_hm_action_form')

EditValueHabitForm.addEventListener('click', (e) => {
    if (e.target == EditValueHabitForm) {
        EditValueHabitForm.close();
    }
});
