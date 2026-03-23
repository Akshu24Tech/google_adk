import sys
import os

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from finance_advisor.tools import calculate_monthly_budget, calculate_compound_interest, convert_currency

def test_calculate_monthly_budget():
    income = 5000
    expenses = [
        {"description": "Rent", "amount": 2000, "category": "Housing"},
        {"description": "Food", "amount": 500, "category": "Utilities"}
    ]
    result = calculate_monthly_budget(income, expenses)
    print("Budget Result:", result)
    assert result["total_expenses"] == 2500
    assert result["remaining_budget"] == 2500
    assert result["savings_rate_percent"] == 50.0

def test_calculate_compound_interest():
    principal = 1000
    rate = 5
    years = 10
    contribution = 100
    result = calculate_compound_interest(principal, rate, years, contribution)
    print("Compound Interest Result:", result)
    assert result["final_balance"] > 1000
    assert result["total_interest_earned"] > 0

def test_convert_currency():
    # Note: This tool makes an external API call
    amount = 100
    from_curr = "USD"
    to_curr = "INR"
    result = convert_currency(amount, from_curr, to_curr)
    print("Currency Result:", result)
    if "error" not in result:
        assert result["converted_amount"] > 0
        assert result["from_currency"] == "USD"
    else:
        print("Skipping assertion due to API error:", result["error"])

if __name__ == "__main__":
    print("Running tests...")
    test_calculate_monthly_budget()
    test_calculate_compound_interest()
    test_convert_currency()
    print("All tests passed!")
