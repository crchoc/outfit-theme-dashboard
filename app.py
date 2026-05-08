import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


st.set_page_config(
    page_title="Outfit Theme Analysis Dashboard",
    page_icon="👗",
    layout="wide"
)


REQUIRED_COLUMNS = [
    "outfit_id",
    "theme",
    "top_category",
    "bottom_category",
    "shoe_category",
    "accessory_category",
    "num_items"
]


@st.cache_data
def load_sample_data():
    return pd.read_csv("data/sample_outfits.csv")


def validate_data(df):
    missing_columns = [col for col in REQUIRED_COLUMNS if col not in df.columns]

    if missing_columns:
        return False, missing_columns

    return True, []


def load_uploaded_data(uploaded_file):
    try:
        df = pd.read_csv(uploaded_file)
        is_valid, missing_columns = validate_data(df)

        if not is_valid:
            return None, missing_columns, "missing_columns"

        return df, [], None

    except Exception:
        return None, [], "read_error"


def clean_data(df):
    df = df.copy()

    df["theme"] = df["theme"].astype(str)
    df["outfit_id"] = df["outfit_id"].astype(str)

    df["num_items"] = pd.to_numeric(df["num_items"], errors="coerce")
    df = df.dropna(subset=["num_items"])
    df["num_items"] = df["num_items"].astype(int)

    return df


st.title("Outfit Theme Analysis Dashboard")
st.write(
    "An interactive dashboard for exploring outfit themes, fashion categories, and dataset statistics."
)


st.sidebar.header("Data Source")

uploaded_file = st.sidebar.file_uploader(
    "Upload your outfit CSV file",
    type=["csv"]
)

if uploaded_file is not None:
    uploaded_df, missing_columns, error_type = load_uploaded_data(uploaded_file)

    if error_type == "missing_columns":
        st.error("The uploaded CSV file is missing required columns.")
        st.write("Missing columns:")
        st.write(missing_columns)

        st.info("The dashboard is currently using the sample dataset instead.")
        df = load_sample_data()

    elif error_type == "read_error":
        st.error("The uploaded file could not be read. Please upload a valid CSV file.")
        st.info("The dashboard is currently using the sample dataset instead.")
        df = load_sample_data()

    else:
        df = uploaded_df
        st.sidebar.success("Uploaded CSV loaded successfully.")

else:
    df = load_sample_data()
    st.sidebar.info("Using sample dataset.")


df = clean_data(df)


st.sidebar.header("Filters")

theme_options = ["All"] + sorted(df["theme"].unique().tolist())
selected_theme = st.sidebar.selectbox("Select theme", theme_options)

min_items = int(df["num_items"].min())
max_items = int(df["num_items"].max())

selected_item_range = st.sidebar.slider(
    "Number of items per outfit",
    min_value=min_items,
    max_value=max_items,
    value=(min_items, max_items)
)


filtered_df = df.copy()

if selected_theme != "All":
    filtered_df = filtered_df[filtered_df["theme"] == selected_theme]

filtered_df = filtered_df[
    (filtered_df["num_items"] >= selected_item_range[0]) &
    (filtered_df["num_items"] <= selected_item_range[1])
]


st.subheader("Dataset Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Outfits", len(filtered_df))

with col2:
    st.metric("Number of Themes", filtered_df["theme"].nunique())

with col3:
    if len(filtered_df) > 0:
        st.metric("Average Items", round(filtered_df["num_items"].mean(), 2))
    else:
        st.metric("Average Items", 0)

with col4:
    st.metric("Original Dataset Size", len(df))


if len(filtered_df) == 0:
    st.warning("No outfits match the selected filters.")
    st.stop()


st.subheader("Theme Distribution")

theme_counts = filtered_df["theme"].value_counts()

fig, ax = plt.subplots()
ax.bar(theme_counts.index, theme_counts.values)
ax.set_xlabel("Theme")
ax.set_ylabel("Number of Outfits")
ax.set_title("Number of Outfits by Theme")
plt.xticks(rotation=30)

st.pyplot(fig)


st.subheader("Category Summary")

category_columns = [
    "top_category",
    "bottom_category",
    "shoe_category",
    "accessory_category"
]

selected_category_column = st.selectbox(
    "Choose category type",
    category_columns
)

category_counts = (
    filtered_df[selected_category_column]
    .replace("None", pd.NA)
    .dropna()
    .value_counts()
    .reset_index()
)

category_counts.columns = ["Category", "Count"]

st.dataframe(category_counts, use_container_width=True)


st.subheader("Theme-Level Summary")

theme_summary = (
    filtered_df
    .groupby("theme")
    .agg(
        total_outfits=("outfit_id", "count"),
        average_items=("num_items", "mean")
    )
    .reset_index()
)

theme_summary["average_items"] = theme_summary["average_items"].round(2)

st.dataframe(theme_summary, use_container_width=True)


st.subheader("Outfit Data")

st.dataframe(filtered_df, use_container_width=True)


st.subheader("Required CSV Format")

st.write(
    "To upload your own data, the CSV file should contain the following columns:"
)

st.code(
    "outfit_id, theme, top_category, bottom_category, shoe_category, accessory_category, num_items"
)


st.subheader("Project Purpose")

st.write(
    """
    This dashboard is designed as a portfolio project based on outfit recommendation research.
    Version 2 adds CSV upload, basic data validation, and improved filtering.
    
    Future versions can include model result visualization, FITB analysis,
    category grouping comparison, and research-style performance dashboards.
    """
)