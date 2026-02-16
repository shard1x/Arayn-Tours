// carousel.js
const prevBtn = document.getElementById('prevBtn');
const nextBtn = document.getElementById('nextBtn');
const cardsWrapper = document.getElementById('cardsWrapper');
// Получаем ширину карточки из CSS (включая margin)
const cardWidth = document.querySelector('.country-card').offsetWidth;
let currentPosition = 0;
const cardCount = cardsWrapper.children.length; // Количество карточек

nextBtn.addEventListener('click', () => {
    // Если не последняя карточка
    if (currentPosition < cardCount - 1) {
        currentPosition++; // Увеличиваем текущую позицию на 1
        // Сдвигаем wrapper на ширину одной карточки влево
        cardsWrapper.style.transform = `translateX(-${currentPosition * cardWidth}px)`;
    } else {
        // Если последняя, возвращаемся к началу
        currentPosition = 0;
        cardsWrapper.style.transform = `translateX(0)`;
    }
});

prevBtn.addEventListener('click', () => {
    // Если не первая карточка
    if (currentPosition > 0) {
        currentPosition--; // Уменьшаем текущую позицию на 1
        // Сдвигаем wrapper на ширину одной карточки вправо
        cardsWrapper.style.transform = `translateX(-${currentPosition * cardWidth}px)`;
    } else {
        // Если первая, переходим к последней карточке
        currentPosition = cardCount - 1; // Индекс последней карточки
        cardsWrapper.style.transform = `translateX(-${currentPosition * cardWidth}px)`;
    }
});
