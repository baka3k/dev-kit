# Chrome DevTools Protocol Domains Reference

CDP is organized into 47 domains grouped by functionality.

## Core

**Runtime** — Execute JavaScript, manage objects, handle promises
- `Runtime.evaluate(expression)` — Execute JS
- `Runtime.callFunctionOn(functionDeclaration, objectId)` — Call function on object
- `Runtime.getProperties(objectId)` — Get object properties
- Events: `consoleAPICalled`, `exceptionThrown`

**Debugger** — JavaScript debugging, breakpoints, stack traces
- `Debugger.enable()`, `Debugger.setBreakpoint(location)`, `Debugger.pause()`, `Debugger.resume()`
- Events: `paused`, `resumed`, `scriptParsed`

## DOM & Styling

**DOM** — Access and manipulate DOM tree
- `DOM.getDocument()`, `DOM.querySelector(nodeId, selector)`, `DOM.querySelectorAll(nodeId, selector)`
- `DOM.getAttributes(nodeId)`, `DOM.setOuterHTML(nodeId, outerHTML)`, `DOM.getBoxModel(nodeId)`
- Events: `documentUpdated`, `setChildNodes`

**CSS** — Inspect and modify CSS styles
- `CSS.enable()`, `CSS.getComputedStyleForNode(nodeId)`, `CSS.getMatchedStylesForNode(nodeId)`, `CSS.setStyleTexts(edits)`
- Events: `styleSheetAdded`, `styleSheetChanged`

**Accessibility** — Access accessibility tree
- `Accessibility.getFullAXTree()`, `Accessibility.getPartialAXTree(nodeId)`, `Accessibility.queryAXTree(nodeId, role, name)`

## Network & Fetch

**Network** — Monitor and control HTTP traffic
- `Network.enable()`, `Network.setCacheDisabled(cacheDisabled)`, `Network.setExtraHTTPHeaders(headers)`
- `Network.getCookies(urls)`, `Network.setCookie(name, value, domain)`, `Network.getResponseBody(requestId)`
- `Network.emulateNetworkConditions(offline, latency, downloadThroughput, uploadThroughput)`
- Events: `requestWillBeSent`, `responseReceived`, `loadingFinished`, `loadingFailed`

**Fetch** — Intercept and modify network requests
- `Fetch.enable(patterns)`, `Fetch.continueRequest(requestId, url, method, headers)`
- `Fetch.fulfillRequest(requestId, responseCode, headers, body)`, `Fetch.failRequest(requestId, errorReason)`
- Events: `requestPaused`

## Page & Navigation

**Page** — Control page lifecycle and navigation
- `Page.navigate(url)`, `Page.reload(ignoreCache)`, `Page.goBack()/goForward()`
- `Page.captureScreenshot(format, quality)`, `Page.printToPDF(landscape)`, `Page.getLayoutMetrics()`
- `Page.handleJavaScriptDialog(accept, promptText)`
- Events: `loadEventFired`, `domContentEventFired`, `frameNavigated`, `javascriptDialogOpening`

**Target** — Manage browser targets (tabs, workers, frames)
- `Target.getTargets()`, `Target.createTarget(url)`, `Target.closeTarget(targetId)`
- `Target.attachToTarget(targetId)`, `Target.setDiscoverTargets(discover)`
- Events: `targetCreated`, `targetDestroyed`, `targetInfoChanged`

**Input** — Simulate user input
- `Input.dispatchKeyEvent(type, key, code)`, `Input.dispatchMouseEvent(type, x, y, button)`
- `Input.dispatchTouchEvent(type, touchPoints)`, `Input.synthesizeScrollGesture(x, y, xDistance, yDistance)`

## Storage & Data

**Storage** — Manage browser storage
- `Storage.getCookies(browserContextId)`, `Storage.setCookies(cookies)`, `Storage.clearCookies(browserContextId)`
- `Storage.clearDataForOrigin(origin, storageTypes)`, `Storage.getUsageAndQuota(origin)`
- Storage types: appcache, cookies, file_systems, indexeddb, local_storage, websql, service_workers, cache_storage

