const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const path = require('path');

(async () => {
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
  const fileUrl = 'file://' + path.resolve(__dirname, 'index.html');
  await page.goto(fileUrl, { waitUntil: 'networkidle' });

  const total = await page.evaluate(() => document.querySelectorAll('.slide').length);
  console.log('total slides:', total);

  // Disable transitions/animations and nav UI for clean print, force each slide visible+static in turn
  await page.addStyleTag({ content: `
    * { animation: none !important; transition: none !important; }
    #nav { display: none !important; }
    body { margin: 0; }
  `});

  for (let i = 0; i < total; i++) {
    await page.evaluate((idx) => {
      document.querySelectorAll('.slide').forEach((s, j) => {
        s.classList.remove('active', 'exit');
        s.style.opacity = '';
        s.style.transform = '';
        s.style.position = 'absolute';
        s.style.display = 'none';
        if (j === idx) {
          s.classList.add('active');
          s.style.display = 'flex';
          s.style.position = 'relative';
          s.style.opacity = '1';
          s.style.transform = 'none';
        }
      });
    }, i);
    await page.waitForTimeout(150);
    await page.pdf({
      path: path.resolve(__dirname, `slide_${String(i+1).padStart(2,'0')}.pdf`),
      width: '1920px',
      height: '1080px',
      printBackground: true,
      pageRanges: '1',
      margin: { top: 0, bottom: 0, left: 0, right: 0 },
    });
  }

  await browser.close();
  console.log('done');
})();
