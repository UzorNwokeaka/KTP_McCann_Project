from datetime import datetime, time

import streamlit as st

try:
    from src.db import init_db, save_job_submission
except ModuleNotFoundError:
    from db import init_db, save_job_submission

LABOUR_RATE_PER_HOUR = 30.00

VEHICLE_RATES = {
    "Van": 15.00,
    "Pickup Truck": 20.00,
    "None": 0.00,
}

TOOL_RATES = {
    "None": 0.00,
    "Cherry Picker": 45.00,
    "Cable Locator": 18.00,
    "Testing Kit": 12.00,
}

MATERIAL_COSTS = {
    "Lamp Unit": 50.00,
    "Cable per metre": 3.00,
    "Fuse": 6.00,
}


def calculate_hours(start_time: time, end_time: time) -> float:
    """Calculate total hours between arrival and departure."""
    start = datetime.combine(datetime.today(), start_time)
    end = datetime.combine(datetime.today(), end_time)

    if end <= start:
        return 0

    duration = end - start
    return round(duration.total_seconds() / 3600, 2)


def calculate_job_cost(
    hours_on_site: float,
    number_of_operatives: int,
    vehicle_type: str,
    tool_type: str,
    tool_hours: float,
    lamp_qty: int,
    cable_qty: int,
    fuse_qty: int,
) -> dict:
    """Calculate estimated job cost breakdown."""
    labour_cost = hours_on_site * number_of_operatives * LABOUR_RATE_PER_HOUR
    vehicle_cost = hours_on_site * VEHICLE_RATES.get(vehicle_type, 0)
    tool_cost = tool_hours * TOOL_RATES.get(tool_type, 0)

    material_cost = (
        lamp_qty * MATERIAL_COSTS["Lamp Unit"]
        + cable_qty * MATERIAL_COSTS["Cable per metre"]
        + fuse_qty * MATERIAL_COSTS["Fuse"]
    )

    total_cost = labour_cost + vehicle_cost + tool_cost + material_cost

    return {
        "labour_cost": round(labour_cost, 2),
        "vehicle_cost": round(vehicle_cost, 2),
        "tool_cost": round(tool_cost, 2),
        "material_cost": round(material_cost, 2),
        "total_cost": round(total_cost, 2),
    }


st.set_page_config(
    page_title="Backpack Job Cost Capture",
    page_icon="",
    layout="centered",
)

init_db()

st.title("Backpack: Job Completion & Cost Capture")
st.caption("Prototype screen for Operative job submission and QS cost visibility")

with st.form("job_cost_form"):
    st.subheader("1. Job Details")

    job_reference = st.text_input("Job Reference", placeholder="e.g. SCC-2026-00124")
    asset_id = st.text_input("Asset ID", placeholder="e.g. SL-045892")
    location = st.text_input("Location", placeholder="e.g. Ipswich Road, Melton")

    job_type = st.selectbox(
        "Job Type",
        [
            "Streetlight Repair",
            "Inspection",
            "Column Replacement",
            "Emergency Callout",
        ],
    )

    st.subheader("2. Time on Site")

    arrival_time = st.time_input("Arrival Time", value=time(9, 0))
    departure_time = st.time_input("Departure Time", value=time(11, 30))
    number_of_operatives = st.number_input(
        "Number of Operatives",
        min_value=1,
        max_value=10,
        value=2,
    )

    hours_on_site = calculate_hours(arrival_time, departure_time)

    if hours_on_site == 0:
        st.warning("Departure time must be later than arrival time.")

    st.info(f"Calculated time on site: {hours_on_site} hours")

    st.subheader("3. Resources Used")

    vehicle_type = st.selectbox("Vehicle Used", list(VEHICLE_RATES.keys()))
    tool_type = st.selectbox("Plant/Tool Used", list(TOOL_RATES.keys()))

    tool_hours = st.number_input(
        "Tool Hours Used",
        min_value=0.0,
        max_value=24.0,
        value=hours_on_site,
        step=0.5,
    )

    st.subheader("4. Materials Used")

    lamp_qty = st.number_input("Lamp Units Used", min_value=0, value=1)
    cable_qty = st.number_input("Cable Used - metres", min_value=0, value=3)
    fuse_qty = st.number_input("Fuses Used", min_value=0, value=1)

    st.subheader("5. Work Completed")

    work_completed = st.text_area(
        "Description of Work Completed",
        placeholder="Describe the completed work, issues found, and any follow-up required.",
    )

    submitted = st.form_submit_button("Calculate and Save Job Cost")


if submitted:
    errors = []

    if not job_reference:
        errors.append("Job reference is required.")

    if not asset_id:
        errors.append("Asset ID is required.")

    if not location:
        errors.append("Location is required.")

    if not work_completed:
        errors.append("Work completed description is required.")

    if hours_on_site <= 0:
        errors.append("Valid arrival and departure times are required.")

    if errors:
        st.error("Please correct the following issues:")
        for error in errors:
            st.write(f"- {error}")
    else:
        cost = calculate_job_cost(
            hours_on_site=hours_on_site,
            number_of_operatives=number_of_operatives,
            vehicle_type=vehicle_type,
            tool_type=tool_type,
            tool_hours=tool_hours,
            lamp_qty=lamp_qty,
            cable_qty=cable_qty,
            fuse_qty=fuse_qty,
        )

        job_data = {
            "job_reference": job_reference,
            "asset_id": asset_id,
            "location": location,
            "job_type": job_type,
            "arrival_time": str(arrival_time),
            "departure_time": str(departure_time),
            "hours_on_site": hours_on_site,
            "number_of_operatives": number_of_operatives,
            "vehicle_type": vehicle_type,
            "tool_type": tool_type,
            "tool_hours": tool_hours,
            "lamp_qty": lamp_qty,
            "cable_qty": cable_qty,
            "fuse_qty": fuse_qty,
            "work_completed": work_completed,
            "labour_cost": cost["labour_cost"],
            "vehicle_cost": cost["vehicle_cost"],
            "tool_cost": cost["tool_cost"],
            "material_cost": cost["material_cost"],
            "total_cost": cost["total_cost"],
        }

        try:
            saved_job_id = save_job_submission(job_data)

            st.success(
                f"Job cost calculated and saved successfully. "
                f"Database ID: {saved_job_id}"
            )

            st.subheader("Estimated Cost Breakdown")

            col1, col2 = st.columns(2)

            with col1:
                st.metric("Labour Cost", f"£{cost['labour_cost']:,.2f}")
                st.metric("Vehicle Cost", f"£{cost['vehicle_cost']:,.2f}")

            with col2:
                st.metric("Tool/Plant Cost", f"£{cost['tool_cost']:,.2f}")
                st.metric("Material Cost", f"£{cost['material_cost']:,.2f}")

            st.divider()
            st.metric("Total Estimated Job Cost", f"£{cost['total_cost']:,.2f}")

            st.subheader("Job Summary for QS Review")

            st.write(
                {
                    "Database ID": saved_job_id,
                    "Job Reference": job_reference,
                    "Asset ID": asset_id,
                    "Location": location,
                    "Job Type": job_type,
                    "Arrival Time": str(arrival_time),
                    "Departure Time": str(departure_time),
                    "Hours on Site": hours_on_site,
                    "Number of Operatives": number_of_operatives,
                    "Vehicle": vehicle_type,
                    "Tool/Plant": tool_type,
                    "Work Completed": work_completed,
                    "Total Estimated Cost": f"£{cost['total_cost']:,.2f}",
                }
            )

        except Exception as error:
            st.error("The job cost was calculated, but it could not be saved.")
            st.exception(error)
