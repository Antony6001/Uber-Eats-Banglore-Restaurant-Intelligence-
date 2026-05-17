
# 🚀 Uber Eats Bangalore – Restaurant Intelligence & Decision Support System

An end-to-end data analytics and business intelligence system designed to optimize restaurant performance marketplace logistics in Bangalore. This project processes multi-format raw data (CSV & JSON), implements dynamic analytical business logic strictly via SQL, and surfaces insights through an interactive Streamlit web dashboard.

## 🛠️ Project Architecture & Data Pipeline

```text
Data Sources (orders.json & c_data.csv)
      │
      ▼
Data Cleaning & Feature Engineering (Pandas / Jupyter Notebooks)
      │
      ▼
Relational Database Layer (MySQL / restaurant.db)
      │
      ▼
SQL Analytics Layer (Complex Queries, Joins, Aggregations)
      │
      ▼
Interactive UI Dashboard (Streamlit App)

```

---

## 📂 Repository Structure

* **`Dashboard.py`**: The main entry point for the Streamlit dashboard user interface.
* **`json_file_cleaning.ipynb`**: Jupyter notebook handling raw JSON data flattening, missing value parsing, and preparation.
* **`mini_project_mysql.ipynb`**: Notebook focusing on schema creation, data insertion, and drafting complex SQL analytical queries.
* **`uber_eats_bangalore_mini_project.ipynb`**: Core exploratory data analysis (EDA) and early prototyping.
* **`restaurant.db` / `c_data.csv` / `orders.json**`: The structured database and raw/cleaned datasets driving the application.
* **`screenshots/`**: Visual documentation of the operational dashboard application.

---

## 🔧 Core Features & Implementation

### 🔹 1. Dynamic Analytics Dashboard

* Fully integrated user interface using Streamlit.
* Multi-dimensional data filtration capabilities by **Location**, **Cuisine Type**, **Customer Ratings**, and **Price Range**.
* Efficient data extraction powered by an underlying SQL engine returning clean tabular data frames.

### 🔹 2. SQL-Driven Q&A Intelligence Module

Features a dedicated section answering over 10 critical operational business questions using raw SQL queries (`GROUP BY`, `CASE WHEN`, subqueries, and window functions):

* **Location Strategy:** Identifying high-performing vs. heavily saturated culinary pockets.
* **Pricing Optimization:** Evaluating price distributions to find sweet spots where ratings peak.
* **Feature Impact:** Assessing how platform features like *Online Ordering* and *Table Booking* affect customer satisfaction scores.

### 🔹 3. Semi-Structured Order Data Integration

* Built a custom pipeline to ingest, flatten, and normalize semi-structured `orders.json` files.
* Relational conversion to SQL tables to allow side-by-side behavioral analysis matching restaurant profiles with transactional order histories.

---

## 💼 Business Use Cases Addressed

* **📍 Location Intelligence:** Pinpoints optimal expansion zones for scaling chains or cloud kitchens based on supply-demand density.
* **💰 Pricing Matrix Strategy:** Analyzes market pricing segments to optimize menus for maximizing margins without shedding active customer ratings.
* **🍜 Cuisine Mix & Performance:** Segments local high-volume mainstream cuisines against high-margin premium niche offerings.
* **🤝 Partner Onboarding:** Provides data-backed consulting metrics to new culinary partners looking to sign onto the platform.

---

## 🚀 Getting Started

### 1. Prerequisites

Ensure you have Python 3.x installed along with a localized database environment setup. Install dependencies via pip:

```bash
pip install pandas numpy streamlit tabulate mysql-connector-python

```

### 2. Database Set Up & Data Cleaning

Execute the data engineering pipeline notebooks to generate your localized database structures:

1. Run `json_file_cleaning.ipynb` to structure the raw JSON orders.
2. Run `mini_project_mysql.ipynb` to establish table schemas and populate your SQL tables.

### 3. Launching the Dashboard App

Boot up the Streamlit interface locally using the following terminal command:

```bash
streamlit run Dashboard.py

``` 
