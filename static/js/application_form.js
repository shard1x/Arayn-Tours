document.addEventListener('DOMContentLoaded', function() {
    const openBtn = document.getElementById('openApplicationFormBtn');
    const closeBtn = document.getElementById('closeApplicationFormBtn');
    const form = document.getElementById('applicationForm');
    const overlay = document.getElementById('overlay');

    // Изначально скрываем форму и оверлей
    form.style.display = 'none';
    overlay.style.display = 'none';

    // Функция для показа формы и оверлея
    function openForm() {
        form.style.display = 'block';
        overlay.style.display = 'block';
    }

    // Функция для скрытия формы и оверлея
    function closeForm() {
        form.style.display = 'none';
        overlay.style.display = 'none';
    }

    // Обработчик клика на кнопку "Оставить заявку"
    openBtn.addEventListener('click', openForm);

    // Обработчик клика на кнопку "Закрыть"
    closeBtn.addEventListener('click', closeForm);

    // Обработчик клика на оверлей
    overlay.addEventListener('click', closeForm);
});
