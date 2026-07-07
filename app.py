

import sqlite3
import pandas as pd
import streamlit as st

# ---------------------------------------------------------------------------
# Page config (must be the first Streamlit call)
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Uber Eats Bangalore — Restaurant Intelligence",
    layout="wide",
)

# ---------------------------------------------------------------------------
# Data loading (cached so CSVs are read / loaded into SQLite only once)
# ---------------------------------------------------------------------------
@st.cache_resource
def get_connection():
    """Create an in-memory SQLite DB and load the restaurant CSV into it."""
    conn = sqlite3.connect(":memory:", check_same_thread=False)
    df = pd.read_csv("c_data.csv")
    df.to_sql("uber_eats_res_data", conn, index=False, if_exists="replace")
    return conn


@st.cache_data
def load_orders():
    return pd.read_csv("orders.csv")


conn = get_connection()

# ---------------------------------------------------------------------------
# Top-level navigation
# ---------------------------------------------------------------------------
st.title("📊 Uber Eats Bangalore Restaurant Intelligence & Decision Support")

tab_dashboard, tab_business_qa, tab_order_qa = st.tabs(
    ["🧭 Dashboard", "💼 Business Q&A", "🧾 Order Data Q&A"]
)

# ===========================================================================
# TAB 1 — DASHBOARD
# ===========================================================================
with tab_dashboard:
    st.text(
        "Uber Eats operates a large-scale restaurant marketplace where business "
        "success depends on factors such as location strategy, pricing, cuisine "
        "mix, customer ratings, and platform features like online ordering and "
        "table booking."
    )

    base_df = pd.read_sql("SELECT * FROM uber_eats_res_data", conn)

    # --- Sidebar filters --------------------------------------------------
    st.sidebar.header("Dashboard Filters")

    locations = sorted(base_df["location"].dropna().unique().tolist())
    selected_loc = st.sidebar.selectbox("Select Location", options=["All"] + locations)

    rest_types = sorted(base_df["rest_type"].dropna().unique().tolist())
    selected_rest_types = st.sidebar.multiselect(
        "Select Restaurant Type", options=rest_types, default=rest_types
    )

    min_rating, max_rating = st.sidebar.slider(
        "Select Rating Range",
        min_value=0.0,
        max_value=5.0,
        value=(0.0, 5.0),
        step=0.1,
    )

    online_order = st.sidebar.radio("Online Order Available?", options=["All", "yes", "no"])

    # --- Build ONE combined query with all filters applied together -------
    conditions = ["1=1"]
    params = []

    if selected_loc != "All":
        conditions.append("location = ?")
        params.append(selected_loc)

    if selected_rest_types:
        placeholders = ",".join(["?"] * len(selected_rest_types))
        conditions.append(f"rest_type IN ({placeholders})")
        params.extend(selected_rest_types)
    else:
        # Nothing selected -> no restaurant types match
        conditions.append("1=0")

    conditions.append("rate BETWEEN ? AND ?")
    params.extend([min_rating, max_rating])

    if online_order != "All":
        conditions.append("online_order = ?")
        params.append(online_order)

    query = f"SELECT * FROM uber_eats_res_data WHERE {' AND '.join(conditions)}"
    filtered_df = pd.read_sql(query, conn, params=params)

    st.subheader(f"Filtered Results ({len(filtered_df)} restaurants)")
    st.dataframe(filtered_df, use_container_width=True)

