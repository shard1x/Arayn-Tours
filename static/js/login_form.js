document.addEventListener('DOMContentLoaded', function() {
  // Получаем форму входа
  const loginForm = document.querySelector('form[action="/login"]');

  if (loginForm) {
    loginForm.addEventListener('submit', function(event) {
      event.preventDefault(); // Отменяем стандартную отправку формы

      // Удаляем предыдущие красные рамки, если они есть
      document.querySelectorAll('.red-border').forEach(el => el.classList.remove('red-border'));

      const usernameInput = loginForm.querySelector('input[name="username"]');
      const passwordInput = loginForm.querySelector('input[name="password"]');

      let isValid = true;

      // Валидация логина: проверка на пустую строку и допустимые символы
      if (!usernameInput.value || !/^[a-zA-Z0-9]+$/.test(usernameInput.value)) {
        usernameInput.classList.add('red-border');
        isValid = false;
      }

      // Валидация пароля: проверка на пустую строку, минимальную длину и допустимые символы
      if (passwordInput.value.length < 6 || !/^[a-zA-Z0-9]+$/.test(passwordInput.value)) {
        passwordInput.classList.add('red-border');
        isValid = false;
      }

      // Если форма валидна, отправляем данные через Fetch API
      if (isValid) {
        fetch(loginForm.action, {
          method: 'POST',
          body: new FormData(loginForm)
        })
        .then(response => {
          if (response.ok) {
            // Успешный вход, перенаправляем на главную страницу
            window.location.href = '/'; // Предполагается, что '/' - это главная страница
          } else {
            // Обработка ошибок сервера (например, неверный логин/пароль)
            console.error('Ошибка входа:', response.status);
            // Можно добавить отображение сообщения об ошибке пользователю
            // Например, добавив новый элемент с текстом ошибки или обведя поля красным
            usernameInput.classList.add('red-border');
            passwordInput.classList.add('red-border');
          }
        })
        .catch(error => {
          // Обработка ошибок сети
          console.error('Ошибка сети:', error);
          // Можно добавить отображение сообщения об ошибке сети
        });
      }
    });
  }
});
