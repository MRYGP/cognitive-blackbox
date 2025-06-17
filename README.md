# 🧠 Cognitive Black Box

**An AI-powered cognitive upgrade experience that exposes decision-making blind spots through immersive historical case studies**

## 📋 Project Overview

**Project Name**: Cognitive Black Box  
**Project Type**: AI-driven cognitive upgrade product  
**Target Users**: Senior decision-makers such as entrepreneurs, business leaders, and government officials who have experienced major decision failures  
**Core Value**: Through 18-minute shocking historical case experiences, users deeply recognize cognitive blind spots and obtain actionable decision-making frameworks  
**Current Stage**: MVP Development Phase  

## 🎯 Key Features

- **🎭 Four-Role AI Experience**: Host → Investor → Mentor → Assistant
- **⚡ Magic Moments**: Cognitive shock through sudden perspective shifts
- **🎯 Personalization Engine**: Adaptive content based on user background
- **🛠️ Decision Tools**: Generate customized decision safety systems
- **📊 Three Premium Cases**: Madoff, LTCM, Lehman Brothers

## 🏗️ Technical Architecture

### Core Components

```
cognitive-blackbox/
├── app.py                    # Streamlit main application entry
├── utils/
│   ├── session_manager.py    # Session state management
│   ├── ai_roles.py          # AI role engine (4 characters)
│   ├── data_models.py       # Data structure definitions
│   ├── config.py            # Application configuration
│   └── constants.py         # Constants definition
├── tests/
│   └── conftest.py          # Test configuration
├── requirements.txt         # Dependencies
├── .env.example            # Environment variables template
├── .gitignore              # Git ignore rules
└── README.md               # This file
```

### Technology Stack

- **Frontend**: Streamlit (Python web framework)
- **AI Engine**: Gemini 2.0 Flash / Claude Sonnet
- **State Management**: Custom session manager
- **Deployment**: Streamlit Community Cloud + GitHub
- **Development**: Python 3.9+

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- Git
- API keys for Gemini and/or Claude

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/cognitive-blackbox.git
   cd cognitive-blackbox
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env file with your API keys
   ```

5. **Run the application**
   ```bash
   streamlit run app.py
   ```

### Environment Variables

Create a `.env` file in the project root:

```env
# AI API Keys
GEMINI_API_KEY=your_gemini_api_key_here
ANTHROPIC_API_KEY=your_claude_api_key_here

# Application Settings
DEBUG_MODE=true
CACHE_ENABLED=true
DEFAULT_CASE=madoff
```

## 🎮 How It Works

### The 18-Minute Experience

1. **🎭 Act 1 - Decision Immersion (Host)**
   - Collect user background information
   - Build case immersion and identification
   - Set up decision context

2. **🔥 Act 2 - Reality Disruption (Investor)**
   - Use shocking data to shatter cognitive assumptions
   - Create strong cognitive dissonance
   - **Magic Moment**: Sudden perspective shift

3. **🧠 Act 3 - Framework Reconstruction (Mentor)**
   - Provide authoritative theoretical explanations
   - Build systematic cognitive frameworks
   - Transform shock into profound insights

4. **🎯 Act 4 - Capability Armament (Assistant)**
   - Design personalized decision safety systems
   - Provide specific application guidance
   - Generate actionable tools

### Supported Cases

| Case | Cognitive Bias | Description |
|------|---------------|-------------|
| **Madoff** | Halo Effect | The fatal halo of former NASDAQ chairman |
| **LTCM** | Overconfidence | The downfall of the Nobel Prize winning team |
| **Lehman** | Confirmation Bias | The obsession that housing prices will never fall |

## 🎨 UI/UX Design Status

**Current Status**: Architecture framework completed, awaiting STUDIO design specifications

**Planned Features**:
- Role-specific visual themes (blue/red/green/cyan)
- Smooth transitions between acts
- Magic moment visual effects
- Responsive design for desktop/mobile
- Progress indicators and engagement metrics

## 🔧 Development Status

### ✅ Completed Components

- [x] **Core Architecture**: Session management, AI roles, data models
- [x] **English Localization**: All code comments and documentation
- [x] **API Integration**: Gemini 2.0 Flash and Claude Sonnet support
- [x] **Basic UI Framework**: Streamlit application structure
- [x] **Configuration System**: Environment management and constants
- [x] **Testing Framework**: Basic test structure

### 🔄 In Progress

- [ ] **UI Implementation**: Awaiting STUDIO design specifications
- [ ] **Content Integration**: Case scripts and AI prompts
- [ ] **Magic Moments**: Visual effect implementations
- [ ] **Performance Optimization**: Caching and response times

### ⏳ Planned

- [ ] **User Testing**: Internal and external validation
- [ ] **Analytics Integration**: User behavior tracking
- [ ] **Advanced Personalization**: ML-driven adaptations
- [ ] **Multi-language Support**: Chinese/English versions

## 🚀 Deployment

### Streamlit Community Cloud

1. **Push to GitHub**: Ensure all files are committed
2. **Connect to Streamlit**: Link your GitHub repository
3. **Configure Environment**: Add API keys in Streamlit secrets
4. **Deploy**: Automatic deployment on every push

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export GEMINI_API_KEY="your_key_here"
export ANTHROPIC_API_KEY="your_key_here"

# Run application
streamlit run app.py
```

## 📊 Performance Metrics

**Target Performance**:
- Initial load time: < 3 seconds
- AI response time: < 2 seconds per turn
- Complete experience: 18 minutes ± 2 minutes
- User engagement: > 85% completion rate

## 🤝 Team & Collaboration

### Core Team

- **👑 Human Founder**: Strategic decisions, content control, resource coordination, final validation
- **🤖 Claude (C)**: Engineering execution, technical implementation, product delivery, progress management  
- **🎨 STUDIO (S)**: Experience design, user journey, business optimization

### Development Principles

- **User Value First**: Every decision answers "What value does this provide to users?"
- **Progressive Validation**: From hypothesis to verification, step-by-step uncertainty reduction
- **Magic Moment Driven**: Create surprises while solving problems
- **Simple yet Profound**: Solve complex problems with simple methods
- **Executable Landing**: All recommendations must be actionable

## 📝 Contributing

### Development Workflow

1. **Fork the repository**
2. **Create feature branch**: `git checkout -b feature/amazing-feature`
3. **Commit changes**: `git commit -m 'Add amazing feature'`
4. **Push to branch**: `git push origin feature/amazing-feature`
5. **Open Pull Request**

### Code Standards

- **English Only**: All code comments, documentation, and variable names in English
- **Type Hints**: Use Python type hints throughout
- **Docstrings**: Document all classes and methods
- **Testing**: Write tests for new features
- **Formatting**: Follow PEP 8 standards

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 Links

- **Live Demo**: [Coming Soon]
- **Documentation**: [Project Wiki]
- **Issues**: [GitHub Issues](https://github.com/your-username/cognitive-blackbox/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-username/cognitive-blackbox/discussions)

## 📞 Contact

For questions, suggestions, or collaboration opportunities:

- **GitHub Issues**: For technical problems and feature requests
- **Email**: [Your contact email]
- **LinkedIn**: [Your LinkedIn profile]

---

**Built with ❤️ using Streamlit, Python, and AI**

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-app-url.streamlit.app)

---

*"Users don't want a faster horse, they want the peace of mind that comes with reaching their destination." - Project Philosophy*
