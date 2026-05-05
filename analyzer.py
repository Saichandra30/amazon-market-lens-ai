from groq import Groq
import os
import json
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_market_report(products: list[dict], market_summary: dict) -> str:
    """
    Ask Groq (LLaMA 3.3 70B) to write a smart market analysis report.
    """
    prompt = f"""
You are an Amazon India market research analyst.

IMPORTANT: All prices and revenue figures are in Indian Rupees (₹). 
Always use ₹ symbol, never $ or USD in your report.

Here is data for the Top 10 Best Sellers in a category:
{json.dumps(products, indent=2)}

Estimated Market Summary:
- Top 10 combined monthly revenue: ₹{market_summary['top10_total_revenue']:,.0f}
- Estimated total market size (monthly): ₹{market_summary['estimated_market_size']:,.0f}

Write a concise market analysis report covering:
1. Market opportunity summary (2-3 sentences)
2. Key trends from the top sellers (pricing, ratings, review count)
3. Who is dominating and why
4. Whitespace / gaps a new seller could exploit
5. Risk factors

Keep it under 400 words. Be direct, data-driven, and actionable.
Use ₹ for all currency values.
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role":    "system",
                "content": "You are a sharp Amazon market analyst. Be concise, data-driven, and actionable."
            },
            {
                "role":    "user",
                "content": prompt
            }
        ],
        temperature=0.7,
        max_tokens=1024,
    )

    return response.choices[0].message.content
