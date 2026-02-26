const { chromium } = require('playwright');

(async () => {
    const browser = await chromium.launch({ headless: true });
    const context = await browser.newContext();
    const page = await context.newPage();

    page.on('console', msg => console.log(`[PAGE CONSOLE] ${msg.type()}: ${msg.text()}`));
    page.on('pageerror', error => console.error(`[PAGE ERROR] ${error.message}`));

    console.log('Navigating to game directly...');
    await page.goto('http://localhost:5173/games/iceout/index.html');
    await page.waitForTimeout(2000);
    console.log('Clicking the screen...');
    await page.click('#canvas');
    await page.waitForTimeout(10000); // 10s wait is enough since we only need boot logs

    // Dump python terminal
    const terminalText = await page.$eval('#terminal', el => el.innerText);
    console.log("=== PYTHON TERMINAL DUMP ===");
    console.log(terminalText);
    console.log("============================");

    await browser.close();
})();
