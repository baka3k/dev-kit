# Data visualization playbook

Use this reference whenever a slide contains numeric evidence, a chart, a KPI,
or a quantitative comparison.

## Contents

1. Start with the analytical question
2. Validate and compute
3. Select the chart
4. Apply the template style
5. Build native charts
6. Write the takeaway
7. Chart QA

## 1. Start with the analytical question

State the question before choosing a visual:

- How has a measure changed over time?
- Which categories are larger or smaller?
- How does composition differ across groups or periods?
- What explains the change from a starting value to an ending value?
- Are two measures related?
- How is a measure distributed?
- How does actual performance compare with a target or benchmark?
- Which metric is the decision signal?

A chart must answer one primary question. If it attempts to answer several,
split the analysis across slides.

## 2. Validate and compute

Before design:

1. Preserve a clean source table and never overwrite the original data.
2. Confirm the grain: one row per what, measured when, for which population.
3. Confirm units, currency, scale, denominator, period, and timezone when relevant.
4. Identify missing, duplicate, suppressed, estimated, and outlier values.
5. Recalculate totals, shares, averages, deltas, and rates from source values.
6. Decide whether category order is chronological, ranked, or semantically fixed.
7. Define rounding only after calculations; never calculate from displayed rounded
   values.
8. Preserve uncertainty or ranges. Do not turn a range into a point estimate.

Useful calculations:

- Absolute change = final minus initial.
- Percentage change = (final minus initial) divided by absolute initial.
- Share = part divided by total, using the same scope and period.
- Weighted average = sum(value times weight) divided by sum(weight).
- CAGR = (final divided by initial) raised to (1 divided by years), minus 1; use
  only for positive comparable endpoints and state the period.
- Variance to target = actual minus target; also show percent variance when the
  target is non-zero.

Do not infer causation from correlation, rank small differences without noting
uncertainty, or combine measures with incompatible definitions.

## 3. Select the chart

| Analytical question | Preferred chart | Notes |
| --- | --- | --- |
| Trend over ordered time | Line | One to four series; direct-label endpoints |
| Category ranking | Horizontal bar | Sort descending unless order has meaning |
| Few categories over time | Column | Keep categories and periods limited |
| Composition across groups | 100% stacked bar | Use when each group totals 100% |
| Contribution to total change | Waterfall | Reconcile start + changes = end |
| Actual vs target | Bar/bullet-style bar | Highlight variance, not decoration |
| Relationship of two measures | Scatter | Show sample size; add trendline only if useful |
| Distribution | Histogram or box/whisker | State bin or quartile method |
| A single decision metric | KPI + small trend | Always include context or benchmark |
| Part-to-whole with 2–5 stable parts | Doughnut, cautiously | Prefer bar if labels or differences matter |
| Detailed values are primary | Table | Use when lookup precision beats pattern recognition |

Avoid:

- pie/doughnut charts with more than five slices;
- radar charts for ordinary comparisons;
- 3D charts;
- dual-axis charts unless the relationship is essential and clearly labeled;
- maps when geography is not the analytical question;
- area charts when overlap hides values;
- decorative icons scaled as data marks.

## 4. Apply the template style

Use the palette from `reference-template.md`:

- Primary series: navy `#1F3864`.
- Single highlighted series or point: orange `#F37021`.
- Secondary series: teal `#127E84`.
- Positive/achieved series: green `#1E9E54`.
- Testing/validation series when semantically appropriate: purple `#7E4FB8`.
- Gridlines: cool gray `#EEF1F6`.
- Axis and secondary text: `#5A6370`.
- Plot and chart area: white.

Styling rules:

- Use one highlight. Do not color every bar differently.
- Remove chart borders and background decoration.
- Prefer no legend for one series; direct-label series or endpoints.
- Use light major gridlines only when they aid estimation.
- Use data labels selectively: endpoints, maxima/minima, target variance, or the
  decision-relevant point.
- Keep labels horizontal when possible. Use horizontal bars for long categories.
- Use zero as the value-axis baseline for bars and columns.
- For line charts, a non-zero baseline may be valid but must not exaggerate the
  change; provide axis context.
- Format numbers consistently: for example `1.2M`, `23%`, or `¥4.6B`, not mixed
  scales on the same axis.
- Put title and key message outside the chart area using the selected archetype's
  title and message zones. Avoid repeating the same title inside the chart.

## 5. Build native charts

Use `@oai/artifact-tool` native charts so the data remains editable. Read the
runtime chart API reference before authoring. A template-styled horizontal bar
pattern is:

```js
slide.charts.add("bar", {
  position: { left: 76, top: 200, width: 760, height: 330 },
  categories,
  series: [{
    name: seriesName,
    values,
    fill: "#1F3864",
    points: [{ idx: highlightIndex, fill: "#F37021" }],
  }],
  barOptions: { direction: "bar", grouping: "clustered", gapWidth: 48 },
  hasLegend: false,
  chartFill: "#FFFFFF",
  plotAreaFill: "#FFFFFF",
  xAxis: {
    visible: false,
    majorGridlines: null,
    numberFormatCode,
  },
  yAxis: {
    textStyle: { fill: "#5A6370", fontSize: 13 },
    line: { style: "solid", fill: "#EEF1F6", width: 1 },
  },
  dataLabels: {
    showValue: true,
    position: "outEnd",
    textStyle: { fill: "#1A284A", fontSize: 13, bold: true },
  },
});
```

Adapt the position to one of the bounded chart zones in
`reference-template.md`. If the user supplies a different template, inspect it
at runtime rather than assuming the example coordinates still fit.

For line charts:

- use a 2.5–3 px navy line for the primary series;
- use a teal line for one comparator;
- use markers only when observations are sparse;
- label the final point and any decision threshold;
- use muted gray gridlines and no surrounding box.

For waterfall charts:

- verify the arithmetic reconciliation;
- use navy for start/end totals;
- use teal/green for favorable contributions and orange for adverse or
  decision-relevant contributions;
- label the start, end, and major drivers.

For 100% stacked bars:

- verify each group sums to 100% within rounding tolerance;
- keep category colors stable across every group and slide;
- directly label meaningful segments; group tiny residual segments as “Other”
  only with a documented rule.

## 6. Write the takeaway

The slide title should state the result that changes the decision. Examples:

- “Cycle time fell 18% after pilot launch”
- “Two teams account for 64% of open defects”
- “Pilot scope reaches the target within 11 weeks”

Use only titles directly supported by computed data. If the evidence is
directional or uncertain, say so: “Early data suggests…”, “Within this sample…”,
or “Range reflects…”.

Pair the chart with at most one short interpretation block:

- what changed;
- why it matters;
- what decision or next step follows.

Do not narrate every point visible in the chart.

## 7. Chart QA

Before delivery:

- reconcile plotted values against the clean source table;
- verify sorting, category order, series order, units, labels, totals, and rounding;
- verify shares and stacked charts sum correctly;
- verify waterfall start + contributions = end;
- verify no label is clipped, overlapped, or too small at full-slide view;
- verify the orange highlight matches the slide takeaway;
- verify color meanings remain consistent across slides;
- verify axes do not distort the conclusion;
- verify the source, period, scope, sample size, and calculation method are in
  notes or a compact footer;
- verify the title is supported by the displayed values;
- inspect the exported PowerPoint chart, not only a preview image.
