const tg = window.Telegram.WebApp;
tg.expand();

document.getElementById("spin").onclick = () => {
    const items = ["Blue", "Purple", "Pink", "Red", "Gold"];
    const weights = [79.9, 16, 3.2, 0.6, 0.2];

    let rnd = Math.random() * 100;
    let sum = 0;

    for (let i = 0; i < items.length; i++) {
        sum += weights[i];
        if (rnd <= sum) {
            document.getElementById("result").innerText = Выпало: ${items[i]};
            break;
        }
    }
};