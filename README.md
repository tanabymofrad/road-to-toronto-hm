# Road to the Toronto Waterfront Half

Tanaby's training dashboard for the TCS Toronto Waterfront Half, October 18, 2026: every run from W1D1 on May 4 to the start line, with the race-day countdown, weekly distance, pace zones, long-run pace and training load.

**Live app:** https://tanabymofrad.github.io/road-to-toronto-hm/

On a phone, open the link and choose **Add to Home Screen** (Safari: Share menu; Chrome: ⋮ menu) to install it like an app.

## How it stays up to date

A scheduled Claude task runs every morning a little before 10 am Toronto time. It pulls any new runs from Strava, adds them to the `RUNS` data in `index.html`, and commits the change here, so the live site updates within a minute or two. The countdown is calculated in the browser, so it's always current.

## Files

- `index.html` – the dashboard (single page, Chart.js from cdnjs)
- `manifest.webmanifest`, `sw.js`, `icons/` – make it installable and readable offline
