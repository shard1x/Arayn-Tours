document.addEventListener('DOMContentLoaded', function() {
    const openBtn = document.getElementById('openApplicationFormBtn');
    const form = document.getElementById('applicationForm');
    const closeBtn = document.getElementById('closeApplicationFormBtn');
    const overlay = document.getElementById('overlay');
    const formElem = document.getElementById('applicationFormElem');
    const nameInput = document.getElementById('name');
    const emailInput = document.getElementById('email');
    const phoneInput = document.getElementById('phone');
    const successNotification = document.getElementById('successNotification');
    const errorNotification = document.getElementById('errorNotification');

    let isFirstFocus = true; // Флаг для первого получения фокуса

    openBtn.addEventListener('click', function() {
        form.classList.remove('hidden');
        overlay.classList.remove('hidden');
    });

    closeBtn.addEventListener('click', function() {
        form.classList.add('hidden');
        overlay.classList.add('hidden');
        resetValidation(); //очищаем ошибки при закрытии
    });

    overlay.addEventListener('click', function() {
        form.classList.add('hidden');
        overlay.classList.add('hidden');
        resetValidation(); //очищаем ошибки при закрытии
    });

    // Функция для отображения сообщения об ошибке
    function showError(inputElement, message) {
        const errorDivId = inputElement.id + '-error';
        const errorDiv = document.getElementById(errorDivId);
        errorDiv.textContent = message;
        inputElement.classList.add('error'); // Добавляем класс 'error' к input
    }

    // Функция для очистки сообщения об ошибке
    function clearError(inputElement) {
        const errorDivId = inputElement.id + '-error';
        const errorDiv = document.getElementById(errorDivId);
        errorDiv.textContent = '';
        inputElement.classList.remove('error'); // Удаляем класс 'error' с input
    }

    // Функция для сброса всей валидации
    function resetValidation() {
        clearError(nameInput);
        clearError(emailInput);
        clearError(phoneInput);

        // Очищаем значения полей
        nameInput.value = '';
        emailInput.value = '';
        phoneInput.value = '';


        isFirstFocus = true; // Сбрасываем флаг первого фокуса
    }

    // Валидация имени (только буквы и пробелы)
    function validateName() {
        const nameValue = nameInput.value.trim();
        if (nameValue === '') {
            showError(nameInput, 'Имя обязательно для заполнения.');
            return false;
        }
        const nameRegex = /^[а-яА-Я\s]+$/; // Разрешены только русские буквы
        if (!nameRegex.test(nameValue)) {
            showError(nameInput, 'Имя может содержать только буквы русского алфавита.');
            return false;
        }
        clearError(nameInput);
        return true;
    }

    // Валидация email
    function validateEmail() {
        const emailValue = emailInput.value.trim();
        if (emailValue === '') {
            showError(emailInput, 'Email обязателен для заполнения.');
            return false;
        }
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(emailValue)) {
            showError(emailInput, 'Пожалуйста, введите корректный email.');
            return false;
        }
        clearError(emailInput);
        return true;
    }

    function formatPhoneNumber(value) {
        const digits = value.replace(/\D/g, ''); // Удаляем все нецифровые символы
        let formattedNumber = '';

        if (digits.length > 0) {
            formattedNumber += '+7';
        }
        if (digits.length > 1) {
            formattedNumber += ' (' + digits.substring(1, 4);
        }
        if (digits.length > 4) {
            formattedNumber += ') ' + digits.substring(4, 7);
        }
        if (digits.length > 7) {
            formattedNumber += '-' + digits.substring(7, 9);
        }
        if (digits.length > 9) {
            formattedNumber += '-' + digits.substring(9, 11);
        }

        return formattedNumber;
    }

   // Валидация телефона (Упрощенная версия)
function validatePhone() {
    let phoneValue = phoneInput.value.trim();
    const digits = phoneValue.replace(/\D/g, ''); // Оставляем только цифры

    if (phoneValue === '') {
        showError(phoneInput, 'Номер телефона обязателен для заполнения.');
        return false;
    }

    if (digits.length !== 11) {
        showError(phoneInput, 'Номер телефона должен содержать 11 цифр.');
        return false;
    }

    // Проверка, что начинается с +7 (или 7, если без плюса вводят)
    if (!phoneValue.startsWith('+7') && !phoneValue.startsWith('7')) {
        showError(phoneInput, 'Номер телефона должен начинаться с +7 или 7.');
        return false;
    }

    clearError(phoneInput);
    return true;
}


    // Обработчик ввода номера телефона
    phoneInput.addEventListener('input', function() {
        phoneInput.value = formatPhoneNumber(phoneInput.value);
    });

    // Обработчик фокуса
    phoneInput.addEventListener('focus', function() {
        if (isFirstFocus) {
            phoneInput.value = '+7 (';
            isFirstFocus = false;
        }
    });

     // Обработчик потери фокуса
     phoneInput.addEventListener('blur', function() {
         validatePhone(); // Валидация при потере фокуса
        if (phoneInput.value === '+7 (') {
            phoneInput.value = '';
            isFirstFocus = true;
              clearError(phoneInput);
        }

    });

    function showNotification(element) {
        element.classList.add('show');
        setTimeout(() => {
            element.classList.remove('show');
        }, 3000); // Скрыть через 3 секунды
    }

    // Обработчик отправки формы
    formElem.addEventListener('submit', function(event) {
        event.preventDefault(); // Предотвращаем отправку формы по умолчанию

        const isNameValid = validateName();
        const isEmailValid = validateEmail();
        const isPhoneValid = validatePhone();

        if (!isNameValid || !isEmailValid || !isPhoneValid) {
            showNotification(errorNotification);
            return;
        }

        // Если все поля валидны, можно отправлять форму
        console.log('Форма отправлена!'); // Замените на реальную отправку
        form.classList.add('hidden');
        overlay.classList.add('hidden');
        resetValidation(); //очищаем ошибки после отправки
        showNotification(successNotification);

    });


    nameInput.addEventListener('input', validateName);
    emailInput.addEventListener('input', validateEmail);
    //phoneInput.addEventListener('input', validatePhone); // Убрали валидацию при вводе
});
