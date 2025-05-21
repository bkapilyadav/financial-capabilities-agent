def generate_report(name, decision):
    if decision["eligible"]:
        return f"""
📄 Loan Approval Report

Borrower: {name}
Status: ✅ Approved
Eligible Amount: ₹{decision['eligible_amount']}
Suggested Terms:
- Tenure: {decision['terms']['tenure_months']} months
- Interest Rate: {decision['terms']['interest_rate']}
"""
    else:
        suggestion = decision.get('suggestion', 'Please consult a financial advisor.')
        return f"""
📄 Loan Rejection Report

Borrower: {name}
Status: ❌ Rejected
Reason: {decision['reason']}
Suggestion: {suggestion}
"""
