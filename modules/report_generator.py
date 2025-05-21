def generate_report(borrower_name, result, include_rejection=False):
    if result['eligible']:
        return f"Loan Approval Report for {borrower_name}\n\nStatus: ✅ Approved\nAmount: ₹{result['approved_amount']}\nTerms: {result['terms']}\nCollateral Provided: {result['collateral_flag']}"
    else:
        report = f"Loan Rejection Report for {borrower_name}\n\nStatus: ❌ Rejected\nReason: {result['reason']}\nCollateral Provided: {result['collateral_flag']}"
        if include_rejection:
            report += '\n\nSuggestions:\n• Improve CIBIL Score\n• Increase Income Documentation\n• Add Strong Collateral'
        return report
