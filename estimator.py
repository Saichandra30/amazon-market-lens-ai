def estimate_monthly_sales(
    review_count: float,
    rating: float,
    price: float,
    rank: int
) -> dict:
    """
    Estimate monthly unit sales using review velocity heuristic.
    Rule of thumb: ~1 review per 50-100 sales.
    Adjust by rank and rating.
    """
    # Base estimate
    base_units = max(review_count * 0.02, 10)

    # Rank multiplier: rank 1 sells ~10x more than rank 10
    rank_multiplier = max(1.5 - (rank * 0.08), 0.3)

    # Rating quality multiplier
    rating_multiplier = (rating / 5.0) if rating > 0 else 0.6

    monthly_units   = base_units * rank_multiplier * rating_multiplier
    monthly_revenue = monthly_units * price

    return {
        "estimated_monthly_units":   round(monthly_units),
        "estimated_monthly_revenue": round(monthly_revenue, 2),
    }


def estimate_market(products: list[dict]) -> dict:
    """
    Estimate total market size from top 10 products.
    Assumes top 10 = ~40% of total market (common heuristic).
    """
    total_top10_revenue  = sum(p["estimated_monthly_revenue"] for p in products)
    total_market_estimate = total_top10_revenue / 0.40

    return {
        "top10_total_revenue":    round(total_top10_revenue, 2),
        "estimated_market_size":  round(total_market_estimate, 2),
    }
