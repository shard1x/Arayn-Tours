document.addEventListener('DOMContentLoaded', function() {
  // Функция для валидации формы регистрации
  function validateForm() {
    const username = document.querySelector('input[name="username"]').value;
    const email = document.querySelector('input[name="email"]').value;
    const password = document.querySelector('input[name="password"]').value;

    const usernameError = document.createElement('div');
    const emailError = document.createElement('div');
    const passwordError = document.createElement('div');

    clearErrors();

    let isValid = true;

    if (!/^[a-zA-Z0-9]+$/.test(username)) {
      usernameError.textContent = "Логин: только англ. буквы и цифры.";
      usernameError.classList.add('error');
      document.querySelector('input[name="username"]').parentNode.appendChild(usernameError);
      isValid = false;
    }

    if (!/^[a-zA-Z0-9]+@[a-zA-Z0-9.]+$/.test(email)) {
      emailError.textContent = "Почта: некорректный формат.";
      emailError.classList.add('error');
      document.querySelector('input[name="email"]').parentNode.appendChild(emailError);
      isValid = false;
    }

    if (password.length < 8 || !/^[a-zA-Z0-9]+$/.test(password)) {
      passwordError.textContent = "Пароль: мин. 8 символов, только англ. буквы и цифры.";
      passwordError.classList.add('error');
      document.querySelector('input[name="password"]').parentNode.appendChild(passwordError);
      isValid = false;
    }

    return isValid;
  }

  // Очистка ошибок
  function clearErrors() {
    const errors = document.querySelectorAll('.error');
    errors.forEach(error => error.remove());
  }

  const form = document.querySelector('form');

  if (form) {
    form.addEventListener('submit', function(event) {
      event.preventDefault(); // Отмена отправки формы по умолчанию

      if (!validateForm()) return; // Если валидация не пройдена

      // Отправка данных через fetch
      fetch(form.action, {
        method: 'POST',
        body: new FormData(form)
      })
      .then(response => {
        if (response.ok) {
          // Перенаправление при успехе.  Замените '/login' на нужный вам URL.
          window.location.href = '/login';
        } else {
          console.error('Ошибка:', response.status); // Вывод ошибки
        }
      })
      .catch(error => {
        console.error('Ошибка сети:', error); // Вывод ошибки сети
      });
    });
  }
});
