# Performance Analysis Guide

Web performance analysis using Puppeteer and chrome-devtools skill scripts.

## Core Web Vitals

- **LCP** (Largest Contentful Paint) — Loading performance, < 2.5s good
- **FID** (First Input Delay) — Interactivity, < 100ms good
- **CLS** (Cumulative Layout Shift) — Visual stability, < 0.1 good

### Measuring with Puppeteer

```javascript
const vitals = await page.evaluate(() => {
  return new Promise((resolve) => {
    const vitals = { LCP: null, FID: null, CLS: 0 };

    new PerformanceObserver((list) => {
      const entries = list.getEntries();
      vitals.LCP = entries[entries.length - 1].renderTime || entries[entries.length - 1].loadTime;
    }).observe({ entryTypes: ['largest-contentful-paint'] });

    new PerformanceObserver((list) => {
      vitals.FID = list.getEntries()[0].processingStart - list.getEntries()[0].startTime;
    }).observe({ entryTypes: ['first-input'] });

    new PerformanceObserver((list) => {
      list.getEntries().forEach((entry) => {
        if (!entry.hadRecentInput) vitals.CLS += entry.value;
      });
    }).observe({ entryTypes: ['layout-shift'] });

    setTimeout(() => resolve(vitals), 5000);
  });
});
```

### Other Metrics

```javascript
// TTFB
const ttfb = await page.evaluate(() => {
  const [nav] = performance.getEntriesByType('navigation');
  return nav.responseStart - nav.requestStart;
});

// FCP
const fcp = await page.evaluate(() => {
  const paints = performance.getEntriesByType('paint');
  return paints.find(e => e.name === 'first-contentful-paint')?.startTime;
});

// FPS
const fps = await page.evaluate(() => {
  return new Promise((resolve) => {
    let frames = 0, lastTime = performance.now();
    function count() { frames++; requestAnimationFrame(count); }
    count();
    setTimeout(() => resolve(frames / ((performance.now() - lastTime) / 1000)), 5000);
  });
});
```

## Performance Tracing

```javascript
await page.tracing.start({
  path: 'trace.json',
  categories: ['devtools.timeline', 'disabled-by-default-devtools.timeline']
});
await page.goto('https://example.com', { waitUntil: 'networkidle2' });
await page.tracing.stop();
// Analyze in chrome://tracing
```

## Network Analysis

### Monitor Requests

```javascript
page.on('request', (request) => {
  console.log(request.method(), request.url(), request.resourceType());
});

page.on('response', (response) => {
  console.log(response.status(), response.url(), response.fromCache());
});

page.on('requestfailed', (request) => {
  console.log('Failed:', request.failure().errorText, request.url());
});
```

### Calculate Page Weight

```javascript
let totalBytes = 0;
page.on('response', async (response) => {
  const buffer = await response.buffer();
  totalBytes += buffer.length;
});
```

### Network Throttling

```javascript
// Puppeteer
const client = await page.createCDPSession();
await client.send('Network.emulateNetworkConditions', {
  offline: false,
  downloadThroughput: 400 * 1024 / 8,
  uploadThroughput: 400 * 1024 / 8,
  latency: 2000
});

// Predefined
await page.emulateNetworkConditions(puppeteer.networkConditions['Slow 3G']);
```

## JavaScript Performance

### Long Tasks

```javascript
const longTasks = await page.evaluate(() => {
  return new Promise((resolve) => {
    const tasks = [];
    const observer = new PerformanceObserver((list) => {
      list.getEntries().forEach(e => tasks.push({ duration: e.duration, startTime: e.startTime }));
    });
    observer.observe({ entryTypes: ['longtask'] });
    setTimeout(() => { observer.disconnect(); resolve(tasks); }, 10000);
  });
});
```

### CPU Profiling

```javascript
const client = await page.createCDPSession();
await client.send('Profiler.enable');
await client.send('Profiler.start');
await page.goto('https://example.com');
const { profile } = await client.send('Profiler.stop');
```

### Code Coverage

```javascript
await Promise.all([page.coverage.startJSCoverage(), page.coverage.startCSSCoverage()]);
await page.goto('https://example.com');
const [jsCov, cssCov] = await Promise.all([page.coverage.stopJSCoverage(), page.coverage.stopCSSCoverage()]);

for (const entry of [...jsCov, ...cssCov]) {
  let used = 0;
  for (const range of entry.ranges) used += range.end - range.start - 1;
  console.log(`${entry.url}: ${(used / entry.text.length * 100).toFixed(1)}% used`);
}
```

