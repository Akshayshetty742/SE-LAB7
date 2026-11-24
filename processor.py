import re

# Category mapping for Indian Permanent Account Numbers (4th character)
CATEGORIES = {
    "P": "Individual",
    "C": "Company",
    "H": "HUF",
    "F": "Firm"
}

# Lab 6 Minimum Income Thresholds
MIN_INCOME = {
    "salaried": 25000,
    "self_employed": 40000
}


def parse_income(income):
    """
    Parses monthly income string (e.g. '50,000') into an integer.
    Validates input type, format, length, and non-negativity.
    Enforces strictly ASCII decimal digits (0-9) to prevent Unicode digit ValueError crashes (e.g., '¹').
    Returns parsed integer if valid, or None if invalid.
    """
    if not isinstance(income, str):
        return None
    
    cleaned = income.strip().replace(',', '')
    if not cleaned or not re.match(r'^[0-9]+$', cleaned) or len(cleaned) > 15:
        return None
    
    val = int(cleaned)
    if val < 0:
        return None
    return val


def monthly_emi(details):
    """
    Calculates monthly EMI from comma-separated string 'principal,rate,years'.
    Validates formatting, numerical bounds, and handles zero-rate & overflow safely.
    Returns rounded EMI float (2 decimal places) or None if invalid.
    """
    if not isinstance(details, str):
        return None
    
    parts = [p.strip() for p in details.split(',')]
    if len(parts) != 3:
        return None
    
    p_str, r_str, y_str = parts
    num_pattern = r'^[0-9]+(\.[0-9]+)?$'
    if not (re.match(num_pattern, p_str) and re.match(num_pattern, r_str) and re.match(num_pattern, y_str)):
        return None
    
    principal = float(p_str)
    rate = float(r_str)
    years = float(y_str)
    
    # Domain constraints: realistic ranges to prevent overflows and division by zero
    if principal <= 0 or principal > 1e12:
        return None
    if rate < 0 or rate > 100:
        return None
    if years <= 0 or years > 50:
        return None
    
    n = int(years * 12)
    if n <= 0:
        return None
    
    # 0% interest loan case
    if rate == 0:
        return round(principal / n, 2)
    
    r = rate / 1200.0
    factor = (1.0 + r) ** n
    denom = factor - 1.0
    if denom <= 0:
        return None
    
    emi = (principal * r * factor) / denom
    return round(emi, 2)


def pan_category(pan):
    """
    Identifies PAN category from 4th character of PAN string.
    Validates type, length, and category membership safely.
    Returns category name string or None if invalid.
    """
    if not isinstance(pan, str):
        return None
    
    cleaned = pan.strip()
    if len(cleaned) < 4 or len(cleaned) > 20:
        return None
    
    category_char = cleaned[3].upper()
    return CATEGORIES.get(category_char, None)


# --- Lab 6 Functions Preserved ---

def credit_band(score):
    if not isinstance(score, (int, float)) or isinstance(score, bool):
        raise ValueError("invalid score")
    if score < 300 or score > 900:
        raise ValueError("invalid score")
    if score >= 750:
        return "excellent"
    elif score >= 650:
        return "good"
    elif score >= 550:
        return "fair"
    return "poor"


def is_eligible(age, income, employment, score):
    if employment not in MIN_INCOME:
        raise ValueError("unknown employment")
    if not isinstance(age, (int, float)) or age < 21 or age > 60:
        return False
    if not isinstance(income, (int, float)) or income < MIN_INCOME[employment]:
        return False
    if credit_band(score) == "poor":
        return False
    return True


def interest_rate(score, employment, has_collateral):
    band = credit_band(score)
    if band == "excellent":
        rate = 8
    elif band == "good":
        rate = 10
    else:
        rate = 13
    if employment == "self_employed":
        rate += 1
    if has_collateral:
        rate -= 2
    return rate


def main():
    print("==== Running parse_income ====")
    user_input = input("Enter monthly income (e.g. 50,000): ")
    result = parse_income(user_input)
    print("Income:", result if result is not None else "Invalid income format")

    print("\n==== Running monthly_emi ====")
    user_input = input("Enter principal,rate,years (e.g. 500000,10,5): ")
    result = monthly_emi(user_input)
    print("Monthly EMI:", result if result is not None else "Invalid EMI details")

    print("\n==== Running pan_category ====")
    user_input = input("Enter a PAN number (e.g. ABCPE1234F): ")
    result = pan_category(user_input)
    print("PAN Category:", result if result is not None else "Invalid PAN number")


if __name__ == "__main__":
    main()
