# amazon-market-lens-ai

> Paste any Amazon Best Sellers URL and get estimated monthly revenue for the market and top 10 products.

![Python](https://img.shields.io/badge/Python-3.11+-blue?style=flat-square)
![Streamlit](https://img.shields.io/badge/Streamlit-1.57-red?style=flat-square)
![Groq](https://img.shields.io/badge/Groq-LLaMA_3.3_70B-orange?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

---

## Overview

`amazon-market-lens-ai` is a Streamlit web app that scrapes any Amazon Best Sellers page, estimates monthly sales and revenue for the top 10 products using a review velocity heuristic, sizes the total addressable market, and generates an AI-powered market analysis report.

---

## Features

- Scrapes any Amazon Best Sellers URL (`amazon.in`, `amazon.com`, and other domains)
- Extracts title, price, rating, review count, and ASIN for top 10 products
- Estimates monthly units and revenue per product
- Estimates total category market size
- Interactive Plotly bar chart of revenue by rank
- AI market analysis report via Groq (LLaMA 3.3 70B)
- One-click CSV export

---

## Project Structure

```
amazon-market-lens-ai/
├── app.py              # Streamlit UI
├── scraper.py          # BeautifulSoup scraping logic
├── estimator.py        # Revenue estimation engine
├── analyzer.py         # Groq API integration
├── requirements.txt    # Python dependencies
├── .gitignore
├── .env                # API keys — not committed
└── README.md
```

---

## Tech Stack

| Layer       | Tool                          |
|-------------|-------------------------------|
| UI          | Streamlit                     |
| Scraping    | BeautifulSoup4 + Requests     |
| Estimation  | Review velocity heuristic     |
| AI Report   | Groq API — LLaMA 3.3 70B      |
| Charts      | Plotly                        |
| Data        | Pandas                        |

---

## Revenue Estimation Methodology

Uses a **review velocity heuristic** — a standard e-commerce market intelligence technique.

```
Base Units        = max(review_count × 0.02, 10)
Rank Multiplier   = max(1.5 − (rank × 0.08), 0.3)
Rating Multiplier = rating / 5.0

Monthly Units     = Base Units × Rank Multiplier × Rating Multiplier
Monthly Revenue   = Monthly Units × Price
Market Size       = Top 10 Revenue / 0.40
```

**Why 0.40?**
In most Amazon categories, the top 10 best sellers account for ~40% of total category revenue. Dividing by 0.40 scales up to the estimated total addressable market.

---

## Local Setup

**Prerequisites**
- Python 3.11+
- Groq API key — free at [console.groq.com](https://console.groq.com)

**Installation**

```bash
# Clone
git clone https://github.com/Saichandra30/amazon-market-lens-ai.git
cd amazon-market-lens-ai

# Virtual environment
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows

# Install dependencies
pip install -r requirements.txt
```

**Environment variables**

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
```

**Run**

```bash
streamlit run app.py
```

App runs at `http://localhost:8501`

---

## Deployment

### Streamlit Cloud

1. Push repo to GitHub — ensure `.env` is in `.gitignore`
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repo, set main file to `app.py`
4. Add secret under **Settings → Secrets**

```toml
GROQ_API_KEY = "your_groq_api_key_here"
```

5. Click **Deploy**

---

## Test URLs

| Category         | URL                                                                  |
|------------------|----------------------------------------------------------------------|
| Beauty (India)   | `https://www.amazon.in/gp/bestsellers/beauty/`                      |
| Laptops (India)  | `https://www.amazon.in/gp/bestsellers/computers/`                   |
| Health (India)   | `https://www.amazon.in/gp/bestsellers/hpc/`                         |
| Electronics (US) | `https://www.amazon.com/Best-Sellers-Electronics/zgbs/electronics/` |

---

## APIs Used

### 1. BeautifulSoup + Requests
Scrapes Amazon Best Sellers pages directly with no paid API required. Auto-detects Amazon domain from the URL. Uses multiple CSS selector fallbacks to handle Amazon's varying page layouts.

### 2. Groq API — LLaMA 3.3 70B
Sends enriched product data and market estimates to LLaMA 3.3 70B via Groq's inference API. Returns a structured market report covering:
- Market opportunity summary
- Key trends across pricing, ratings, and reviews
- Dominant brands and reasons for their success
- Whitespace gaps for new entrants
- Risk factors

---

## Known Limitations

- Revenue estimates are approximations based on public review data, not actual sales figures
- Amazon occasionally updates page HTML structure which may break CSS selectors
- High-volume scraping without proxy rotation may trigger Amazon rate limits

---

## Roadmap

- [ ] Multi-category side-by-side comparison
- [ ] Historical rank snapshots and trend tracking
- [ ] PDF report export
- [ ] Confidence intervals on revenue estimates
- [ ] ScraperAPI integration for high-volume use
- [ ] Auto-detect currency symbol from URL domain

---

## License

MIT — see [LICENSE](LICENSE)

---

## Author

[Saichandra](https://github.com/Saichandra30)
