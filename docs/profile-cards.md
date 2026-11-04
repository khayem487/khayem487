# About the profile cards

The cards combine public GitHub activity with reviewed project highlights.

| Label | What it counts |
| --- | --- |
| Commits · last year | The public commit statistic returned by the pinned GitHub Stats Extended renderer. |
| Stars earned | Stars on public repositories, as returned by that renderer. |
| Public repos | Repositories owned by `khayem487`, visible publicly and not marked as forks. This includes the portfolio and profile repositories; it is not a count of separate applications. |
| Live demos | Ten distinct interactive web demonstrations in the reviewed inventory. The portfolio, presentation pages, CROUS, fan control and browser extensions are excluded. |
| Hackathon IA · 2nd | The ASL team's second-place result at Hackathon IA, already described in this profile's project and hackathon sections. |

The language card reports the relative code size of the selected public-repository languages. Its design is preserved independently of the activity-card highlights.

## Demo inventory

The demo entrypoints below returned HTTP 200 without authentication on **4 November 2026**. This check confirms their entrypoint availability on that date; it does not claim continuous uptime or a fresh complete test of every workflow.

- [OneTech document workshop](https://khayem-onetech.vercel.app/) — actual native PDF/DOCX extraction and manual qualification; the complete AI/OCR pipeline remains separate.
- [ASL Recognition](https://khayem-asl.vercel.app/) — camera-based sign classification.
- [Purchasing dashboard](https://khayem-data-dashboard.vercel.app/) — interactive purchasing-data analysis.
- [Facial attendance](https://khayem-facial-attendance.vercel.app/) — isolated browser demo with the documented cloud recognition mode.
- [Smart Home](https://khayem-smart-home.vercel.app/) — home controls and persistent state.
- [Loc Auto](https://khayem-car-rental.vercel.app/) — authentication and vehicle reservations.
- [HealthRadar](https://khayem-healthradar.vercel.app/) — a web adaptation of the team simulation project using its Java engine.
- [Watch Party](https://khayem-watch-party.vercel.app/) — synchronized viewing application.
- [Exchange Matcher](https://khayem-exchange-matcher.vercel.app/) — the matching application published under the acknowledged pseudonym.
- [OOP Game](https://khayem-oop-game.vercel.app/) — browser campaign using the shared Java game engine.

## Updating the cards

The daily GitHub workflow refreshes commits, stars, languages and the owned public-repository inventory. It uses GitHub's public user-repository endpoint; it does not enumerate private repositories.

The demo inventory in [`assets/profile/highlights.json`](../assets/profile/highlights.json) is curated. Add or remove a demo there after reviewing it, then update `demos_verified_on`. The scheduled workflow does not ping the demo servers or try to keep them awake.

The pinned renderer supplies the GitHub figures. `scripts/style_profile_cards.py` preserves those values and derives the two inventory counts. If fetching or validation fails, the workflow does not replace the last successful cards.

Local refresh:

```text
python scripts/refresh_profile_highlights.py
python scripts/style_profile_cards.py
```
