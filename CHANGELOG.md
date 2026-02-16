# Changelog

All notable changes to **GuessMyPlace** will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.0] - 2025-02-15

### 🎉 Initial Release — Prototype

#### Added
- Core Akinator-style place guessing engine with Yes / No / Maybe answers
- **Intelligent question picker** — selects questions using information-gain scoring to maximize candidate elimination per question
- **Dynamic candidate filtering** — real-time narrowing of the place pool based on attribute matching
- **Early-exit confidence system** — automatically makes a guess when confidence exceeds threshold (85–97%), no need to ask all 20 questions
- **20 iconic places** across all continents: landmarks, natural wonders, cities, islands, deserts, mountains, waterfalls, reefs
- **30 logical questions** covering: continent, type (natural/manmade), climate, category (mountain/beach/desert etc.), UNESCO heritage, and more
- **Answer History panel** — shows every Q&A in reverse order with color-coded badges
- **Confidence meter** — dot-based visual + percentage shown at guess time
- **Wrong guess recovery** — if the user says the guess is wrong, the engine removes that candidate and re-guesses
- **Reveal screen** — when the AI fails, user can type the place name with live autocomplete suggestions
- **Session stats** — tracks Games Played and Games Won in the header
- **Win screen** — shows questions used, confidence, total games, and a key-answers summary
- **Dark mode UI** — fully dark, vibrant gradient design with animated background orbs
- **Fully responsive** — optimized for mobile and desktop
- `data/places.json` — separate data file with 20 places and 30 questions, ready to scale
- Vercel-ready deployment structure (single `index.html` + `data/places.json`)

#### Architecture
- Single `index.html` with embedded CSS and vanilla JS — zero dependencies, zero build step
- External data via `data/places.json` — easy to extend without touching game logic
- Each place has 30+ boolean attributes enabling precise logical deduction
- Each question has a `weight` field for future ML/scoring enhancements

---

## [Unreleased] — Roadmap

### Planned for v1.1.0
- [ ] Add 50+ more places (total 70+)
- [ ] Add more question attributes (is it a river? is it a cave? is it in South America?)
- [ ] Improve confidence algorithm with Bayesian scoring
- [ ] Add `CONTRIBUTING.md` for community contributors
- [ ] Add place images/thumbnails on the win screen

### Planned for v1.2.0
- [ ] Multiple game modes: Easy (landmarks only), Hard (all places)
- [ ] Difficulty selector
- [ ] Share result card (screenshot-style)
- [ ] Multilingual support (Bengali, Spanish, French...)

### Planned for v2.0.0
- [ ] Community place submissions
- [ ] Backend + database for learning from failed guesses
- [ ] 500+ places database
- [ ] Leaderboard system
- [ ] Claude AI API integration for natural language hint generation
