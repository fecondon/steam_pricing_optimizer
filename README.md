# 🎮 Steam Pricing Optimizer
A full-stack machine learning project that scrapes, models, and simulates pricing strategies for Steam games. Built to estimate the causal impact of additional discounting on conversion rates, optimize price points, and display results in a dynamic Streamlit dashboard.

---

## 🎬 Features
- ✅ Web scraper from Steam website
- ✅ Simulated conversion probabilities based on discount and new-release status
- ✅ Gradient Boosting classification model for conversion prediction\
- ✅ Price optimization via maximizing expected revenue
- ✅ A/B test simulator (+5% discount treatment)
- ✅ Causal uplift modeling with UpliftTreeClassifier
- ✅ Gain and Qini curve visualization
- ✅ Streamlit dashboard with dynamic filtering and insights

---

## 🗂️ Project Structure
```
steam-pricing-optimizer/
├── app/                   # Streamlit dashboard app
├── data/                  # Raw and processed CSV files
├── notebooks/             # Exploratory analysis notebooks
├── scripts/               # Scraping, simulation, and modeling scripts
├── .github/workflows/     # CI/CD workflows (optional)
├── requirements.txt       # Python dependencies
├── README.md              # This file
└── .gitignore
```

---

## 📊 Dashboard Preview
Launch the dashboard locally
```bash
streamlit run app/steamlit.py
```

---

## 🔬 How it works
### 🎯 Conversion Simulation
- Uses `discount_percent` and `is_new_release` to simulate conversion probability

### 📈 Price Optimization
- Tests multiple price points per game to find the maximum price

### 🧬 Causal Inference
- Simulates an A/B test: original discount (control) vs additional 5% (treatment)
- Estimatese the uplift with a decision tree based causal model

### 🖥️ Streamlit App
- Filters by discount, uplift and pricing
- Interactive visualizations (Gain/Qini curves)
- Hosted locally, deployable via Streamlit Cloud

---

## 🛠️ Tech Stack
- **Languages:** Python, Bash
- **Libraries:** pandas, numpy, scikit-learn, causalml, matplotlib, Streamlit
- **Tools:** GitHub, Streamlit, GitHub Actions (CI/CD)

---

## 📦 Install & Run
```bash
pip install -r requirements.txt
streamlit run app/steamlit.py
```

---

## 🔮 Future Enhancements
- Dynamic model retraining in Streamlit based on filters
- Deploy to Streamlit Cloud via GitHub Actions
- Targeting engine for uplift segments
- Revenue vs. Price trade-off exploration

---

## ✍️ Author
**Nick Fecondo** - [GitHub](https://github.com/fecondon) | [LinkedIn](https://linkedin.com/in/nickfecondo)

---

## 🪪 License
MIT - feel free to use, modify, and ⭐️