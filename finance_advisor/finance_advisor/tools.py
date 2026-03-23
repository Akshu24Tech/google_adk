import requests
from typing import List, Dict, Union, Optional

def calculate_monthly_budget(income: float, expenses: list[Dict[str, Union[str, float]]]) -> Dict[str, float]:
    """
    Calculate the monthly budget based on income and a list of expenses.
    
    Args:
        income: Total monthly income.
        expenses: A list of dicts, each with "description", "amount", and "category".
        
    Returns:
        A dictionary containing total_expenses, remaining_budget, and savings_rate.
    """
    total_expenses = sum(float(e["amount"]) for e in expenses)
    remaining = income - total_expenses
    savings_rate = (remaining / income * 100) if income > 0 else 0
    
    return {
        "income": round(float(income), 2),
        "total_expenses": round(total_expenses, 2),
        "remaining_budget": round(remaining, 2),
        "savings_rate_percent": round(savings_rate, 2)
    }

def convert_currency(amount: float, from_currency: str, to_currency: str) -> Dict[str, Union[float, str]]:
    """
    Convert an amount from one currency to another using a free exchange rate API.
    
    Args:
        amount: The amount to convert.
        from_currency: 3-letter currency code (e.g., USD, INR).
        to_currency: 3-letter currency code (e.g., EUR, GBP).
        
    Returns:
        A dictionary with the converted amount and the exchange rate used.
    """
    try:
        from_currency = from_currency.upper()
        to_currency = to_currency.upper()
        url = f"https://api.exchangerate-api.com/v4/latest/{from_currency}"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            rate = data["rates"].get(to_currency)
            if rate:
                converted = amount * rate
                return {
                    "from_currency": from_currency,
                    "to_currency": to_currency,
                    "amount": round(amount, 2),
                    "converted_amount": round(converted, 2),
                    "exchange_rate": rate
                }
            return {"error": f"Currency code {to_currency} not found."}
        return {"error": "Failed to fetch exchange rates."}
    except Exception as e:
        return {"error": str(e)}

def calculate_compound_interest(
    principal: float, 
    annual_interest_rate: float, 
    years: int, 
    monthly_contribution: float = 0
) -> Dict[str, float]:
    """
    Calculate compound interest with optional monthly contributions.
    
    Args:
        principal: Initial amount investment.
        annual_interest_rate: Annual rate (as percentage, e.g., 5 for 5%).
        years: Investment duration in years.
        monthly_contribution: Monthly amount added to the investment.
        
    Returns:
        A dictionary with the final balance and total interest earned.
    """
    rate = (annual_interest_rate / 100) / 12
    months = int(years) * 12
    
    # Formula for compound interest with monthly contributions:
    # A = P(1+r)^n + PMT * [((1+r)^n - 1) / r]
    
    future_value_principal = principal * (1 + rate) ** months
    
    if rate > 0:
        future_value_contributions = monthly_contribution * (((1 + rate) ** months - 1) / rate)
    else:
        future_value_contributions = monthly_contribution * months
        
    final_balance = future_value_principal + future_value_contributions
    total_contributions = principal + (monthly_contribution * months)
    total_interest = final_balance - total_contributions
    
    return {
        "initial_investment": round(float(principal), 2),
        "total_contributions": round(total_contributions, 2),
        "total_interest_earned": round(total_interest, 2),
        "final_balance": round(final_balance, 2)
    }
