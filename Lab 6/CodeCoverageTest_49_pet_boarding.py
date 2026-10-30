
import pytest
from pet_boarding import boarding_fee, admission_ok, checkout_status


# ============================================================
# 1. BOARDING FEE TESTS
# ============================================================

@pytest.mark.parametrize(
    "pet_type,days,expected",
    [
        ("cat", 1, 0),
        ("dog", 2, 0),
        ("rabbit", 4, 0),
        ("cat", 4, 20),
        ("dog", 3, 30),
        ("rabbit", 5, 20),
    ],
)
def test_boarding_fee_normal_cases(pet_type, days, expected):
    assert boarding_fee(pet_type, days, False) == expected


@pytest.mark.parametrize(
    "pet_type,days,expected",
    [
        ("cat", 4, 0),
        ("dog", 3, 0),
        ("rabbit", 5, 20),
    ],
)
def test_boarding_fee_premium(pet_type, days, expected):
    assert boarding_fee(pet_type, days, True) == expected


def test_boarding_fee_unknown_pet():
    with pytest.raises(ValueError, match="unknown pet type"):
        boarding_fee("hamster", 5, False)


def test_boarding_fee_negative_days():
    with pytest.raises(ValueError, match="invalid days"):
        boarding_fee("cat", -1, False)


def test_boarding_fee_long_cat_stay():
    # 14 days - 3 included = 11 extra days.
    # Cat rate: 20 + 10 = 30 per extra day.
    assert boarding_fee("cat", 14, False) == 330


def test_boarding_fee_long_dog_stay():
    # 13 days - 2 included = 11 extra days.
    # Dog rate: 30 + 10 + 5 = 45 per extra day.
    assert boarding_fee("dog", 13, False) == 495


# ============================================================
# 2. ADMISSION TESTS
# ============================================================

@pytest.mark.parametrize(
    "age,vaccinations,is_senior,expected",
    [
        (4, 2, False, True),
        (4, 1, False, False),
        (1, 2, False, True),
        (0.5, 3, False, False),
        (5, 3, True, True),
        (5, 2, True, False),
        (0.5, 3, True, True),
    ],
)
def test_admission_cases(age, vaccinations, is_senior, expected):
    assert admission_ok(age, vaccinations, is_senior) is expected


# ============================================================
# 3. CHECKOUT STATUS TESTS
# ============================================================

@pytest.mark.parametrize(
    "is_long_stay,is_weekend,cutoff",
    [
        (False, False, 15),
        (True, False, 30),
        (False, True, 35),
        (True, True, 50),
    ],
)
def test_checkout_open_at_cutoff(is_long_stay, is_weekend, cutoff):
    assert checkout_status(
        cutoff, is_long_stay, is_weekend
    ) == "open"


@pytest.mark.parametrize(
    "is_long_stay,is_weekend,cutoff",
    [
        (False, False, 15),
        (True, False, 30),
        (False, True, 35),
        (True, True, 50),
    ],
)
def test_checkout_late(is_long_stay, is_weekend, cutoff):
    assert checkout_status(
        cutoff - 1, is_long_stay, is_weekend
    ) == "late"


@pytest.mark.parametrize(
    "is_long_stay,is_weekend,cutoff",
    [
        (False, False, 15),
        (True, False, 30),
        (False, True, 35),
        (True, True, 50),
    ],
)
def test_checkout_closed(is_long_stay, is_weekend, cutoff):
    assert checkout_status(
        cutoff - 16, is_long_stay, is_weekend
    ) == "closed"
