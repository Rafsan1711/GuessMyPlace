# 🌍 GuessMyPlace

An intelligent Akinator-style guessing game for Countries, Cities, and Historic Places. Using advanced algorithms and strategic questioning, GuessMyPlace can guess what you're thinking with remarkable accuracy!

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Frontend](https://img.shields.io/badge/Frontend-Vercel-black)](https://vercel.com)
[![Backend](https://img.shields.io/badge/Backend-HuggingFace-yellow)](https://huggingface.co/spaces)

## 🎮 How It Works

1. **Think** of any country, city, or historic place
2. **Answer** strategic yes/no questions
3. **Watch** as GuessMyPlace narrows down possibilities
4. **Be amazed** when it guesses correctly!

## ✨ Features

- 🧠 **Intelligent Algorithm**: C++ powered decision tree with information gain optimization
- 🎯 **High Accuracy**: Advanced probability scoring engine
- 🌐 **Multi-language**: Support for English and Bengali
- 📱 **Responsive**: Works seamlessly on mobile, tablet, and desktop
- 🎨 **Beautiful UI**: Modern design with smooth animations
- 🔄 **Learning System**: Improves from wrong guesses
- 📊 **Statistics**: Track your games and accuracy
- 🌙 **Dark Mode**: Easy on the eyes

## 🚀 Tech Stack

### Frontend
- **React** + **TypeScript** - Type-safe component development
- **Vite** - Lightning-fast build tool
- **Tailwind CSS** - Utility-first styling
- **Framer Motion** - Smooth animations
- **Axios** - API communication

### Backend
- **Python** + **Flask** - RESTful API server
- **C++** - Performance-critical algorithms
- **Firebase Realtime Database** - Data persistence
- **Redis** (Upstash) - High-speed caching
- **Docker** - Containerization

### DevOps
- **GitHub Actions** - CI/CD pipeline
- **Vercel** - Frontend hosting
- **Hugging Face Spaces** - Backend hosting (Docker)
- **Jest/Pytest** - Testing frameworks

## 📦 Repository Structure

```
GuessMyPlace/
├── frontend/          # React + TypeScript frontend
├── backend/           # Flask API + C++ algorithms
├── data/              # Place data & questions (JSON)
├── docs/              # Documentation
├── scripts/           # Automation scripts
└── .github/           # CI/CD workflows
```

## 🛠️ Quick Start

### Prerequisites
- **Node.js** 18+ 
- **Python** 3.10+
- **Docker** & Docker Compose
- **Git**

### Local Development

1. **Clone the repository**
```bash
git clone https://github.com/Rafsan1711/GuessMyPlace.git
cd GuessMyPlace
```

2. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env with your Firebase and Redis credentials
```

3. **Run with Docker Compose**
```bash
docker-compose up
```

4. **Access the application**
- Frontend: http://localhost:5173
- Backend API: http://localhost:5000
- API Docs: http://localhost:5000/docs

### Manual Setup

#### Frontend
```bash
cd frontend
npm install
npm run dev
```

#### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python run.py
```

## 📖 Documentation

- [Architecture Overview](docs/ARCHITECTURE.md)
- [API Documentation](docs/API.md)
- [Contributing Guide](docs/CONTRIBUTING.md)
- [Data Format Specification](docs/DATA_FORMAT.md)

## 🎯 Project Status

### Current Phase: Milestone 1 - Foundation Setup
- [x] Repository structure
- [x] Documentation templates
- [ ] Development environment
- [ ] CI/CD pipeline

See [ROADMAP.md](ROADMAP.md) for complete development plan.

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Add Places**: Expand our database with new countries, cities, or historic places
2. **Improve Algorithms**: Optimize question selection logic
3. **Enhance UI**: Make the interface more beautiful and accessible
4. **Fix Bugs**: Help us squash those pesky bugs
5. **Write Tests**: Improve code coverage

Please read [CONTRIBUTING.md](docs/CONTRIBUTING.md) for details on our code of conduct and development process.

## 📊 Current Statistics

- **Places**: 200+ (Countries, Cities, Historic Places)
- **Questions**: 200+ strategic questions
- **Accuracy**: Target 80%+
- **Response Time**: <500ms average

## 🗺️ Roadmap Highlights

- [x] ✅ Project setup and infrastructure
- [ ] 🔄 Core algorithm implementation (C++ + Python)
- [ ] 🔄 REST API development
- [ ] 🔄 Frontend UI/UX
- [ ] 📋 Machine learning integration
- [ ] 📋 Mobile app (React Native)
- [ ] 📋 Multiplayer mode

## 🐛 Known Issues

No critical issues at the moment. Check [Issues](https://github.com/Rafsan1711/GuessMyPlace/issues) for current bugs and feature requests.

## 📝 License

This project is licensed under the **GNU General Public License v3.0** - see the [LICENSE](LICENSE) file for details.

## 👏 Acknowledgments

- Built with ❤️ for geography and history enthusiasts
- Thanks to all contributors!

## 📧 Contact

- **Project Lead**: Your Name
- **Email**: your.email@example.com
- **Issues**: [GitHub Issues](https://github.com/Rafsan1711/GuessMyPlace/issues)
- **Discussions**: [GitHub Discussions](https://github.com/Rafsan1711/GuessMyPlace/discussions)

## 🌟 Star History

If you find this project useful, please consider giving it a star ⭐!

---

**Made with 🧠 and ☕ | Open Source | GPL v3**