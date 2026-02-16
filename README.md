# 🌍 GuessMyPlace

> An Akinator-style AI place guessing game. Think of any famous place — we'll guess it!

[![Version](https://img.shields.io/badge/version-1.0.0-6c63ff?style=flat-square)](CHANGELOG.md)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

[![Status](https://img.shields.io/badge/status-prototype-f472b6?style=flat-square)]()

---

## ✨ What is GuessMyPlace?

GuessMyPlace is an open-source web game where you think of any famous place in the world — a landmark, city, mountain, island, desert, or natural wonder — and the AI guesses it by asking Yes/No/Maybe questions.

Built as a **zero-dependency, single HTML file** prototype, designed to be extended by the community.

---

## 🎮 How to Play

1. **Think of a place** — any famous location anywhere on Earth
2. **Answer questions** — Yes / Maybe / No to each question
3. **AI guesses!** — Usually under 20 questions

---

## 🚀 Getting Started

### Option 1 — Run Locally

```bash
# Clone the repo
git clone https://github.com/yourusername/guessmyplace.git
cd guessmyplace

# Serve locally (required for data/places.json fetch)
npx serve .
# or
python -m http.server 8080
```

Open `http://localhost:8080`

> ⚠️ **Important:** You must serve the files via a local server (not open `index.html` directly) because the game fetches `data/places.json` via `fetch()`.

### Option 2 — Deploy to Vercel

```bash
npm i -g vercel
vercel
```

That's it! Vercel will detect the static files and deploy instantly.

---

## 📁 Project Structure

```
guessmyplace/
├── index.html          # Main game (HTML + CSS + JS, zero dependencies)
├── data/
│   └── places.json     # All places + questions data
├── CHANGELOG.md        # Version history
└── README.md           # This file
```

---

## 🧠 How the AI Works

The guessing engine uses an **information-gain based question selection** algorithm:

1. **Starts** with all places as candidates
2. **Picks** the question that best splits the remaining candidates (closest to 50/50)
3. **Filters** candidates based on your answer
4. **Early exits** when confidence is high enough (no need to ask all 20 questions)
5. **Scores** remaining candidates by how well they match your answer history

### Data Structure (`places.json`)

Each place has **30+ boolean attributes**:
```json
{
  "name": "Eiffel Tower",
  "country": "France",
  "continent": "Europe",
  "attributes": {
    "isManmade": true,
    "isNatural": false,
    "isInEurope": true,
    "isAncient": false,
    "isModern": true,
    "isTall": true,
    "isBuilding": true,
    ...
  }
}
```

---

## 🌐 Current Place Database (v1.0.0)

| # | Place | Country | Type |
|---|-------|---------|------|
| 1 | Eiffel Tower | France | Landmark |
| 2 | Great Wall of China | China | Landmark |
| 3 | Amazon Rainforest | Brazil | Natural |
| 4 | Mount Everest | Nepal | Natural |
| 5 | Sahara Desert | Africa | Natural |
| 6 | Niagara Falls | USA/Canada | Natural |
| 7 | Colosseum | Italy | Landmark |
| 8 | Maldives | Maldives | Natural |
| 9 | Taj Mahal | India | Landmark |
| 10 | Great Barrier Reef | Australia | Natural |
| 11 | Angkor Wat | Cambodia | Landmark |
| 12 | Venice | Italy | City |
| 13 | Santorini | Greece | Natural |
| 14 | Burj Khalifa | UAE | Landmark |
| 15 | Pyramids of Giza | Egypt | Landmark |
| 16 | Aurora Borealis | Norway/Iceland | Natural |
| 17 | Machu Picchu | Peru | Landmark |
| 18 | Serengeti | Tanzania | Natural |
| 19 | Sydney Opera House | Australia | Landmark |
| 20 | Petra | Jordan | Landmark |

---

## 🛣️ Roadmap

See [CHANGELOG.md](CHANGELOG.md) for the full roadmap.

---

## 🤝 Contributing

We're building this step by step. `CONTRIBUTING.md` is coming soon!

In the meantime:
- 🐛 Open an issue for bugs
- 💡 Open an issue for new place suggestions
- 🔀 PRs welcome — especially for adding new places to `data/places.json`

### Adding a New Place

Simply add an entry to `data/places.json` following the existing format. Make sure to fill in **all 30+ boolean attributes** accurately for the guessing engine to work well.

---

## 📜 License

GPL-v3 © GuessMyPlace Contributors
