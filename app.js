// Начальный счёт кристаллов
let crystals = 0;

// Получаем элемент для отображения счёта
const crystalsCount = document.getElementById('crystalsCount');

// Пример: увеличение кристаллов каждые 2 секунды
setInterval(() => {
    crystals += 10; // добавляем 10 кристаллов
    crystalsCount.textContent = `Кристаллы: ${crystals}`;
}, 2000);
