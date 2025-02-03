import streamlit as st

# Tax slabs as per the new regime (2025-26)
TAX_SLABS = [
    (400000, 0.05),  # 5% for ₹4-8 lakh
    (400000, 0.10),  # 10% for ₹8-12 lakh
    (400000, 0.15),  # 15% for ₹12-16 lakh
    (400000, 0.20),  # 20% for ₹16-20 lakh
    (400000, 0.25),  # 25% for ₹20-24 lakh
]
EXCESS_TAX_RATE = 0.30  # 30% for income above ₹24 lakh

STANDARD_DEDUCTION = 75000
TAX_FREE_LIMIT = 1275000  # ₹12.75 lakh (including ₹75,000 deduction)

def calculate_income_tax(income):
    """
    Computes tax based on the new tax regime:
    - No tax for income up to ₹12.75 lakh.
    - Normal tax slabs apply beyond ₹12.75 lakh.
    - Marginal relief applies for incomes slightly above ₹12.75 lakh.
    """
    taxable_income = max(0, income - STANDARD_DEDUCTION)

    # No tax if income is within ₹12.75 lakh
    if taxable_income <= 1200000:
        return 0

    # Compute normal tax for income above ₹12.75 lakh
    tax = 0
    remaining_income = taxable_income - 1200000  # Tax applies beyond ₹12.75 lakh

    for slab, rate in TAX_SLABS:
        if remaining_income > slab:
            tax += slab * rate
            remaining_income -= slab
        else:
            tax += remaining_income * rate
            remaining_income = 0
            break

    if remaining_income > 0:
        tax += remaining_income * EXCESS_TAX_RATE

    # Apply marginal relief for incomes slightly above ₹12.75 lakh
    if taxable_income > 1200000:
        excess_income = taxable_income - 1200000
        if tax > excess_income:
            tax = excess_income

    return round(tax, 2)

# Streamlit UI
st.title("Income Tax Calculator (New Tax Regime 2025-26)")

income = st.number_input("Enter Your Annual Salary (₹):", min_value=0, step=10000)

if st.button("Calculate Tax"):
    tax = calculate_income_tax(income)
    st.write(f"### Your Tax Payable: ₹{tax:,.2f}")

# Footer with creator's name
st.markdown("<br><br><b style='font-size:16px;'>Created by Paramjeet Gusain</b>", unsafe_allow_html=True)
