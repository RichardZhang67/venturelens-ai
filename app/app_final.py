import streamlit as st
import pandas as pd
import os

st.title("AI-Powered Startup Opportunity Explorer")
st.write(
    "This dashboard helps teen entrepreneurs explore startup categories, "
    "funding trends, and opportunity recommendations."
)

# Construct the path relative to the script location
script_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(script_dir, "data", "startups_100.csv")
df = pd.read_csv(csv_path)

st.subheader("Startup Dataset")
st.dataframe(df)
st.subheader("Dataset Summary")

num_startups = len(df)
num_industries = df["industry"].nunique()

col1, col2 = st.columns(2)

with col1:
    st.metric("Number of Startups", num_startups)

with col2:
    st.metric("Number of Industries", num_industries)
    st.sidebar.header("Filters")

industry_options = ["All"] + sorted(df["industry"].dropna().unique().tolist())

selected_industry = st.sidebar.selectbox(
    "Select an industry",
    industry_options
)

if selected_industry == "All":
    filtered_df = df
else:
    filtered_df = df[df["industry"] == selected_industry]

st.subheader("Filtered Startup Dataset")
st.dataframe(filtered_df)

df["funding_amount_numeric"] = pd.to_numeric(
    df["funding_amount_usd"],
    errors="coerce"
)

filtered_df = filtered_df.copy()

filtered_df["funding_amount_numeric"] = pd.to_numeric(
    filtered_df["funding_amount_usd"],
    errors="coerce"
)

st.subheader("Funding Summary")

average_funding = filtered_df["funding_amount_numeric"].mean()
median_funding = filtered_df["funding_amount_numeric"].median()
total_funding = filtered_df["funding_amount_numeric"].sum()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Average Funding", f"${average_funding:,.0f}")

with col2:
    st.metric("Median Funding", f"${median_funding:,.0f}")

with col3:
    st.metric("Total Funding", f"${total_funding:,.0f}")

st.caption(
    "Funding calculations use only rows with numeric funding values. "
    "Rows with Unknown funding are ignored in these calculations."
)

industry_counts = df["industry"].value_counts().reset_index()
industry_counts.columns = ["industry", "startup_count"]

st.subheader("Startup Count by Industry")
st.bar_chart(
    industry_counts,
    x="industry",
    y="startup_count"
)

from src.score import calculate_opportunity_score, explain_recommendation
industry_summary = df.groupby("industry").agg(
    startup_count=("startup_name", "count"),
    average_funding=("funding_amount_numeric", "mean"),
    median_funding=("funding_amount_numeric", "median"),
    total_funding=("funding_amount_numeric", "sum")
).reset_index()
score_results = []

for _, row in industry_summary.iterrows():
    result = calculate_opportunity_score(
        category=row["industry"],
        startup_count=row["startup_count"],
        average_funding=row["average_funding"]
    )
    score_results.append(result)

scores_df = pd.DataFrame(score_results)
scores_df = scores_df.sort_values(by="total_score", ascending=False)

scores_df["explanation"] = scores_df.apply(
    lambda row: explain_recommendation(row.to_dict()),
    axis=1
)
st.subheader("Startup Opportunity Ranking")

ranking_display = scores_df[
    ["category", "total_score", "explanation"]
].reset_index(drop=True)

ranking_display.index = ranking_display.index + 1

st.dataframe(ranking_display)
st.caption(
    "The ranking is based on a simple rule-based scoring system. "
    "It is designed for exploration and learning, not as a guaranteed prediction of startup success."
)
with st.expander("How does the scoring method work?"):
    st.write(
        """
        The opportunity score combines data-based factors and human-judgment factors.

        Data-based factors:
        - Number of startups in the category
        - Average funding in the category

        Human-judgment factors:
        - Growth potential
        - Problem importance
        - Teen accessibility
        - Competition level

        The score is useful for comparing categories, but it does not prove which startup idea will succeed.
        """
    )

with st.expander("Project limitations"):
    st.write(
        """
        This project has several limitations:

        1. The dataset includes only 100 startups.
        2. The data was manually collected.
        3. Funding values may be missing or approximate.
        4. Average funding can be affected by large outliers.
        5. The scoring system includes human judgment.
        6. A high score does not guarantee startup success.
        """
    )


# Fun surprise at the end!
with st.expander("Nothing inside"):
    st.markdown(
        "<h1 style='text-align: center; font-size: 150px;'>"
        "🧑🏿‍🦲"
        "</h1>",
        unsafe_allow_html=True
    )
    st.markdown(
        "<h2 style='text-align: center; color: gold;'>"
        "Mr.Nothing" \
        ""
        "</h2>",
        unsafe_allow_html=True
    )

import plotly.express as px

fig = px.bar(
    industry_counts,
    x="industry",
    y="startup_count",
    title="Startup Count by Industry",
    labels={
        "industry": "Industry",
        "startup_count": "Number of Startups"
    }
)

st.plotly_chart(fig, use_container_width=True)

fig = px.bar(
    industry_summary,
    x="industry",
    y="average_funding",
    title="Average Funding by Industry",
    labels={
        "industry": "Industry",
        "average_funding": "Average Funding Amount"
    }
)

st.plotly_chart(fig, use_container_width=True)