**DOMStorage** — Access localStorage/sessionStorage
- `DOMStorage.getDOMStorageItems(storageId)`, `DOMStorage.setDOMStorageItem(storageId, key, value)`

**IndexedDB** — Query IndexedDB databases
- `IndexedDB.requestDatabaseNames(securityOrigin)`, `IndexedDB.requestDatabase(securityOrigin, databaseName)`

**CacheStorage** — Manage Cache API
- `CacheStorage.requestCacheNames(securityOrigin)`, `CacheStorage.deleteCache(cacheId)`

## Performance & Profiling

**Performance** — Collect performance metrics
- `Performance.getMetrics()` — Timestamp, Documents, Frames, Nodes, LayoutCount, RecalcStyleCount, JSHeapUsedSize, JSHeapTotalSize

**PerformanceTimeline** — Access Performance Timeline API
- `PerformanceTimeline.enable(eventTypes)` — event types: mark, measure, navigation, resource, longtask, paint, layout-shift

**Tracing** — Record Chrome trace
- `Tracing.start(categories)`, `Tracing.end()`, `Tracing.requestMemoryDump()`
- Categories: blink, cc, devtools, gpu, loading, navigation, rendering, v8

**Profiler** — CPU profiling
- `Profiler.enable()`, `Profiler.start()`, `Profiler.stop()`

**HeapProfiler** (via Memory domain) — Memory profiling
- `Memory.getDOMCounters()`, `Memory.forciblyPurgeJavaScriptMemory()`

## Emulation & Simulation

**Emulation** — Emulate device conditions
- `Emulation.setDeviceMetricsOverride(width, height, deviceScaleFactor, mobile)`
- `Emulation.setGeolocationOverride(latitude, longitude, accuracy)`
- `Emulation.setTimezoneOverride(timezoneId)`, `Emulation.setLocaleOverride(locale)`
- `Emulation.setUserAgentOverride(userAgent)`

**DeviceOrientation** — Simulate device orientation
- `DeviceOrientation.setDeviceOrientationOverride(alpha, beta, gamma)`

## Workers & Services

**ServiceWorker** — Manage service workers
- `ServiceWorker.unregister(scopeURL)`, `ServiceWorker.startWorker(scopeURL)`, `ServiceWorker.stopWorker(versionId)`

**WebAuthn** — Simulate WebAuthn/FIDO2
- `WebAuthn.addVirtualAuthenticator(options)`, `WebAuthn.addCredential(authenticatorId, credential)`

## Developer Tools

**Log** — Collect browser logs
- `Log.enable()`, `Log.clear()`
- Events: `entryAdded`

**DOMDebugger** — DOM-level debugging
- `DOMDebugger.setDOMBreakpoint(nodeId, type)` — types: subtree-modified, attribute-modified, node-removed
- `DOMDebugger.setEventListenerBreakpoint(eventName)`, `DOMDebugger.setXHRBreakpoint(url)`

**DOMSnapshot** — Capture complete DOM snapshot
- `DOMSnapshot.captureSnapshot(computedStyles)`

**LayerTree** — Inspect rendering layers
- `LayerTree.compositingReasons(layerId)`

## Other

**Browser** — Browser-level control
- `Browser.getVersion()`, `Browser.getBrowserCommandLine()`, `Browser.setPermission(permission, setting, origin)`
- `Browser.grantPermissions(permissions, origin)` — permissions: geolocation, notifications, camera, microphone, clipboard-read, clipboard-write

**BackgroundService** — Track background services
- `BackgroundService.startObserving(service)` — services: backgroundFetch, backgroundSync, pushMessaging, notifications

## Domain Dependencies

```
Runtime (no dependencies)
  ↓
DOM (depends on Runtime)
  ↓
CSS (depends on DOM)

Network (no dependencies)

Page (depends on Runtime)
  ↓
Target (depends on Page)

Debugger (depends on Runtime)
```

## Best Practices

1. Always call `.enable()` for stateful domains
2. Subscribe to events for real-time updates
3. Disable domains when done to reduce overhead
4. Use sessions for isolated debugging
5. Version awareness: check browser version for experimental APIs
