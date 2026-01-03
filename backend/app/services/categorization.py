from typing import Tuple

# Rule-based keyword map (EXTENSIBLE)
CATEGORY_RULES = {
    "FOOD": ["swiggy", "zomato", "restaurant", "food", "pizza", "burger"],
    "SHOPPING": ["amazon", "flipkart", "myntra", "shopping"],
    "TRAVEL": ["uber", "ola", "flight", "train", "bus"],
    "BILLS": ["electricity", "recharge", "bill", "wifi", "internet"],
    "ENTERTAINMENT": ["netflix", "spotify", "movie"],
}


def categorize_transaction(description: str) -> Tuple[str, float, str]:
    """
    Categorize transaction description using rule-based logic.
    Returns:
        category (str)
        confidence (float)
        method (str)
    """

    description_lower = description.lower()

    for category, keywords in CATEGORY_RULES.items():
        matches = sum(1 for keyword in keywords if keyword in description_lower)

        if matches > 0:
            confidence = min(0.5 + (matches * 0.1), 0.95)
            return category, round(confidence, 2), "rule-based"

    return "OTHER", 0.4, "rule-based"
