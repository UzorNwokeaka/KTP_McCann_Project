import os

import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///local_backpack.db")

if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(DATABASE_URL)

st.set_page_config(
    page_title="QS Dashboard",
    page_icon="",
    layout="wide",
)

st.markdown("""
# J McCann & Co. Ltd

""")

st.divider()

st.title("QS Operational Dashboard")
st.caption("Commercial Review | Cost Visibility | Operational Performance Monitoring")


def load_job_submissions():
    query = """
    SELECT
        id,
        operative_name,
        operative_employee_number,
        job_reference,
        asset_id,
        location,
        job_type,
        work_completed,
        hours_on_site,
        number_of_operatives,
        vehicle_type,
        tool_type,
        tool_hours,
        labour_cost,
        vehicle_cost,
        tool_cost,
        material_cost,
        total_cost,
        qs_approved,
        created_at
    FROM job_submissions
    ORDER BY created_at DESC
    """

    return pd.read_sql(query, engine)


def load_audit_logs():
    query = """
    SELECT
        id,
        job_reference,
        action_type,
        description,
        created_at
    FROM audit_logs
    ORDER BY created_at DESC
    """

    return pd.read_sql(query, engine)


try:
    jobs_df = load_job_submissions()
    audit_df = load_audit_logs()

    if jobs_df.empty:
        st.info("No job submissions have been recorded yet.")
    else:
        total_jobs = len(jobs_df)
        total_cost = jobs_df["total_cost"].sum()
        average_cost = jobs_df["total_cost"].mean()
        total_labour_cost = jobs_df["labour_cost"].sum()

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Total Jobs Submitted", f"{total_jobs}")
        col2.metric("Total Estimated Cost", f"£{total_cost:,.2f}")
        col3.metric("Average Cost per Job", f"£{average_cost:,.2f}")
        col4.metric("Total Labour Cost", f"£{total_labour_cost:,.2f}")

        st.divider()

        st.subheader("Submitted Jobs for QS Review")

        review_columns = [
            "id",
            "operative_name",
            "operative_employee_number",
            "job_reference",
            "asset_id",
            "location",
            "job_type",
            "hours_on_site",
            "number_of_operatives",
            "vehicle_type",
            "tool_type",
            "tool_hours",
            "labour_cost",
            "vehicle_cost",
            "tool_cost",
            "material_cost",
            "total_cost",
            "qs_approved",
            "created_at",
        ]

        st.dataframe(
            jobs_df[review_columns],
            use_container_width=True,
            hide_index=True,
        )

        st.subheader("Work Completion Notes")

        st.dataframe(
            jobs_df[
                [
                    "job_reference",
                    "operative_name",
                    "operative_employee_number",
                    "asset_id",
                    "location",
                    "job_type",
                    "work_completed",
                ]
            ],
            use_container_width=True,
            hide_index=True,
        )

        st.subheader("Cost Breakdown by Job Type")

        cost_by_job_type = (
            jobs_df.groupby("job_type")["total_cost"]
            .sum()
            .reset_index()
            .sort_values(by="total_cost", ascending=False)
        )

        st.dataframe(
            cost_by_job_type,
            use_container_width=True,
            hide_index=True,
        )

        st.subheader("Cost Components Summary")

        cost_components = pd.DataFrame(
            {
                "Cost Component": [
                    "Labour",
                    "Vehicle",
                    "Tool/Plant",
                    "Materials",
                ],
                "Amount": [
                    jobs_df["labour_cost"].sum(),
                    jobs_df["vehicle_cost"].sum(),
                    jobs_df["tool_cost"].sum(),
                    jobs_df["material_cost"].sum(),
                ],
            }
        )

        st.dataframe(
            cost_components,
            use_container_width=True,
            hide_index=True,
        )

        st.subheader("Audit Logs")

        st.dataframe(
            audit_df,
            use_container_width=True,
            hide_index=True,
        )

except Exception as error:
    st.error("Unable to load dashboard data.")
    st.exception(error)
