import pytest
from parking_fee import parking_fee, find_slot, monthly_pass


# ---------------- parking_fee ----------------
def test_free_short_stay():
    assert parking_fee("car", 20, False, False) == 0


def test_unknown_vehicle():
    with pytest.raises(ValueError):
        parking_fee("bus", 60, False, False)


def test_negative_minutes():
    with pytest.raises(ValueError):
        parking_fee("car", -5, False, False)


def test_partial_hour_rounds_up_ev_and_lost_ticket():
    # 90 min -> 2 hours * 30 = 60, EV car -> 30, lost ticket -> +200
    assert parking_fee("car", 90, True, True) == 230


# ---------------- find_slot ----------------
def test_any_floor():
    assert find_slot("car", 5, False) == "any floor"


def test_slot_full():
    assert find_slot("car", 0, False) == "full"


def test_slot_disabled():
    assert find_slot("car", 5, True) == "ground floor"


def test_slot_truck():
    assert find_slot("truck", 5, False) == "basement"


# ---------------- monthly_pass ----------------
def test_bike_pass_resident():
    assert monthly_pass("bike", True) == 400


def test_car_pass():
    assert monthly_pass("car", False) == 1500


def test_pass_invalid_vehicle():
    with pytest.raises(ValueError):
        monthly_pass("truck", False)