## Rendering Performance

### Paint Metrics

```javascript
const paints = await page.evaluate(() => {
  const entries = performance.getEntriesByType('paint');
  return {
    firstPaint: entries.find(p => p.name === 'first-paint')?.startTime,
    firstContentfulPaint: entries.find(p => p.name === 'first-contentful-paint')?.startTime
  };
});
```

### Layout Shifts (CLS)

```javascript
const { totalCLS, shifts } = await page.evaluate(() => {
  return new Promise((resolve) => {
    const shifts = [];
    let totalCLS = 0;
    const observer = new PerformanceObserver((list) => {
      list.getEntries().forEach((entry) => {
        if (!entry.hadRecentInput) { totalCLS += entry.value; shifts.push(entry); }
      });
    });
    observer.observe({ entryTypes: ['layout-shift'] });
    setTimeout(() => { observer.disconnect(); resolve({ totalCLS, shifts }); }, 10000);
  });
});
```

## Memory Analysis

```javascript
// Page metrics
const metrics = await page.metrics();
// { JSHeapUsedSize, JSHeapTotalSize, Nodes, Documents, JSEventListeners, LayoutCount, ... }

// Memory leak detection
async function detectLeak(page, duration = 30000) {
  const samples = [];
  for (let i = 0; i < duration / 1000; i++) {
    const m = await page.metrics();
    samples.push({ time: i, heap: m.JSHeapUsedSize });
    await page.waitForTimeout(1000);
  }
  const increase = ((samples.at(-1).heap - samples[0].heap) / samples[0].heap * 100).toFixed(2);
  return { samples, memoryIncrease: increase + '%', possibleLeak: increase > 50 };
}
```

## Optimization

### Oversized Images

```javascript
const oversized = await page.evaluate(() =>
  Array.from(document.querySelectorAll('img'))
    .filter(img => img.naturalWidth > img.width * 1.5)
    .map(img => ({ src: img.src, natural: img.naturalWidth, display: img.width }))
);
```

### Render-Blocking Resources

```javascript
const blocking = await page.evaluate(() =>
  performance.getEntriesByType('resource')
    .filter(r => (r.initiatorType === 'link' && r.name.includes('.css')) ||
                 (r.initiatorType === 'script' && !r.name.includes('async')))
    .map(r => ({ url: r.name, duration: r.duration }))
);
```

## Performance Budgets

```javascript
const budgets = {
  LCP: 2500, FID: 100, CLS: 0.1, FCP: 1800,
  totalPageSize: 2 * 1024 * 1024,
  jsSize: 500 * 1024, cssSize: 100 * 1024
};

async function checkBudgets(page, budgets) {
  const violations = [];
  const metrics = await page.metrics();
  const resources = await analyzeResources(page); // implement as needed

  if (vitals.LCP > budgets.LCP) violations.push(`LCP: ${vitals.LCP}ms > ${budgets.LCP}ms`);
  if (resources.totalSize > budgets.totalPageSize) violations.push(`Page size: ${resources.totalSize} > budget`);
  return { passed: violations.length === 0, violations };
}
```

## CI/CD Integration

```javascript
async function performanceTest(url) {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  await page.goto(url, { waitUntil: 'networkidle2' });
  const metrics = await page.metrics();
  const vitals = await measureCoreWebVitals(page);
  await browser.close();

  const thresholds = { LCP: 2500, FID: 100, CLS: 0.1, jsHeapSize: 50 * 1024 * 1024 };
  const failed = [];
  if (vitals.LCP > thresholds.LCP) failed.push('LCP');
  if (vitals.FID > thresholds.FID) failed.push('FID');
  if (vitals.CLS > thresholds.CLS) failed.push('CLS');
  if (metrics.JSHeapUsedSize > thresholds.jsHeapSize) failed.push('Memory');

  if (failed.length > 0) { console.error('Failed:', failed); process.exit(1); }
  console.log('Passed');
}
```

## Best Practices

1. Run tests 3-5 times, use median values
2. Test on Fast 3G, Slow 3G, and with CPU throttling
3. Test mobile and desktop viewports
4. Track metrics over time in CI/CD
5. Prioritize Core Web Vitals for user experience
6. Minimize render-blocking resources, defer non-critical JS, optimize fonts
