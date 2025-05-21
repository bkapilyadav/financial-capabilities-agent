def evaluate_loan(cibil_score, income_texts, loan_amount, collateral_value):
    try:
        eligible_amount = 0
        score = int(cibil_score)

        if score < 650:
            return {
                "eligible": False,
                "reason": "Low CIBIL Score (<650)",
                "suggestion": "Improve credit score before reapplying."
            }

        if any("0 income" in text.lower() or "no income" in text.lower() for text in income_texts):
            return {
                "eligible": False,
                "reason": "No verifiable income in ITRs",
                "suggestion": "Submit clear ITR documents for income validation."
            }

        # Rule of thumb: eligible loan = 10x monthly income or based on collateral
        monthly_income = 40000  # Replace with income extraction logic
        eligible_amount = max(10 * monthly_income, collateral_value)

        if loan_amount > eligible_amount:
            return {
                "eligible": False,
                "reason": f"Requested loan ({loan_amount}) exceeds eligible limit ({eligible_amount})",
                "suggestion": "Request lower amount or add collateral."
            }

        return {
            "eligible": True,
            "eligible_amount": eligible_amount,
            "terms": {
                "tenure_months": 24,
                "interest_rate": "14-18% based on risk"
            }
        }

    except Exception as e:
        return {
            "eligible": False,
            "reason": f"Evaluation error: {str(e)}"
        }
