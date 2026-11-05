
import math


def parse_booking(text):
    if not isinstance(text, str):
        return None

    parts = text.split(':')
    if len(parts) != 2:
        return None

    pet, days = parts

    if not pet.strip():
        return None

    try:
        days = float(days.strip())
    except ValueError:
        return None

    if not math.isfinite(days) or days <= 0:
        return None

    return pet.strip().title(), days


def stay_average(days_csv):
    if not isinstance(days_csv, str):
        return None

    parts = days_csv.split(',')

    if not parts or any(not r.strip() for r in parts):
        return None

    try:
        values = [int(r.strip()) for r in parts]
    except ValueError:
        return None

    if any(value <= 0 for value in values):
        return None

    return sum(values) // len(values)


def payable_fee(text):
    if not isinstance(text, str):
        return None

    parts = text.split('|')
    if len(parts) != 2:
        return None

    try:
        fee = float(parts[0].strip())
        discount = float(parts[1].strip())
    except ValueError:
        return None

    if not math.isfinite(fee) or not math.isfinite(discount):
        return None

    if fee < 0 or discount < 0:
        return None

    total = fee * 1.18 - discount

    return max(total, 0)


def main():
    print("==== Running parse_booking ====")
    user_input = input("Enter pet:days (e.g. dog:5): ")
    result = parse_booking(user_input)
    print("Pet and Days:", result)

    print("\n==== Running stay_average ====")
    user_input = input("Enter stay lengths in days as CSV (e.g. 2,5,7): ")
    result = stay_average(user_input)
    print("Average Stay:", result)

    print("\n==== Running payable_fee ====")
    user_input = input("Enter fee|discount (e.g. 1500|100): ")
    result = payable_fee(user_input)
    print("Payable Fee:", result)


if __name__ == "__main__":
    main()
