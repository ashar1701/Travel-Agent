# 🌍 AI Travel Planning Agent

An intelligent travel planning assistant powered by Tavily search and Google Gemini AI.

## 🚀 Features

- **Flight Search**: Find flight options with prices and times
- **Hotel Search**: Discover accommodations based on your budget
- **Attractions**: Get recommendations for must-visit places
- **Local Cuisine**: Find the best local foods and restaurants
- **Safety Tips**: Learn about travel warnings and cultural etiquette

## 📋 Prerequisites

- Python 3.8+
- Tavily API key ([Get one here](https://tavily.com))
- Google Gemini API key ([Get one here](https://makersuite.google.com/app/apikey))

## 🛠️ Setup

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd travel-agent
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**

Create a `.env` file in the root directory:
```bash
TAVILY_SEARCH_API_KEY=your_tavily_api_key_here
GOOGLE_API_KEY=your_google_api_key_here
```

## 🎯 Usage

### Test Flight Search
```bash
python tools/search_flights.py
```

### Test Agent
```bash
python agents/agent.py
```

## 📁 Project Structure

```
travel-agent/
├── agents/
│   └── agent.py           # Main agent logic
├── tools/
│   └── search_flights.py  # Flight search tool
├── .env                   # API keys (not in git)
├── .gitignore
├── requirements.txt
└── README.md
```

## 🔧 Development Status

🚧 **Currently in development** - Building core agent functionality

## 📝 License

MIT

## 🤝 Contributing

This is a personal project, but feel free to fork and experiment!

