from typing import Tuple
import re

CATEGORY_RULES = {
    "FOOD": ["swiggy", "zomato", "restaurant", "food", "pizza", "burger"],
    "SHOPPING": ["amazon", "flipkart", "myntra", "shopping"],
    "TRAVEL": ["uber", "ola", "flight", "train", "bus"],
    "BILLS": ["electricity", "recharge", "bill", "wifi", "internet"],
    "ENTERTAINMENT": ["netflix", "spotify", "movie"],
}


def clean_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def categorize_transaction(description: str) -> Tuple[str, float, str]:
    if not description:
        return "OTHER", 0.2, "rule-based"

    description = clean_text(description)

    best_match = ("OTHER", 0.2)

    for category, keywords in CATEGORY_RULES.items():
        matches = sum(1 for k in keywords if k in description)
        if matches > 0:
            confidence = min(0.5 + matches * 0.12, 0.95)
            if confidence > best_match[1]:
                best_match = (category, confidence)

    return best_match[0], round(best_match[1], 2), "rule-based"
