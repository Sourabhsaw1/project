import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Set the page configuration
st.set_page_config(
    page_title="Intermediate Streamlit Project",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar configuration
st.sidebar.title("Options")
data_option = st.sidebar.selectbox(
    "Choose a dataset to analyze:",
    ("Random Data", "Upload Your Own")
)

# Dataset selection
if data_option == "Random Data":
    st.sidebar.markdown("**Random Data Parameters**")
    rows = st.sidebar.slider("Number of rows:", 50, 500, 100)
    cols = st.sidebar.slider("Number of columns:", 2, 10, 4)
    random_data = pd.DataFrame(
        np.random.randn(rows, cols),
        columns=[f"Feature {i+1}" for i in range(cols)]
    )
    dataset = random_data
else:
    st.sidebar.markdown("**Upload Your Dataset**")
    uploaded_file = st.sidebar.file_uploader("Upload a CSV file:", type="csv")
    if uploaded_file is not None:
        dataset = pd.read_csv(uploaded_file)
    else:
        st.warning("Please upload a CSV file to proceed.")
        dataset = None

# Main content
st.title("Data Analysis Dashboard")

if dataset is not None:
    st.header("Dataset Overview")
    st.write(dataset.head())

    with st.expander("Show Dataset Summary"):
        st.write(dataset.describe())

    st.header("Interactive Visualizations")

    # Correlation heatmap
    st.subheader("Correlation Heatmap")
    if dataset.shape[1] > 1:
        corr = dataset.corr()
        fig, ax = plt.subplots()
        cax = ax.matshow(corr, cmap="coolwarm")
        fig.colorbar(cax)
        plt.xticks(range(len(corr.columns)), corr.columns, rotation=90)
        plt.yticks(range(len(corr.columns)), corr.columns)
        st.pyplot(fig)
    else:
        st.write("Not enough numeric columns for a correlation heatmap.")

    # Line chart
    st.subheader("Line Chart")
    selected_columns = st.multiselect(
        "Select columns to plot:", options=dataset.columns, default=dataset.columns[:2]
    )
    if selected_columns:
        st.line_chart(dataset[selected_columns])

    # Histogram
    st.subheader("Histogram")
    histogram_column = st.selectbox("Select column for histogram:", dataset.columns)
    bins = st.slider("Number of bins:", 5, 50, 20)
    fig, ax = plt.subplots()
    ax.hist(dataset[histogram_column].dropna(), bins=bins, color="skyblue", edgecolor="black")
    ax.set_title(f"Histogram of {histogram_column}")
    st.pyplot(fig)
else:
    st.info("Please select or upload a dataset to start.")

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("Developed with ❤️ using Streamlit.")