# ===========================================================================
# TAB 2 — BUSINESS Q&A
# ===========================================================================
with tab_business_qa:
    st.title("📊 Business Q&A")

    # ---- Question 1 -------------------------------------------------------
    st.subheader(
        """1. Which Bangalore locations have the highest average restaurant ratings?
**Business Value:** Identifies premium-performing areas suitable for brand positioning and new partner onboarding."""
    )
    df = pd.read_sql(
        """
        SELECT location, AVG(rate) AS avg_rating
        FROM uber_eats_res_data
        WHERE rate IS NOT NULL
        GROUP BY location
        ORDER BY avg_rating DESC
        LIMIT 10
        """,
        conn,
    )
    st.dataframe(df, use_container_width=True, hide_index=True)
    st.markdown(
        """***Based on my analysis,
1. Lavelle Road (4.19),
2. Koramangala 5th Block (4.15),
3. Sankey Road (4.10)
have the highest average restaurant ratings in Bangalore.
These areas are very suitable for brand positioning and new partner onboarding.***"""
    )

    # ---- Question 2 -------------------------------------------------------
    st.subheader(
        """2. Which locations are over-saturated with restaurants?
**Business Value:** Helps avoid overcrowded markets and guides smarter expansion decisions."""
    )
    df = pd.read_sql(
        """
        SELECT location, COUNT(*) AS total
        FROM uber_eats_res_data
        GROUP BY location
        ORDER BY total DESC
        LIMIT 5
        """,
        conn,
    )
    st.dataframe(df, hide_index=True)
    st.markdown(
        """***Koramangala 5th Block has 1782 restaurants,
BTM has 1454 restaurants,
Indiranagar has 1345 restaurants,
HSR has 1161 restaurants,
Jayanagar has 1037 restaurants.***"""
    )

    # ---- Question 3 -------------------------------------------------------
    st.subheader(
        """3. Does online ordering improve restaurant ratings?
**Business Value:** Evaluates the ROI of Uber Eats online ordering feature for partners."""
    )
    df = pd.read_sql(
        """
        SELECT online_order, AVG(rate) AS avg_rating, COUNT(*) AS total
        FROM uber_eats_res_data
        GROUP BY online_order
        """,
        conn,
    )
    st.dataframe(df, hide_index=True)
    st.markdown(
        """***Online ordering alone does not significantly improve restaurant rating.
Therefore, Uber Eats may need to focus on improving delivery experience, order accuracy,
and service quality to increase partner ROI.***"""
    )

    # ---- Question 4 -------------------------------------------------------
    st.subheader(
        """4. Does table booking correlate with higher customer ratings?
**Business Value:** Measures the effectiveness of table booking as a premium feature."""
    )
    df = pd.read_sql(
        """
        SELECT book_table, AVG(rate) AS avg_rating, COUNT(*) AS total
        FROM uber_eats_res_data
        GROUP BY book_table
        """,
        conn,
    )
    st.dataframe(df, hide_index=True)
    st.markdown(
        """***Restaurants offering table booking (often combined with online ordering)
show noticeably higher ratings, indicating a strong positive correlation between
table booking and ratings. Customers likely prefer convenience and reduced waiting time.***"""
    )

    # ---- Question 5 -------------------------------------------------------
    st.subheader(
        """5. What price range delivers the best customer satisfaction?
**Business Value:** Helps define the optimal pricing segment for partner success."""
    )
    df = pd.read_sql(
        """
        SELECT "approx_cost(for two people)" AS approx_cost,
               AVG(rate) AS avg_rating,
               COUNT(*) AS total
        FROM uber_eats_res_data
        GROUP BY "approx_cost(for two people)"
        ORDER BY avg_rating DESC
        """,
        conn,
    )
    st.dataframe(df, hide_index=True)
    st.markdown(
        """***Mid to high price range restaurants (₹800–₹2000) deliver the best customer satisfaction,
maintaining consistently high ratings with a significant number of restaurants. While very
high-priced restaurants show slightly higher ratings, the sample size is small, making
mid-range the most reliable segment.***"""
    )

    # ---- Question 6 -------------------------------------------------------
    st.subheader(
        """6. How do low, mid, and premium-priced restaurants perform in terms of ratings?
**Business Value:** Supports pricing-based market segmentation strategies."""
    )
    df = pd.read_sql(
        """
        SELECT price_category, AVG(rate) AS avg_rating, COUNT(*) AS total
        FROM (
            SELECT
                rate,
                CASE
                    WHEN "approx_cost(for two people)" <= 500 THEN 'low'
                    WHEN "approx_cost(for two people)" BETWEEN 501 AND 1500 THEN 'mid'
                    ELSE 'premium'
                END AS price_category
            FROM uber_eats_res_data
        )
        GROUP BY price_category
        ORDER BY avg_rating DESC
        """,
        conn,
    )
    st.dataframe(df, hide_index=True)
    st.markdown(
        """***Premium-priced restaurants have the highest average ratings (4.23),
followed by mid-range restaurants (3.96) and low-priced restaurants (3.79).
This indicates that customer satisfaction tends to increase with price, likely due to
better quality, service, and overall experience.

Premium restaurants provide a superior experience, while mid-range offers a balance
between affordability and quality.

However, this reflects correlation, not causation. Higher ratings may also be
influenced by factors like cuisine, service quality, and location.***"""
    )

    # ---- Question 7 -------------------------------------------------------
    st.subheader(
        """7. Which cuisines are most common in Bangalore?
**Business Value:** Reveals market demand and cuisine saturation levels."""
    )
    df = pd.read_sql("SELECT cuisines FROM uber_eats_res_data", conn)
    df = df.dropna(subset=["cuisines"])
    df["cuisines"] = df["cuisines"].str.split(",")
    df = df.explode("cuisines")
    df["cuisines"] = df["cuisines"].str.strip().str.replace("_", "").str.lower()
    result = df["cuisines"].value_counts().reset_index()
    result.columns = ["cuisines", "total"]
    st.dataframe(result.head(10), hide_index=True)
    st.markdown(
        """***North Indian and Chinese cuisines are the most common in Bangalore.
This indicates high customer demand but also high market saturation.***"""
    )

    # ---- Question 8 -------------------------------------------------------
    st.subheader(
        """8. Which cuisines receive the highest average ratings?
**Business Value:** Identifies high-quality cuisine categories suitable for promotion."""
    )
    df = pd.read_sql("SELECT cuisines, rate FROM uber_eats_res_data", conn)
    df = df.dropna(subset=["cuisines", "rate"])
    df["cuisines"] = df["cuisines"].str.split(",")
    df = df.explode("cuisines")
    df["cuisines"] = df["cuisines"].str.strip().str.replace("_", "").str.lower()

    counts = df["cuisines"].value_counts()
    valid = counts[counts > 50].index
    filtered = df[df["cuisines"].isin(valid)]

    result = filtered.groupby("cuisines")["rate"].mean().reset_index()
    result = result.sort_values(by="rate", ascending=False)
    st.dataframe(result.head(10), hide_index=True)
    st.markdown(
        """***After filtering cuisines with sufficient data, Malaysian, Modern Indian,
and Mediterranean cuisines have the highest average ratings. This indicates that these
cuisines deliver better customer satisfaction and belong to the premium segment. These
categories can be targeted for promotions or high-end restaurant investments.***"""
    )

    # ---- Question 9 -------------------------------------------------------
    st.subheader(
        """9. Which cuisines perform well despite having fewer restaurants?
**Business Value:** Highlights niche opportunities for differentiation."""
    )
    df = pd.read_sql("SELECT cuisines, rate FROM uber_eats_res_data", conn)
    df = df.dropna(subset=["cuisines", "rate"])
    df["cuisines"] = df["cuisines"].str.split(",")
    df = df.explode("cuisines")
    df["cuisines"] = df["cuisines"].str.strip().str.replace("_", "").str.lower()

    res1 = df.groupby("cuisines").agg(
        total_restaurants=("cuisines", "count"), avg_rating=("rate", "mean")
    ).reset_index()

    niche = res1[(res1["total_restaurants"] < 20) & (res1["avg_rating"] > 4.2)]
    niche = niche.sort_values(by="avg_rating", ascending=False)
    st.dataframe(niche, hide_index=True)
    st.markdown(
        """***These cuisines represent niche opportunities where demand quality is high but
supply is limited. Expanding these categories can help platforms differentiate and attract
premium customers. Cuisines like Cantonese, African, and Belgian perform exceptionally well
despite low availability, indicating strong niche demand and expansion opportunities.***"""
    )

    # ---- Question 10 ------------------------------------------------------
    st.subheader(
        """10. What is the relationship between restaurant cost and rating?
**Business Value:** Determines whether higher pricing translates to better customer perception."""
    )
    df = pd.read_sql(
        """
        SELECT
            CASE
                WHEN "approx_cost(for two people)" <= 500 THEN 'low'
                WHEN "approx_cost(for two people)" BETWEEN 501 AND 1500 THEN 'mid'
                ELSE 'premium'
            END AS price_category,
            COUNT(*) AS total_restaurants,
            AVG(rate) AS avg_rating
        FROM uber_eats_res_data
        GROUP BY price_category
        ORDER BY avg_rating DESC
        """,
        conn,
    )
    st.dataframe(df, hide_index=True)
    st.markdown(
        """***There is a mild positive relationship between cost and rating, but high pricing
does not guarantee significantly better customer satisfaction.***"""
    )

