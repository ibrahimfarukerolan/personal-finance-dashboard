
import streamlit as st
import pandas as pd
import plotly.express as px

# =====================================
# PAGE CONFIGURATION
# =====================================

st.set_page_config(
    page_title="FinSight | Personal Finance",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================
# CUSTOM STYLING
# =====================================

st.markdown("""
<style>
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1450px;
}

h1, h2, h3 {
    letter-spacing: -0.5px;
}

div[data-testid="stMetric"] {
    background: #172235;
    border: 1px solid #2A3A50;
    padding: 20px;
    border-radius: 14px;
}

div[data-testid="stMetricLabel"] {
    color: #94A3B8;
}

div[data-testid="stMetricValue"] {
    color: #F1F5F9;
}

section[data-testid="stSidebar"] {
    border-right: 1px solid #263449;
}

.stButton > button,
.stDownloadButton > button {
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# =====================================
# HEADER
# =====================================

st.title("💰 FinSight")
st.caption("PERSONAL FINANCE ANALYTICS")

st.write(
    "Understand your spending, track your savings, "
    "and make smarter financial decisions."
)

st.divider()

# =====================================
# SIDEBAR
# =====================================

st.sidebar.title("FinSight")
st.sidebar.caption("Your personal finance workspace")
st.sidebar.divider()

uploaded_file = st.sidebar.file_uploader(
    "Upload Transactions",
    type=["csv"]
)

st.sidebar.caption(
    "Required CSV columns: Date, Category, Amount. "
    "Positive amounts = income, negative amounts = expenses."
)

# =====================================
# SAMPLE DATA
# =====================================

sample_data = {
    "Date": [
        "2026-08-01",
        "2026-08-02",
        "2026-08-04",
        "2026-09-01",
        "2026-09-03",
        "2026-09-05",
        "2026-10-01",
        "2026-10-03",
        "2026-10-06"
    ],
    "Category": [
        "Salary",
        "Rent",
        "Groceries",
        "Salary",
        "Rent",
        "Shopping",
        "Salary",
        "Rent",
        "Transport"
    ],
    "Amount": [
        5000,
        -1800,
        -450,
        5000,
        -1800,
        -350,
        5200,
        -1800,
        -180
    ]
}

# =====================================
# LOAD DATA
# =====================================

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        st.sidebar.success("CSV loaded successfully!")
    except Exception as error:
        st.error(f"Unable to read CSV: {error}")
        st.stop()
else:
    df = pd.DataFrame(sample_data)
    st.info(
        "Demo mode: Upload a CSV file "
        "to analyze your own transactions."
    )

# =====================================
# DATA VALIDATION
# =====================================

required_columns = {"Date", "Category", "Amount"}

if not required_columns.issubset(df.columns):
    st.error(
        "CSV must contain Date, Category, and Amount columns."
    )
    st.stop()

df["Date"] = pd.to_datetime(
    df["Date"],
    errors="coerce"
)

df["Amount"] = pd.to_numeric(
    df["Amount"],
    errors="coerce"
)

df["Category"] = (
    df["Category"]
    .astype("string")
    .str.strip()
)

invalid_rows = (
    df["Date"].isna()
    | df["Amount"].isna()
    | df["Category"].isna()
    | (df["Category"] == "")
)

if invalid_rows.any():
    st.error(
        f"Found {invalid_rows.sum()} invalid transaction(s). "
        "Please correct your CSV file."
    )
    st.stop()

if df.empty:
    st.warning("No transactions available.")
    st.stop()

# =====================================
# INTERACTIVE FILTERS
# =====================================

st.sidebar.divider()
st.sidebar.subheader("🔎 Filters")

min_date = df["Date"].min().date()
max_date = df["Date"].max().date()

date_range = st.sidebar.date_input(
    "Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

categories = sorted(
    df["Category"].unique().tolist()
)

selected_categories = st.sidebar.multiselect(
    "Categories",
    options=categories,
    default=categories
)

transaction_type = st.sidebar.selectbox(
    "Transaction Type",
    ["All", "Income", "Expenses"]
)

filtered_df = df.copy()

if len(date_range) == 2:
    start_date, end_date = date_range

    filtered_df = filtered_df[
        (filtered_df["Date"].dt.date >= start_date)
        & (filtered_df["Date"].dt.date <= end_date)
    ]

filtered_df = filtered_df[
    filtered_df["Category"].isin(selected_categories)
]

if transaction_type == "Income":
    filtered_df = filtered_df[
        filtered_df["Amount"] > 0
    ]

elif transaction_type == "Expenses":
    filtered_df = filtered_df[
        filtered_df["Amount"] < 0
    ]

if filtered_df.empty:
    st.warning(
        "No transactions match the selected filters."
    )
    st.stop()

# =====================================
# FINANCIAL CALCULATIONS
# =====================================

income = filtered_df.loc[
    filtered_df["Amount"] > 0,
    "Amount"
].sum()

expenses = -filtered_df.loc[
    filtered_df["Amount"] < 0,
    "Amount"
].sum()

savings = income - expenses

savings_rate = (
    savings / income * 100
    if income > 0
    else None
)

# =====================================
# FINANCIAL OVERVIEW
# =====================================

st.subheader("📈 Financial Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "TOTAL INCOME",
    f"{income:,.2f} PLN"
)

col2.metric(
    "TOTAL EXPENSES",
    f"{expenses:,.2f} PLN"
)

col3.metric(
    "NET SAVINGS",
    f"{savings:,.2f} PLN"
)

col4.metric(
    "SAVINGS RATE",
    f"{savings_rate:.1f}%"
    if savings_rate is not None
    else "N/A"
)

st.caption(
    f"Analyzing {len(filtered_df)} "
    f"of {len(df)} transactions"
)

# =====================================
# SAVINGS PERFORMANCE
# =====================================

st.markdown("#### 💚 Savings Performance")

if savings_rate is not None:
    progress = max(
        0.0,
        min(savings_rate / 100, 1.0)
    )

    st.progress(progress)

    st.caption(
        f"{savings_rate:.1f}% of your income "
        "remains after expenses."
    )
else:
    st.info(
        "Savings rate requires income "
        "in the selected transactions."
    )

st.divider()

# =====================================
# SPENDING ANALYSIS
# =====================================

st.subheader("📊 Spending Insights")

expense_df = filtered_df[
    filtered_df["Amount"] < 0
].copy()

expense_df["Amount"] = (
    expense_df["Amount"].abs()
)

if not expense_df.empty:

    category_expenses = (
        expense_df
        .groupby("Category", as_index=False)["Amount"]
        .sum()
        .sort_values("Amount", ascending=False)
    )

    chart1, chart2 = st.columns(2)

    with chart1:

        fig_pie = px.pie(
            category_expenses,
            names="Category",
            values="Amount",
            title="Expense Distribution",
            hole=0.55,
            color_discrete_sequence=px.colors.sequential.Teal
        )

        fig_pie.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="#F1F5F9",
            margin=dict(
                l=10,
                r=10,
                t=50,
                b=10
            )
        )

        st.plotly_chart(
            fig_pie,
            use_container_width=True
        )

    with chart2:

        fig_bar = px.bar(
            category_expenses,
            x="Amount",
            y="Category",
            orientation="h",
            title="Top Spending Categories",
            color_discrete_sequence=["#10B981"]
        )

        fig_bar.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="#F1F5F9",
            yaxis={
                "categoryorder": "total ascending"
            },
            margin=dict(
                l=10,
                r=10,
                t=50,
                b=10
            )
        )

        st.plotly_chart(
            fig_bar,
            use_container_width=True
        )

else:
    category_expenses = pd.DataFrame(
        columns=["Category", "Amount"]
    )

    st.info(
        "No expense transactions match your filters."
    )

st.divider()

# =====================================
# MONTHLY FINANCIAL TRENDS
# =====================================

st.subheader("📅 Monthly Financial Trends")

monthly_df = filtered_df.copy()

monthly_df["Month"] = (
    monthly_df["Date"]
    .dt.to_period("M")
    .astype(str)
)

monthly_df["Income"] = (
    monthly_df["Amount"].clip(lower=0)
)

monthly_df["Expenses"] = (
    -monthly_df["Amount"].clip(upper=0)
)

monthly_summary = (
    monthly_df
    .groupby("Month", as_index=False)[
        ["Income", "Expenses"]
    ]
    .sum()
    .sort_values("Month")
)

monthly_long = monthly_summary.melt(
    id_vars="Month",
    value_vars=["Income", "Expenses"],
    var_name="Type",
    value_name="Amount"
)

fig_monthly = px.bar(
    monthly_long,
    x="Month",
    y="Amount",
    color="Type",
    barmode="group",
    title="Income vs Expenses",
    color_discrete_map={
        "Income": "#10B981",
        "Expenses": "#F59E0B"
    }
)

fig_monthly.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font_color="#F1F5F9",
    margin=dict(
        l=10,
        r=10,
        t=50,
        b=10
    )
)

st.plotly_chart(
    fig_monthly,
    use_container_width=True
)

st.divider()

# =====================================
# SMART FINANCIAL INSIGHTS
# =====================================

st.subheader("🧠 Smart Financial Insights")

st.caption(
    "Automatically generated insights "
    "from your selected transactions."
)

# Highest expense category

if not expense_df.empty:

    top_category = category_expenses.iloc[0]

    top_category_name = top_category["Category"]
    top_category_amount = top_category["Amount"]

    expense_share = (
        top_category_amount / expenses * 100
        if expenses > 0
        else 0
    )

else:
    top_category_name = "N/A"
    top_category_amount = 0
    expense_share = 0

insight1, insight2, insight3 = st.columns(3)

with insight1:

    st.metric(
        "Highest Expense Category",
        top_category_name
    )

    st.caption(
        f"{top_category_amount:,.2f} PLN "
        f"({expense_share:.1f}% of expenses)"
    )

with insight2:

    st.metric(
        "Net Cash Flow",
        f"{savings:,.2f} PLN"
    )

    if savings > 0:
        st.success("Positive cash flow")

    elif savings < 0:
        st.warning("Negative cash flow")

    else:
        st.info("Balanced cash flow")

with insight3:

    st.metric(
        "Savings Performance",
        f"{savings_rate:.1f}%"
        if savings_rate is not None
        else "N/A"
    )

    if savings_rate is None:
        st.info("No income in selected transactions")

    elif savings_rate >= 30:
        st.success("High savings rate")

    elif savings_rate >= 10:
        st.info("Moderate savings rate")

    elif savings_rate >= 0:
        st.warning("Low savings rate")

    else:
        st.error("Expenses exceed income")

st.divider()

# =====================================
# MONTH-OVER-MONTH ANALYSIS
# =====================================

st.subheader("📉 Monthly Spending Trends")

expense_trend = monthly_summary[
    ["Month", "Expenses"]
].copy()

expense_trend = expense_trend.sort_values("Month")

expense_trend["Previous Month"] = (
    expense_trend["Expenses"].shift(1)
)

expense_trend["Change (%)"] = (
    expense_trend["Expenses"].pct_change(
        fill_method=None
    ) * 100
)

fig_trend = px.line(
    expense_trend,
    x="Month",
    y="Expenses",
    markers=True,
    title="Monthly Expense Trend",
    labels={
        "Month": "Month",
        "Expenses": "Expenses (PLN)"
    }
)

fig_trend.update_traces(
    line_color="#10B981",
    line_width=3,
    marker_size=9
)

fig_trend.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font_color="#F1F5F9"
)

st.plotly_chart(
    fig_trend,
    use_container_width=True
)

# Latest month comparison

if len(expense_trend) >= 2:

    latest = expense_trend.iloc[-1]
    previous = expense_trend.iloc[-2]

    latest_month = pd.Period(
        latest["Month"],
        freq="M"
    )

    previous_month = pd.Period(
        previous["Month"],
        freq="M"
    )

    latest_expenses = latest["Expenses"]
    previous_expenses = previous["Expenses"]

    if latest_month - 1 != previous_month:

        st.info(
            "The latest two months are not consecutive. "
            "Month-over-month comparison is unavailable."
        )

    elif previous_expenses > 0:

        change = (
            (latest_expenses - previous_expenses)
            / previous_expenses * 100
        )

        if change > 0:

            st.warning(
                f"Expenses increased by {change:.1f}% "
                "compared with the previous month."
            )

        elif change < 0:

            st.success(
                f"Expenses decreased by {abs(change):.1f}% "
                "compared with the previous month."
            )

        else:

            st.info(
                "Expenses remained unchanged "
                "compared with the previous month."
            )

    else:

        st.info(
            "The previous month has no expenses, "
            "so percentage change is unavailable."
        )

else:

    st.info(
        "At least two months of data are needed "
        "for monthly spending comparisons."
    )

st.divider()

# =====================================
# AUTOMATED FINANCIAL SUMMARY
# =====================================

st.subheader("💡 Financial Summary")

if savings > 0:

    st.success(
        f"Your selected transactions show "
        f"positive net cash flow of "
        f"{savings:,.2f} PLN."
    )

elif savings < 0:

    st.warning(
        f"Your expenses exceed your income by "
        f"{abs(savings):,.2f} PLN."
    )

else:

    st.info(
        "Your income and expenses are equal "
        "for the selected transactions."
    )

if expenses > 0:

    st.write(
        f"Your largest expense category is "
        f"**{top_category_name}**, representing "
        f"**{expense_share:.1f}%** of your spending."
    )

if savings_rate is not None:

    st.write(
        f"Your current savings rate is "
        f"**{savings_rate:.1f}%**."
    )

st.caption(
    "Insights are descriptive and based on "
    "selected transactions. Not financial advice."
)

st.divider()

# =====================================
# TRANSACTION HISTORY
# =====================================

st.subheader("📋 Transaction History")

display_df = filtered_df.sort_values(
    "Date",
    ascending=False
).copy()

st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True,
    column_config={
        "Date": st.column_config.DateColumn(
            "Date",
            format="YYYY-MM-DD"
        ),
        "Category": st.column_config.TextColumn(
            "Category"
        ),
        "Amount": st.column_config.NumberColumn(
            "Amount (PLN)",
            format="%.2f"
        )
    }
)

# =====================================
# CSV EXPORT
# =====================================

csv = filtered_df.to_csv(
    index=False,
    date_format="%Y-%m-%d"
).encode("utf-8")

st.download_button(
    "⬇️ Export Filtered Transactions",
    data=csv,
    file_name="finsight_transactions.csv",
    mime="text/csv"
)

# =====================================
# FOOTER
# =====================================

st.divider()

st.caption(
    "FinSight | Personal Finance Analytics "
    "— Built with Python, Pandas, Streamlit & Plotly"
)
