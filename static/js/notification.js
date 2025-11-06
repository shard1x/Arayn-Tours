// notification.js
document.addEventListener('DOMContentLoaded', function() {
    const submitBtn = document.getElementById('submitBtn');
    const notification = document.getElementById('notification');
    const form = document.getElementById('applicationFormElem');

    submitBtn.addEventListener('click', function(event) {
        event.preventDefault(); // Предотвращаем отправку формы по умолчанию

       // Симуляция успешной отправки
        setTimeout(function() {
            // Показываем уведомление
            notification.classList.add('show');

            // Скрываем уведомление через 3 секунды
            setTimeout(function() {
                notification.classList.remove('show');
            }, 3000);

           // Скрываем форму
            const formElem = document.getElementById('applicationForm');
            formElem.classList.add('hidden');

             // Скрываем оверлей
            const overlay = document.getElementById('overlay');
            overlay.classList.add('hidden');

        }, 500); // Delay для имитации отправки
    });
});
