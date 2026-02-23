document.addEventListener('DOMContentLoaded', function() {
    const openBtn = document.getElementById('openApplicationFormBtn');
    const closeBtn = document.getElementById('closeApplicationFormBtn');
    const form = document.getElementById('applicationForm');
    const overlay = document.getElementById('overlay');

    // Скрываем форму и оверлей при загрузке страницы
    form.style.display = 'none';
    overlay.style.display = 'none';

    // Функция открытия формы
    function openForm() {
        form.style.display = 'block';
        overlay.style.display = 'block';
    }

    // Функция закрытия формы
    function closeForm() {
        form.style.display = 'none';
        overlay.style.display = 'none';
    }

    // Обработчики событий для открытия и закрытия формы
    openBtn.addEventListener('click', openForm);
    closeBtn.addEventListener('click', closeForm);
    overlay.addEventListener('click', closeForm);

    const phoneInput = document.getElementById('phone');

    // Форматирование номера телефона при вводе
    phoneInput.addEventListener('input', function() {
        let value = phoneInput.value.replace(/\D/g, '');
        if (!value.startsWith('7')) {
            value = '7' + value;
        }
        let formattedValue = '+7 ';
        if (value.length > 1) {
            formattedValue += value.substring(1, 4);
        }
        if (value.length > 4) {
            formattedValue += '-' + value.substring(4, 7);
        }
        if (value.length > 7) {
            formattedValue += '-' + value.substring(7, 9);
        }
        if (value.length > 9) {
            formattedValue += '-' + value.substring(9, 11);
        }
        phoneInput.value = formattedValue.substring(0, formattedValue.length);
    });

    // Валидация формы перед отправкой
    const formElement = document.querySelector('form');
    formElement.addEventListener('submit', function(event) {
        let isValid = true;

        // Очищаем предыдущие сообщения об ошибках
        document.querySelectorAll('.error-message').forEach(el => el.textContent = '');

        // Проверка имени
        const nameInput = document.getElementById('name');
        const nameRegex = /^[a-zA-Zа-яА-Я\s]+$/;
        if (!nameInput.value.trim()) {
            document.getElementById('name-error').textContent = 'Пожалуйста, введите имя.';
            isValid = false;
        } else if (!nameRegex.test(nameInput.value)) {
            document.getElementById('name-error').textContent = 'Имя должно содержать только буквы.';
            isValid = false;
        }

        // Проверка email
        const emailInput = document.getElementById('email');
        const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
        if (!emailInput.value.trim()) {
            document.getElementById('email-error').textContent = 'Пожалуйста, введите email.';
            isValid = false;
        } else if (!emailRegex.test(emailInput.value)) {
            document.getElementById('email-error').textContent = 'Пожалуйста, введите корректный email.';
            isValid = false;
        }

        // Проверка телефона
        const phoneRegex = /^\+7 \d{3}-\d{3}-\d{2}-\d{2}$/;
        if (!phoneInput.value.trim()) {
            document.getElementById('phone-error').textContent = 'Пожалуйста, введите номер телефона.';
            isValid = false;
        } else if (!phoneRegex.test(phoneInput.value)) {
            document.getElementById('phone-error').textContent = 'Номер телефона должен быть в формате +7 ХХХ-ХХХ-ХХ-ХХ.';
            isValid = false;
        }

            // Предотвращаем отправку формы, если валидация не пройдена
            if (!isValid) {
                event.preventDefault();
            } else {
                // Форма валидна, показываем сообщение об успехе и закрываем форму
                displaySuccessMessage();
                closeForm();
                // event.preventDefault(); <-- Удалите эту строку
            }

    });

    //создаем функцию для отображения сообщения
     function displaySuccessMessage() {
        // Создаем элемент сообщения
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('success-message');
        messageDiv.textContent = 'Заявка успешно отправлена';

        // Добавляем сообщение в body (можно изменить место добавления)
        document.body.appendChild(messageDiv);

        // Позиционируем сообщение в правом нижнем углу
        messageDiv.style.position = 'fixed';
        messageDiv.style.bottom = '20px';
        messageDiv.style.right = '20px';
        messageDiv.style.backgroundColor = 'green';
        messageDiv.style.color = 'white';
        messageDiv.style.padding = '10px';
        messageDiv.style.borderRadius = '5px';
        messageDiv.style.zIndex = '1000'; // Убедитесь, что сообщение поверх других элементов

        // Удаляем сообщение через 7 секунд
        setTimeout(() => {
            messageDiv.remove();
        }, 7000);
      }
});
