import streamlit as st
import pandas as pd
import plotly.express as px
from scraper import get_bestsellers
from estimator import estimate_monthly_sales, estimate_market
from analyzer import generate_market_report

# ── Page Config ────────────────────────────────────────────
st.set_page_config(
    page_title="Amazon Market Size Estimator",
    page_icon="📦",
    layout="wide"
)

st.title("📦 Amazon Market Size Estimator")
st.caption("Paste any Amazon Best Sellers URL → get estimated monthly revenue for the market & top 10 products.")

# ── Input ──────────────────────────────────────────────────
url = st.text_input(
    "🔗 Amazon Best Sellers URL",
    placeholder="https://www.amazon.com/Best-Sellers-Health-Magnesium/zgbs/...",
)

analyze_btn = st.button("🚀 Analyze Market", type="primary")

# ── Main Logic ─────────────────────────────────────────────
if analyze_btn and url:

    with st.spinner("Scraping Amazon Best Sellers..."):
        try:
            raw_products = get_bestsellers(url)
            if not raw_products:
                st.error("No products found. Check your URL or API key.")
                st.stop()
        except Exception as e:
            st.error(f"Scraping failed — check your ScraperAPI key or URL: {e}")
            st.stop()

    with st.spinner("Estimating revenue..."):
        enriched = []
        for p in raw_products:
            estimates = estimate_monthly_sales(
                review_count = p["review_count"],
                rating       = p["rating"],
                price        = p["price"],
                rank         = p["rank"],
            )
            enriched.append({**p, **estimates})

        market = estimate_market(enriched)

    # ── Market Summary Cards ───────────────────────────────
    st.subheader("📊 Market Summary")
    col1, col2, col3 = st.columns(3)
    col1.metric("Top 10 Monthly Revenue",    f"₹{market['top10_total_revenue']:,.0f}")
    col2.metric("Est. Total Market / Month", f"₹{market['estimated_market_size']:,.0f}")
    col3.metric("Est. Market / Year",        f"₹{market['estimated_market_size']*12:,.0f}")

    st.divider()

    # ── Top 10 Table ──────────────────────────────────────
    st.subheader("🏆 Top 10 Products")
    df = pd.DataFrame(enriched)
    df_display = df[[
        "rank", "title", "price", "rating",
        "review_count", "estimated_monthly_units", "estimated_monthly_revenue"
    ]].rename(columns={
        "rank":                      "Rank",
        "title":                     "Product",
        "price":                     "Price (₹)",
        "rating":                    "Rating",
        "review_count":              "Reviews",
        "estimated_monthly_units":   "Est. Units/Mo",
        "estimated_monthly_revenue": "Est. Revenue/Mo (₹)",
    })

    st.dataframe(df_display, use_container_width=True, hide_index=True)

    # ── Revenue Bar Chart ─────────────────────────────────
    st.subheader("💰 Revenue by Product")
    fig = px.bar(
        df,
        x="rank",
        y="estimated_monthly_revenue",
        hover_name="title",
        labels={
            "rank":                      "Rank",
            "estimated_monthly_revenue": "Est. Monthly Revenue (₹)"
        },
        color="estimated_monthly_revenue",
        color_continuous_scale="Blues",
        text="rank",
    )
    fig.update_traces(textposition="outside")
    fig.update_layout(xaxis=dict(tickmode="linear"))
    st.plotly_chart(fig, use_container_width=True)

    # ── Groq AI Report ────────────────────────────────────
    st.subheader("🤖 AI Market Analysis (Groq · LLaMA 3.3 70B)")
    with st.spinner("Groq is writing your market report..."):
        try:
            report = generate_market_report(enriched, market)
            st.markdown(report)
        except Exception as e:
            st.error(f"AI report failed: {e}")

    # ── Download ──────────────────────────────────────────
    csv = df_display.to_csv(index=False)
    st.download_button(
        label    = "⬇️ Download CSV",
        data     = csv,
        file_name = "market_estimate.csv",
        mime     = "text/csv"
    )

elif analyze_btn and not url:
    st.warning("Please enter an Amazon Best Sellers URL first.")
