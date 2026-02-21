# H2C2 - Humanitarian Health Command Center 🌍

**Hacklytics 2026 - Databricks x UN Geo-Insight Challenge**

A 3D interactive command center for UN officials to identify healthcare funding gaps, benchmark project efficiency, and forecast future humanitarian crises.

## 🎯 Project Overview

The H2C2 platform addresses the "Humanitarian Mismatch" by providing:
- **Interactive 3D Globe**: Visualize global health vulnerability in real-time
- **AI/BI Genie Integration**: Natural language queries for non-technical users
- **ML Benchmarking**: Identify inefficient projects using KNN clustering
- **Forecasting Engine**: Predict future medical deserts using population trends

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Databricks account (for production deployment)

### Installation

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd Hacklytics
```

2. **Create a virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On macOS/Linux
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

### Running the App Locally

```bash
streamlit run src/main.py
```

The app will open automatically in your browser at `http://localhost:8501`

## 🎨 UI Features

The interface replicates the Surveillance Watch design aesthetic:
- **Dark Command Center Theme**: Deep blue/black background with neon accents
- **Left Sidebar**: Filters, controls, and AI assistant
- **Main Dashboard**: Interactive 3D globe with drill-down capabilities
- **Alert Cards**: Critical vulnerabilities and efficiency warnings
- **Real-time Metrics**: Key performance indicators at a glance

## 📊 Data Schema

The app expects data with the following structure:
- `p_code`: Unique geographic identifier
- `location_name`: Region/country name
- `severity_score`: Health crisis severity (1-5)
- `funded_amount`: Total USD allocated
- `beneficiary_count`: People reached
- `vulnerability_index`: Calculated need-to-funding ratio
- `cost_per_beneficiary`: Efficiency metric

## 🛠️ Technical Stack

- **Frontend**: Streamlit + PyDeck
- **Backend**: Databricks (Spark, Delta Lake, Unity Catalog)
- **ML**: Scikit-learn (KNN), Prophet (forecasting)
- **NLP**: Databricks AI/BI Genie
- **Geospatial**: PyDeck Globe View

## 📁 Project Structure

```
Hacklytics/
├── src/
│   └── main.py          # Main Streamlit application
├── requirements.txt      # Python dependencies
├── context.txt          # Project context and architecture
└── README.md            # This file
```

## 🎯 Hackathon Roadmap

### Phase 1: Foundation (Hours 0-6)
- ✅ UI prototype with Surveillance Watch styling
- ⏳ Data ingestion from UN HDX
- ⏳ Databricks workspace setup

### Phase 2: Parallel Development (Hours 6-20)
- ⏳ ML benchmarking engine (Teammate A)
- ⏳ 3D globe interactions (Teammate B)
- ⏳ AI/BI Genie integration

### Phase 3: Integration (Hours 20-30)
- ⏳ Connect Streamlit to Databricks SQL Warehouse
- ⏳ Embed Genie chat interface
- ⏳ End-to-end testing

### Phase 4: Polish & Pitch (Hours 30-36)
- ⏳ Demo recording
- ⏳ Pitch deck
- ⏳ Deployment to Databricks Apps

## 🏆 Key Differentiators

1. **3D Globe with Admin-Level Drill-Down**: Zoom from global to district level
2. **Actionable Insights**: Not just dashboards—specific recommendations
3. **Natural Language Interface**: Non-technical users can query via chat
4. **Predictive Analytics**: Forecast where crises will emerge

## 📝 Notes for Judges

- All data is currently simulated for UI demonstration
- Production version will connect to UN HDX datasets via Databricks
- The KNN benchmarking algorithm is designed to scale to millions of projects
- Forecasting model can be trained on historical HNO/HRP data

## 👥 Team

- Teammate A: Data Engineering & ML
- Teammate B: Full-Stack & UI/UX

## 📄 License

MIT License - Built for Hacklytics 2026

---

**"Not just a dashboard—a recommendation engine that tells UN officials exactly which projects to investigate today."**
