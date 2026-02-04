def generate_summary_explanation(
    health_score: int,
    monthly_spend: float,
    top_category: str,
    risk_alerts: list,
):
    explanations = []

    # Health
    if health_score >= 80:
        explanations.append("Your financial health is strong with disciplined spending.")
    elif health_score >= 60:
        explanations.append("Your financial health is stable but has room for improvement.")
    else:
        explanations.append("Your financial health is weak due to high or inconsistent spending.")

    # Spending level
    if monthly_spend > 20000:
        explanations.append("Your monthly spending is relatively high compared to healthy limits.")
    else:
        explanations.append("Your monthly spending is under control.")

    # Category focus
    if top_category:
        explanations.append(f"The majority of your spending is in {top_category} category.")

    # Risk presence
    if risk_alerts:
        explanations.append("Some financial risk patterns were detected this month.")
    else:
        explanations.append("No significant financial risks detected.")

    return explanations
