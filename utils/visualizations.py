import matplotlib.pyplot as plt


# Function to visualize top risks without overlapping names
def plot_overall_risk_gauge(risk_summary):
    """
    Visualizes the top 3 heart disease risks in a bar graph without overlapping risk names.
    """
    # Ensure the data is valid
    if not risk_summary or not isinstance(risk_summary, dict):
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.set_title("No data to display", fontsize=10)
        return plt

    # Sort and limit to top 3 risks for visualization
    sorted_risks = sorted(risk_summary.items(), key=lambda x: x[1], reverse=True)[:3]
    
    # Map long names to shortened names
    risk_mapping = {
        "Potential risk for artery blockage": "Artery blockage",
        "Linked to cholesterol regulation": "Cholesterol",
        "Known mutation affecting heart function": "Heart mutation",
        "Risk linked to high blood pressure": "Blood pressure",
        "Irregular heartbeat risk": "Irregular heartbeat",
    }

    # Shortened names or fallback to the original if not mapped
    risks = [risk_mapping.get(risk, risk) for risk, _ in sorted_risks]
    scores = [score for _, score in sorted_risks]

    # Create the bar graph with better visual spacing
    fig, ax = plt.subplots(figsize=(12, 6))
    bars = ax.bar(risks, scores, color=["red", "orange", "blue"])

    # Set main attributes
    ax.set_ylabel("Risk Score", fontsize=12)
    ax.set_xlabel("Risk Factors", fontsize=12)
    ax.set_title("Top 3 Heart Disease Risk Factors from Genetic Data", fontsize=14)

    # Avoid overlap by ensuring tick properties are spaced well
    ax.tick_params(axis="x", labelsize=10, rotation=30, ha="right")
    ax.tick_params(axis="y", labelsize=10)

    # Annotate bars with their respective scores dynamically
    for bar in bars:
        # Avoid annotations for very small values
        if bar.get_height() > 0.1:
            ax.annotate(
                f"{bar.get_height():.2f}",
                (bar.get_x() + bar.get_width() / 2, bar.get_height()),
                ha="center",
                va="bottom",
                fontsize=10,
                color="black",
            )

    # Improve layout spacing
    fig.tight_layout()

    return plt