# ===========================================================================
# TAB 3 — ORDER DATA Q&A
# ===========================================================================
with tab_order_qa:
    st.title("Order Data Integration & Custom Analytical Q&A")

    orders_df = load_orders()

    # Normalized helper columns for robust, case-insensitive comparisons
    orders_df["_restaurant_name_norm"] = orders_df["restaurant_name"].str.strip().str.lower()
    orders_df["_discount_used_norm"] = orders_df["discount_used"].str.strip().str.lower()

    st.subheader("1. How many unique restaurants are listed in this dataset?")
    st.dataframe(orders_df.drop(columns=["_restaurant_name_norm", "_discount_used_norm"]))
    unique_restaurants = orders_df["restaurant_name"].nunique()
    st.metric(label="Total Unique Restaurants", value=unique_restaurants)

    st.divider()

    st.subheader("2. What is the restaurant_name for the order placed on 2026-01-08?")
    st.dataframe(orders_df[orders_df["order_date"] == "2026-01-08"]["restaurant_name"])

    st.divider()

    st.subheader(
        """3. List all order IDs where a discount was actually used (discount_used is "Yes")"""
    )
    discount_orders = orders_df[orders_df["_discount_used_norm"] == "yes"]["order_id"]
    st.write("order_id with discount used")
    st.dataframe(discount_orders)

    st.divider()

    st.subheader(
        "4. What is the total sum of order_value for all orders placed at Bawarchi Inn?"
    )
    bawarchi_sum = orders_df[orders_df["_restaurant_name_norm"] == "bawarchi inn"][
        "order_value"
    ].sum()
    st.metric(label="Total Sales: Bawarchi Inn", value=f"₹{bawarchi_sum:,.2f}")

    st.divider()

    st.subheader("5. Which restaurant had the highest single order_value in the entire list?")
    max_order_idx = orders_df["order_value"].idxmax()
    top_restaurant = orders_df.loc[max_order_idx, "restaurant_name"]
    max_value = orders_df.loc[max_order_idx, "order_value"]
    st.write("### Highest Value Order")
    st.metric(label=f"Highest Order: {str(top_restaurant).title()}", value=f"₹{max_value:,.2f}")

    st.divider()
