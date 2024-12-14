import pandas as pd


# Load disease markers (Ensure this is accurate)
def load_disease_markers():
    # Example: You can replace this CSV loading logic with actual paths
    file_path = "data/disease_markers.csv"
    try:
        markers_df = pd.read_csv(file_path)
    except FileNotFoundError:
        # Handle missing CSV case gracefully
        markers_df = pd.DataFrame({
            "Marker": ["ATCGT", "GCTAG", "TTAGC", "CCTGA", "AGGCT"],
            "Associated Risk": [0.8, 0.6, 0.7, 0.9, 0.5],
            "Description": [
                "Marker linked to cholesterol regulation",
                "Gene sequence associated with blood pressure",
                "Known mutation affecting heart function",
                "Potential risk for artery blockage",
                "Linked to irregular heartbeat",
            ]
        })
    return markers_df


# Analyze uploaded DNA sequence
def analyze_sequence(sequence, user_threshold):
    """
    Analyzes the uploaded sequence for disease markers.
    Args:
        sequence: Uploaded sequence data as a string.
        user_threshold: User-provided threshold value for risk analysis.
    Returns:
        markers_detected: List of detected markers and their risks.
        risk_summary: Dictionary summarizing analysis.
    """
    markers_df = load_disease_markers()
    markers_detected = []
    total_risk_score = 0

    # Validate sequence to ensure only A, T, C, and G are used
    valid_sequence = all(base in "ATCG" for base in sequence)

    if not valid_sequence:
        # Handle invalid sequence
        return [], {"Detected Markers": 0, "Total Risk Score": 0}

    # Search for known markers in sequence
    for index, row in markers_df.iterrows():
        if row["Marker"] in sequence:
            markers_detected.append({
                "Marker": row["Marker"],
                "Associated Risk": row["Associated Risk"],
                "Description": row["Description"]
            })
            total_risk_score += row["Associated Risk"]

    # Apply the user-defined threshold
    filtered_markers = [marker for marker in markers_detected if marker["Associated Risk"] >= user_threshold]

    risk_summary = {
        "Detected Markers": len(filtered_markers),
        "Total Risk Score": total_risk_score
    }

    return filtered_markers, risk_summary
