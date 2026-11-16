import pytest
from parking_fee import parking_fee, find_slot, monthly_pass


# ================= parking_fee =================
# vehicle validity (True / False branch)
def test_unknown_vehicle():
    with pytest.raises(ValueError):
        parking_fee("bus", 60, False, False)


# minutes < 0 (True / False branch)
def test_negative_minutes():
    with pytest.raises(ValueError):
        parking_fee("car", -5, False, False)


# minutes <= 30 (True branch) incl. boundary value
def test_free_short_stay():
    assert parking_fee("car", 20, False, False) == 0


def test_free_boundary_30_minutes():
    assert parking_fee("car", 30, False, False) == 0


# minutes <= 30 (False) and minutes % 60 != 0 (False): exact hours
def test_exact_hour_no_roundup():
    assert parking_fee("car", 60, False, False) == 30


def test_just_over_free_boundary_31_minutes():
    assert parking_fee("car", 31, False, False) == 30


# minutes % 60 != 0 (True): partial hour rounds up
def test_partial_hour_rounds_up():
    assert parking_fee("bike", 90, False, False) == 20


# every vehicle rate
def test_truck_rate():
    assert parking_fee("truck", 120, False, False) == 120


# is_ev and vehicle != "truck": True / False via is_ev / False via truck
def test_ev_car_half_price():
    assert parking_fee("car", 120, True, False) == 30


def test_ev_bike_half_price():
    assert parking_fee("bike", 120, True, False) == 10


def test_ev_truck_no_discount():
    assert parking_fee("truck", 120, True, False) == 120


def test_non_ev_car_no_discount():
    assert parking_fee("car", 120, False, False) == 60


# lost_ticket (True / False)
def test_lost_ticket_penalty():
    assert parking_fee("car", 20, False, True) == 200


def test_ev_and_lost_ticket_combined():
    assert parking_fee("car", 90, True, True) == 230


# ================= find_slot =================
def test_slot_full():
    assert find_slot("car", 0, False) == "full"


def test_slot_negative_free_slots():
    assert find_slot("car", -1, False) == "full"


def test_slot_disabled():
    assert find_slot("car", 5, True) == "ground floor"


def test_slot_truck():
    assert find_slot("truck", 5, False) == "basement"


def test_any_floor():
    assert find_slot("car", 5, False) == "any floor"


def test_slot_full_beats_disabled():
    assert find_slot("truck", 0, True) == "full"


# ================= monthly_pass =================
def test_bike_pass_non_resident():
    assert monthly_pass("bike", False) == 500


def test_bike_pass_resident():
    assert monthly_pass("bike", True) == 400


def test_car_pass_non_resident():
    assert monthly_pass("car", False) == 1500


def test_car_pass_resident():
    assert monthly_pass("car", True) == 1200


def test_pass_invalid_vehicle():
    with pytest.raises(ValueError):
        monthly_pass("truck", False)
