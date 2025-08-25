import os
import sys
current_path = os.path.dirname(os.path.abspath(__file__))
parent_path = os.path.abspath(os.path.join(current_path, ".."))
sys.path.append(parent_path)
import pandas as pd
import streamlit as st
import duckdb
import altair as alt

def select_data_report(target_table):
    duckdb.install_extension("ducklake")
    duckdb.load_extension("ducklake")
    db_path = os.path.join(parent_path, "ondoriya.db")
    con = duckdb.connect(db_path)
    data_path = os.path.join(parent_path, "data")
    catalog_path = os.path.join(parent_path, "catalog.ducklake")
    con.execute(f"ATTACH 'ducklake:{catalog_path}' AS my_ducklake (DATA_PATH '{data_path}')")
    con.execute("USE my_ducklake")
    result_df = con.execute(f"SELECT * FROM {target_table}").df()
    con.close()
    return result_df

def dashboard():
    st.set_page_config(page_title="Ondoriya Data Analysis", layout="wide")
    st.title("Ondoriya Data Analysis")

    with st.spinner("Loading data aggregations..."):
        df_population = select_data_report("CLEANED.TOTAL_POPULATION")
        df_dominant_faction = select_data_report("CLEANED.DOMINANT_FACTION")
        df_population_density = select_data_report("CLEANED.POPULATION_DENSITY")
        df_faction_distribution = select_data_report("CLEANED.FACTION_DISTRIBUTION_CLEANED")
        df_top_5_regions = select_data_report("CLEANED.TOP_5_POPULOUS_REGIONS")

    DATASETS = {
        "Total Population": df_population,
        "Dominant Faction": df_dominant_faction,
        "Population Density": df_population_density,
        "Faction Distribution": df_faction_distribution,
        "Top 5 Regions": df_top_5_regions,
    }

    # --- KPIs ---
    kpi_column_total, kpi_column_dominant, _ = st.columns([1, 1, 2])

    total_population_value = int(df_population["TOTAL_POPULATION"].iloc[0])
    dominant_faction_value = str(df_dominant_faction["Faction"].iloc[0])

    kpi_column_total.metric("Total Population", total_population_value)
    kpi_column_dominant.metric("Dominant Faction", dominant_faction_value)

    st.markdown("---")

    # Population density
    st.header("Population Density by Region")
    region_column = "Colloquial_Name"
    population_column = "population"
    simple_density_df = df_population_density[[region_column, population_column]].dropna().rename(columns=lambda column_name: str(column_name))
    simple_density_chart = alt.Chart(simple_density_df).mark_bar().encode(
        x=alt.X(str(population_column), title="Population"),
        y=alt.Y(str(region_column), sort='-x', title="Region"),
    ).properties(height=400)
    st.altair_chart(simple_density_chart, use_container_width=True)

    st.markdown("---")

    # show Faction distribution and Top 5 regions side-by-side
    left_column, right_column = st.columns(2)

    with left_column:
        # Faction distribution
        st.header("Faction Distribution")
        faction_distribution_subsetted = df_faction_distribution[["Faction", "Percent"]].copy()
        faction_distribution_subsetted["Percent_numeric"] = pd.to_numeric(
            faction_distribution_subsetted["Percent"].astype(str)
                .str.replace("%", "", regex=False)
                .str.replace(",", "", regex=False)
                .str.strip(),
            errors="coerce",
        )
        faction_distribution_subsetted = faction_distribution_subsetted.sort_values(by="Percent_numeric", ascending=False).reset_index(drop=True)
        faction_distribution_subsetted["Percent_display"] = faction_distribution_subsetted["Percent_numeric"].map(
            lambda value: f"{value:.2f}%"
        )
        st.dataframe(faction_distribution_subsetted[["Faction", "Percent_display"]].rename(columns={"Percent_display": "Percent"}))

    with right_column:
        # Top 5 regions
        st.header("Top 5 Most Populous Regions")
        region_column = "Colloquial_Name"
        population_column = "population"
        simple_top_df = df_top_5_regions[[region_column, population_column]].dropna().rename(columns=lambda column_name: str(column_name))
        top_chart = alt.Chart(simple_top_df).mark_bar().encode(
            x=alt.X(str(population_column), title="Population"),
            y=alt.Y(str(region_column), sort='-x', title="Region"),
        ).properties(height=300)
        st.altair_chart(top_chart, use_container_width=True)

    

if __name__ == "__main__":
    dashboard()