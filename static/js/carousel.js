const prevBtn = document.getElementById('prevBtn');
const nextBtn = document.getElementById('nextBtn');
const cardsWrapper = document.getElementById('cardsWrapper');
const cardWidth = 300; // Ширина одной карточки (включая margin).  Важно!
let currentPosition = 0;

nextBtn.addEventListener('click', () => {
    const maxPosition = (cardsWrapper.children.length - 1) * cardWidth;  // Максимальная позиция прокрутки
    if (currentPosition < maxPosition) {
        currentPosition += cardWidth;
        cardsWrapper.style.transform = `translateX(-${currentPosition}px)`;
    } else {
        // Если достигли конца, можно вернуться к началу (зациклить)
        currentPosition = 0;
        cardsWrapper.style.transform = `translateX(0)`;
    }
});

prevBtn.addEventListener('click', () => {
    if (currentPosition > 0) {
        currentPosition -= cardWidth;
        cardsWrapper.style.transform = `translateX(-${currentPosition}px)`;
    } else {
        // Если в начале, можно перейти к концу (зациклить)
         const maxPosition = (cardsWrapper.children.length - 1) * cardWidth;
         currentPosition = maxPosition;
         cardsWrapper.style.transform = `translateX(-${currentPosition}px)`;

    }
});
