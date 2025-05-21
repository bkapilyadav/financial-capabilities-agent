def analyze_financials(cibil_text, itr_texts, collateral, requested_amount):
    result = {}

    # Placeholder CIBIL check logic
    if 'poor' in cibil_text.lower():
        result['eligible'] = False
        result['reason'] = 'Low CIBIL score detected in report.'
    elif any('default' in t.lower() for t in itr_texts):
        result['eligible'] = False
        result['reason'] = 'Defaults or irregularities in ITR records.'
    else:
        result['eligible'] = True
        result['approved_amount'] = min(requested_amount, 500000)  # cap at 5 lakhs for demo
        result['terms'] = 'Repayable in 12 months at 10% interest.'

    result['collateral_flag'] = bool(collateral.strip())
    return result
