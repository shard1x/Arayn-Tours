document.addEventListener('DOMContentLoaded', function() {
  // Функция для валидации формы регистрации
  function validateForm() {
    const usernameInput = document.querySelector('input[name="username"]');
    const emailInput = document.querySelector('input[name="email"]');
    const passwordInput = document.querySelector('input[name="password"]');

    // Удаляем предыдущие красные рамки, если они есть
    document.querySelectorAll('.red-border').forEach(el => el.classList.remove('red-border'));

    let isValid = true;

    // Валидация имени пользователя
    // Требования: минимум 5 символов, обязательно хотя бы одна буква, можно цифры
    const usernameValue = usernameInput.value;
    if (usernameValue.length < 5 || !/[a-zA-Z]/.test(usernameValue) || !/^[a-zA-Z0-9]+$/.test(usernameValue)) {
      usernameInput.classList.add('red-border');
      isValid = false;
    }

    // Валидация email (ваш текущий код)
    if (!/^[a-zA-Z0-9]+@[a-zA-Z0-9.]+$/.test(emailInput.value)) {
      emailInput.classList.add('red-border');
      isValid = false;
    }

    // Валидация пароля (ваш текущий код)
    if (passwordInput.value.length < 8 || !/^[a-zA-Z0-9]+$/.test(passwordInput.value)) {
      passwordInput.classList.add('red-border');
      isValid = false;
    }

    return isValid;
  }

  // Обработчик отправки формы
  const form = document.querySelector('form');
  if (form) {
    form.addEventListener('submit', function(event) {
      event.preventDefault(); // Отмена отправки формы по умолчанию

      if (!validateForm()) {
        // Если валидация не пройдена, выходим из функции
        return;
      }

      // Отправка данных через fetch, если валидация успешна
      fetch(form.action, {
        method: 'POST',
        body: new FormData(form)
      })
      .then(response => {
        if (response.ok) {
          // Перенаправление при успехе. Замените '/login' на нужный вам URL.
          window.location.href = '/login';
        } else {
          console.error('Ошибка:', response.status); // Вывод ошибки
          // Можно добавить визуальное оповещение об общей ошибке сервера, если нужно
        }
      })
      .catch(error => {
        console.error('Ошибка сети:', error); // Вывод ошибки сети
        // Можно добавить визуальное оповещение об ошибке сети
      });
    });
  }
});
