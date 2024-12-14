import os
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from utils.nucleotide_analysis import analyze_sequence


# Page configuration
st.set_page_config(
    page_title="Heart Disease DNA Risk Analyzer",
    page_icon="💓",
    layout="wide"
)

# Function to create markers CSV
def create_markers_csv():
    file_path = "data/disease_markers.csv"
    if not os.path.exists("data"):
        os.makedirs("data")
    if not os.path.exists(file_path):
        markers_data = {
            "Marker": ["ATCGT", "GCTAG", "TTAGC", "CCTGA", "AGGCT"],
            "Associated Risk": [0.8, 0.6, 0.7, 0.9, 0.5],
            "Description": [
                "High cholesterol risk",
                "Linked to hypertension",
                "Heart function irregularity",
                "Artery blockage risk",
                "Irregular heartbeat"
            ],
        }
        markers_df = pd.DataFrame(markers_data)
        markers_df.to_csv(file_path, index=False)


# Call the function to ensure the markers CSV exists
create_markers_csv()


# Function to clean and validate DNA sequence
def clean_and_validate_sequence(sequence: str) -> str:
    # Remove headers (lines starting with '>') for FASTA files
    lines = sequence.splitlines()
    cleaned_sequence = "".join([line.strip() for line in lines if not line.startswith(">")])
    
    # Validate the sequence: Ensure it only contains A, T, C, and G
    if not all(base in "ATCG" for base in cleaned_sequence.upper()):
        raise ValueError("Invalid DNA sequence detected! Ensure the sequence contains only A, T, C, and G.")
    
    return cleaned_sequence.upper()


# App title and instructions
st.title("💓 Heart Disease Risk Analysis from DNA Sequences")
st.write("""
    Welcome to the **Heart Disease Risk Analyzer**. This app helps identify genetic markers in DNA sequences that are linked to heart disease risks. Follow the steps below to get started:
    - Upload your DNA sequence file in supported formats (FASTA, TXT, FNA).
    - Adjust the **risk threshold** to filter markers with significant risks.
    - Visualize and interpret the analysis results.
""")

# User guidance icons
st.info("ℹ️ **Tip**: Hover over the 🛈 icons to get more information about each feature.")


# File uploader
uploaded_file = st.file_uploader(
    "📂 Upload a DNA sequence file (in FASTA, TXT, or FNA format)", 
    type=["fasta", "txt", "fna"], 
    key="file_uploader",
    help="Upload your DNA sequence file here. Ensure it's in FASTA, TXT, or FNA format."
)

if uploaded_file:
    try:
        # Read the uploaded file and clean the sequence
        raw_sequence = uploaded_file.read().decode("utf-8").strip()
        cleaned_sequence = clean_and_validate_sequence(raw_sequence)

        # Display the cleaned DNA sequence
        st.subheader("🧬 Validated DNA Sequence")
        st.code(cleaned_sequence, language="plain")
        st.info("ℹ️ The DNA sequence above has been validated and is ready for analysis.")

        # User threshold setting
        st.subheader("🎚️ Adjust Risk Threshold")
        st.write("""
            The **risk threshold** determines the minimum risk score a marker must have to be included in the results. 
            - A higher threshold focuses on markers with stronger associations to risks.
            - A lower threshold includes more markers, even those with moderate risk scores.
        """)
        user_threshold = st.slider(
            "Set the risk threshold (default is 0.5)", 
            min_value=0.0, 
            max_value=1.0, 
            value=0.5, 
            step=0.1, 
            key="threshold_slider",
            help="Adjust the threshold to refine the results based on the associated risk score."
        )

        # Analyze the sequence
        markers_detected, risk_summary = analyze_sequence(cleaned_sequence, user_threshold)

        # Show analysis results
        st.subheader("📊 Analysis Results")
        if markers_detected:
            st.success(f"✅ {len(markers_detected)} marker(s) detected above the threshold.")
            st.write("**Detected Markers and Associated Risks**")
            st.table(pd.DataFrame(markers_detected))

            # Visualization: Top 3 risks
            top_markers = sorted(markers_detected, key=lambda x: x["Associated Risk"], reverse=True)[:3]

            # Bar graph visualization of top 3 risks
            def plot_top_risks(top_markers):
                """
                Visualizes the top 3 detected genetic risk factors for heart disease from uploaded DNA sequence analysis.
                """
                fig, ax = plt.subplots(figsize=(10, 6))  # Set the figure size

                # Truncate long descriptions to ensure clarity
                risks = [
                    m["Description"][:20] + "..." if len(m["Description"]) > 20 else m["Description"] for m in top_markers
                ]
                scores = [m["Associated Risk"] for m in top_markers]

                # Create bar graph
                bars = ax.bar(risks, scores, color=["#FF6F61", "#6B8E23", "#4682B4"])

                # Set graph details
                ax.set_title(
                    "Top 3 Detected Genetic Risk Factors for Heart Disease", fontsize=12
                )
                ax.set_xlabel("Risk Factors", fontsize=10)
                ax.set_ylabel("Risk Score", fontsize=10)
                ax.set_ylim(0, 1.0)

                # Annotate scores
                for bar, score in zip(bars, scores):
                    ax.text(
                        bar.get_x() + bar.get_width() / 2,
                        bar.get_height() - 0.05 if bar.get_height() > 0.1 else bar.get_height() + 0.02,
                        f"{score:.2f}",
                        ha="center",
                        fontsize=8,
                    )

                # Improve layout for visual clarity
                fig.tight_layout()
                return fig

            st.subheader("📉 Top 3 Risk Factors Visualization")
            st.pyplot(plot_top_risks(top_markers))

            # Explain the risks to users
            st.markdown("### 🩺 Explanation of Detected Risks")
            for marker in top_markers:
                st.write(f"**{marker['Description']}**: Detected in your sequence with a risk score of **{marker['Associated Risk']:.2f}**.")
        else:
            st.warning("⚠️ No markers detected above the threshold. Try lowering the threshold for more results.")
    except ValueError as e:
        st.error(f"🚨 {str(e)}")
else:
    st.warning("📥 Please upload a DNA sequence file to begin the analysis.")
