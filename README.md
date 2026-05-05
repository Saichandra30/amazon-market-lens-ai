<![CDATA[<div align="center">

# 📦 Amazon Market Lens AI

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.57-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-LLaMA_3.3_70B-F55036?style=for-the-badge&logo=meta&logoColor=white)
![BeautifulSoup](https://img.shields.io/badge/BeautifulSoup-4-43B02A?style=for-the-badge&logo=python&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-Interactive_Charts-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

**Paste any Amazon Best Sellers URL → get estimated monthly revenue for the market & top 10 products**

*Built for the [Pixii.ai](https://pixii.ai) Founding Engineer take-home project*

---

[Features](#-features) · [How It Works](#-how-it-works) · [Setup](#-local-setup) · [Deploy](#-deploy-to-streamlit-cloud) · [APIs Used](#-apis--tools-used)

</div>

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🔗 **Any Amazon URL** | Paste any Best Sellers URL — supports `amazon.in`, `amazon.com`, and other domains |
| 🕷️ **Smart Scraping** | Extracts top 10 products with price, rating, reviews, and ASIN using BeautifulSoup |
| 📊 **Revenue Estimation** | Estimates monthly units and revenue per product using review velocity heuristics |
| 🏪 **Market Sizing** | Estimates total addressable market using the top-10 = 40% heuristic |
| 📈 **Interactive Charts** | Plotly bar chart showing revenue distribution by rank |
| 🤖 **AI Analysis** | Groq-powered LLaMA 3.3 70B generates a data-driven market research report |
| 💾 **CSV Export** | One-click download of the full analysis as CSV |
| ⚡ **Fast** | End-to-end analysis in under 30 seconds |

---

## 📸 Screenshots

<div align="center">

> 🖼️ *Add screenshots of the app here after deployment*
>
> Recommended: Hero screenshot showing metric cards + data table + chart + AI report

</div>

---

## 🗂️ Project Structure

```
amazon-market-lens-ai/
├── app.py              # 🎯 Streamlit UI — metric cards, table, chart, AI report
├── scraper.py          # 🕷️ BeautifulSoup scraping logic for Amazon Best Sellers
├── estimator.py        # 📊 Revenue estimation engine (review velocity heuristic)
├── analyzer.py         # 🤖 Groq API integration (LLaMA 3.3 70B market report)
├── requirements.txt    # 📦 Python dependencies
├── .env                # 🔑 API keys (not committed)
└── README.md           # 📝 You are here
```

---

## 🧠 How It Works

### Revenue Estimation Methodology

The estimator uses a **review velocity heuristic** — a widely-used e-commerce intelligence technique:

```
Monthly Units = (Reviews × 0.02) × Rank Multiplier × Rating Multiplier
Monthly Revenue = Monthly Units × Price
```

| Factor | Formula | Rationale |
|--------|---------|-----------|
| **Base Units** | `max(review_count × 0.02, 10)` | ~1 review per 50–100 sales is the industry rule of thumb |
| **Rank Multiplier** | `max(1.5 - (rank × 0.08), 0.3)` | Rank #1 sells ~10× more than Rank #10 |
| **Rating Multiplier** | `rating / 5.0` | Higher-rated products convert better |

### Market Sizing

```
Total Market Size = Top 10 Revenue ÷ 0.40
```

> 💡 **Why 40%?** In most Amazon categories, the top 10 best sellers account for approximately 30–50% of total category revenue. We use 40% as a balanced estimate.

### AI Analysis

The enriched product data and market estimates are sent to **Groq's LLaMA 3.3 70B** model, which generates a concise report covering:

1. 📍 Market opportunity summary
2. 📈 Key trends (pricing, ratings, review patterns)
3. 👑 Who's dominating and why
4. 🔍 Whitespace / gaps for new sellers
5. ⚠️ Risk factors

---

## 🚀 Local Setup

### Prerequisites

- Python 3.11+
- A free [Groq API key](https://console.groq.com/)

### Step 1 — Clone the repo

```bash
git clone https://github.com/Saichandra30/amazon-market-lens-ai.git
cd amazon-market-lens-ai
```

### Step 2 — Create virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac / Linux
source venv/bin/activate
```

### Step 3 — Install dependencies

```bash
pip install -r requirements.txt
```

### Step 4 — Set up environment variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
```

### Step 5 — Run the app

```bash
streamlit run app.py
```

The app will open at [http://localhost:8501](http://localhost:8501) 🎉

---

## ☁️ Deploy to Streamlit Cloud

1. Push your code to GitHub (make sure `.env` is in `.gitignore`)
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repo
4. Set the main file path to `app.py`
5. Add your secrets in **Settings → Secrets**:

```toml
GROQ_API_KEY = "your_groq_api_key_here"
```

6. Click **Deploy** 🚀

---

## 🔌 APIs & Tools Used

| Tool | Purpose | Cost |
|------|---------|------|
| **BeautifulSoup + Requests** | Scrapes Amazon Best Sellers pages directly | Free |
| **Groq API** (LLaMA 3.3 70B) | Generates AI-powered market analysis report | Free tier available |
| **Streamlit** | Web UI framework | Free |
| **Plotly** | Interactive bar charts | Free |
| **Pandas** | Data processing & CSV export | Free |

---

## 🧪 Example URLs to Test

Try these Amazon Best Sellers URLs:

| Category | URL |
|----------|-----|
| 🇮🇳 Beauty (India) | `https://www.amazon.in/gp/bestsellers/beauty/` |
| 🇮🇳 Laptops (India) | `https://www.amazon.in/gp/bestsellers/computers/1375424031/` |
| 🇮🇳 Health (India) | `https://www.amazon.in/gp/bestsellers/hpc/` |
| 🇺🇸 Electronics (US) | `https://www.amazon.com/Best-Sellers-Electronics/zgbs/electronics/` |
| 🇺🇸 Books (US) | `https://www.amazon.com/best-sellers-books-Amazon/zgbs/books/` |

---

## 🔮 What I'd Build Next

- [ ] **Multi-category comparison** — analyze 2–3 categories side by side
- [ ] **Historical tracking** — store snapshots and show trends over time
- [ ] **ASIN deep-dive** — click any product to see detailed revenue trajectory
- [ ] **Competitor mapping** — cluster sellers by brand and visualize market share
- [ ] **Automated alerts** — notify when a new product enters the top 10
- [ ] **PDF report export** — one-click downloadable investor-style report
- [ ] **Multi-country support** — auto-detect currency from URL domain
- [ ] **Proxy rotation** — add ScraperAPI integration for high-volume scraping
- [ ] **Confidence intervals** — show estimation ranges instead of point estimates

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 👤 Author

Built with ☕ and 🤖 for the **Pixii.ai Founding Engineer** take-home assessment.

---

<div align="center">

**⭐ Star this repo if you found it useful!**

</div>
]]>
