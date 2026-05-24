from datetime import time
from src.app import calculate_hours, calculate_job_cost


def test_calculate_hours_valid_time_range():
    result = calculate_hours(time(9, 0), time(11, 30))
    assert result == 2.5


def test_calculate_hours_invalid_time_range():
    result = calculate_hours(time(12, 0), time(10, 0))
    assert result == 0


def test_calculate_job_cost():
    result = calculate_job_cost(
        hours_on_site=2.5,
        number_of_operatives=2,
        vehicle_type="Van",
        tool_type="Cherry Picker",
        tool_hours=2.5,
        lamp_qty=1,
        cable_qty=3,
        fuse_qty=1,
    )

    assert result["labour_cost"] == 150.00
    assert result["vehicle_cost"] == 37.50
    assert result["tool_cost"] == 112.50
    assert result["material_cost"] == 65.00
    assert result["total_cost"] == 365.00
