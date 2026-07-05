# Puppeteer Quick Reference

## Setup

```javascript
import puppeteer from 'puppeteer';

const browser = await puppeteer.launch({
  headless: true,
  args: ['--no-sandbox'],
  defaultViewport: { width: 1920, height: 1080 },
  slowMo: 250  // slow down by 250ms per action
});

const page = await browser.newPage();
await page.goto('https://example.com');
await browser.close();
```

## Browser & Page Management

```javascript
// Launch options
const browser = await puppeteer.launch({
  headless: false,
  executablePath: '/path/to/chrome',
  userDataDir: './user-data',
  devtools: true
});

// Connect to running Chrome
const browser = await puppeteer.connect({ browserURL: 'http://localhost:9222' });

// Page management
const pages = await browser.pages();
const page2 = await browser.newPage();
await page.close();

// Isolated context (incognito)
const context = await browser.createBrowserContext();
const page = await context.newPage();
await context.close();
```

## Navigation

```javascript
await page.goto('https://example.com', {
  waitUntil: 'networkidle2',  // load | domcontentloaded | networkidle0 | networkidle2
  timeout: 30000
});

await page.reload({ waitUntil: 'networkidle2' });
await page.goBack();
await page.goForward();
await page.waitForNavigation({ waitUntil: 'networkidle2' });
```

## Element Interaction

### Selectors

```javascript
await page.$('#id');
await page.$('.class');
await page.$('div > p');
await page.$x('//button[text()="Submit"]');
await page.$$('.item');         // all matches
```

### Click & Type

```javascript
await page.click('.button');
await page.click('.button', { button: 'left', clickCount: 2, delay: 100 });
await page.type('#search', 'query', { delay: 100 });

const btn = await page.$('.button');
await btn.click();
```

### Forms

```javascript
await page.type('#username', 'john@example.com');
await page.type('#password', 'secret123');
await page.select('#country', 'US');
await page.click('input[type="checkbox"]');
await page.click('button[type=submit]');

// Upload
const input = await page.$('input[type="file"]');
await input.uploadFile('/path/to/file.pdf');
```

### Hover, Focus, Drag

```javascript
await page.hover('.menu-item');
await page.focus('#input');
await page.$eval('#input', el => el.blur());

const source = await page.$('.draggable');
const target = await page.$('.drop-zone');
await source.drag(target);
```

## JavaScript Execution

```javascript
// Evaluate
const title = await page.evaluate(() => document.title);
const text = await page.evaluate(sel => document.querySelector(sel).textContent, '.heading');

// Return complex data
const data = await page.evaluate(() => ({ title: document.title, url: location.href }));

// DOM query
const value = await page.$eval('#input', el => el.value);
const items = await page.$$eval('.item', els => els.map(el => el.textContent));

// Modify
await page.$eval('#input', (el, val) => { el.value = val; }, 'new value');

// Expose Node.js function
await page.exposeFunction('md5', text => crypto.createHash('md5').update(text).digest('hex'));
```

## Screenshots & PDF

```javascript
await page.screenshot({ path: 'page.png', fullPage: true });
await page.screenshot({ path: 'clip.png', clip: { x: 0, y: 0, width: 500, height: 500 } });

const element = await page.$('.chart');
await element.screenshot({ path: 'chart.png' });

await page.pdf({ path: 'page.pdf', format: 'A4', printBackground: true });
```

## Network Interception

```javascript
await page.setRequestInterception(true);

page.on('request', (request) => {
  if (request.resourceType() === 'image') request.abort();
  else if (request.url().includes('ads')) request.abort();
  else if (request.url().includes('api')) request.continue({ headers: { ...request.headers(), 'Authorization': 'Bearer token' } });
  else request.continue();
});

// Mock response
page.on('request', (request) => {
  if (request.url().includes('/api/user')) {
    request.respond({ status: 200, contentType: 'application/json', body: JSON.stringify({ id: 1 }) });
  }
});
```

## Device Emulation

```javascript
import { devices } from 'puppeteer';
await page.emulate(devices['iPhone 13 Pro']);
await page.emulate(devices['Pixel 5']);

// Custom
await page.emulate({
  viewport: { width: 375, height: 812, deviceScaleFactor: 3, isMobile: true, hasTouch: true },
  userAgent: 'Mozilla/5.0 ...'
});

await page.setViewport({ width: 1920, height: 1080 });
await page.setGeolocation({ latitude: 37.7749, longitude: -122.4194 });
await page.emulateTimezone('America/New_York');
```

## Performance

```javascript
// CPU throttling
const client = await page.createCDPSession();
await client.send('Emulation.setCPUThrottlingRate', { rate: 4 });

// Network throttling
await page.emulateNetworkConditions(puppeteer.networkConditions['Slow 3G']);

// Metrics
const metrics = await page.metrics();

// Tracing
await page.tracing.start({ path: 'trace.json', categories: ['devtools.timeline'] });
await page.goto('https://example.com');
await page.tracing.stop();

// Coverage
await page.coverage.startJSCoverage();
await page.goto('https://example.com');
const jsCoverage = await page.coverage.stopJSCoverage();
```

## Common Patterns

### Waiting

```javascript
await page.waitForSelector('.element', { visible: true, timeout: 5000 });
await page.waitForFunction(() => document.querySelector('.loading') === null, { timeout: 10000 });
await page.waitForTimeout(2000);
```

### Dialogs

```javascript
page.on('dialog', async (dialog) => {
  console.log(dialog.type(), dialog.message());
  await dialog.accept();
  // await dialog.dismiss();
  // await dialog.accept('input');  // for prompts
});
```

### New Tabs

```javascript
const [newPage] = await Promise.all([
  new Promise(resolve => browser.once('targetcreated', target => resolve(target.page()))),
  page.click('a[target="_blank"]')
]);
```

### Frames

```javascript
const frame = page.frames().find(f => f.name() === 'myframe');
await frame.click('.button');
```

### Cookies

```javascript
const cookies = await page.cookies();
await page.setCookie({ name: 'session', value: 'abc', domain: 'example.com', path: '/' });
await page.deleteCookie({ name: 'session' });
```

### localStorage

```javascript
await page.evaluate(() => localStorage.setItem('key', 'value'));
const value = await page.evaluate(() => localStorage.getItem('key'));
await page.evaluate(() => localStorage.clear());
```

### Infinite Scroll

```javascript
async function autoScroll(page) {
  await page.evaluate(async () => {
    await new Promise(resolve => {
      let total = 0;
      const timer = setInterval(() => {
        window.scrollBy(0, 100);
        total += 100;
        if (total >= document.body.scrollHeight) { clearInterval(timer); resolve(); }
      }, 100);
    });
  });
}
```

### Error Handling

```javascript
try {
  await page.goto('https://example.com', { waitUntil: 'networkidle2', timeout: 30000 });
} catch (error) {
  await page.screenshot({ path: 'error.png' });
}
```

### Stealth Mode

```javascript
await page.evaluateOnNewDocument(() => {
  Object.defineProperty(navigator, 'webdriver', { get: () => false });
  window.chrome = { runtime: {} };
});
```

## Debugging

```javascript
// Console forwarding
page.on('console', msg => console.log('PAGE:', msg.text()));
page.on('pageerror', async (error) => {
  console.error('Error:', error);
  await page.screenshot({ path: `error-${Date.now()}.png` });
});

// Keep browser open
const browser = await puppeteer.launch({ headless: false, devtools: true, slowMo: 250 });
```
