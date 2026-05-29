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
    page_icon="📊",
    layout="wide",
)

col1, col2 = st.columns([1, 5])

with col1:
    st.image(
        "assets/jmccann_logo.png",
        width=120,
    )

with col2:
    st.markdown("""
# J. McCann & Co. Ltd

**Commercial Review | Cost Visibility | Operational Performance Monitoring**
""")

# col1, col2 = st.columns([1, 6])

# with col1:
#     st.image(
#         "assets/jmccann_logo.png",
#         width=120,
#     )

# with col2:
#     st.markdown(
#         """
# # J. McCann & Co. Ltd

# """
#     )

# st.caption("Commercial Review | Cost Visibility | Operational Performance Monitoring")

st.divider()


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

        st.subheader("Operational Performance Summary")

        metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)

        metric_col1.metric("Jobs Submitted", f"{total_jobs}")
        metric_col2.metric("Total Cost", f"£{total_cost:,.2f}")
        metric_col3.metric("Average Job Cost", f"£{average_cost:,.2f}")
        metric_col4.metric("Labour Cost", f"£{total_labour_cost:,.2f}")

        st.divider()

        st.subheader("Job Register")

        job_register_columns = [
            "job_reference",
            "operative_name",
            "operative_employee_number",
            "asset_id",
            "job_type",
            "location",
            "hours_on_site",
            "total_cost",
            "qs_approved",
            "created_at",
        ]

        st.dataframe(
            jobs_df[job_register_columns],
            use_container_width=True,
            hide_index=True,
        )

        st.subheader("Detailed Cost Records")

        detailed_cost_columns = [
            "job_reference",
            "vehicle_type",
            "tool_type",
            "tool_hours",
            "labour_cost",
            "vehicle_cost",
            "tool_cost",
            "material_cost",
            "total_cost",
        ]

        st.dataframe(
            jobs_df[detailed_cost_columns],
            use_container_width=True,
            hide_index=True,
        )

        st.subheader("Work Completion Records")

        work_completion_columns = [
            "job_reference",
            "operative_name",
            "operative_employee_number",
            "asset_id",
            "location",
            "job_type",
            "work_completed",
        ]

        st.dataframe(
            jobs_df[work_completion_columns],
            use_container_width=True,
            hide_index=True,
        )

        st.subheader("Cost Analysis by Job Type")

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

        st.subheader("Cost Component Analysis")

        cost_components = pd.DataFrame(
            {
                "Cost Component": [
                    "Labour",
                    "Vehicle",
                    "Tool/Plant",
                    "Materials",
                ],
                "Total Cost": [
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

        st.subheader("Audit Trail")

        st.dataframe(
            audit_df,
            use_container_width=True,
            hide_index=True,
        )

except Exception as error:
    st.error("Unable to load dashboard data.")
    st.exception(error)
