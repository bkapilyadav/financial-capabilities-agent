import streamlit as st
from PIL import Image
import pytesseract
import io
from PyPDF2 import PdfReader
import os

from utils.ocr_parser import extract_text_from_pdf, extract_text_from_image
from utils.loan_evaluator import evaluate_loan
from utils.report_generator import generate_report
from modules.financial_analyzer import analyze_financials

st.set_page_config(page_title='Financial Capabilities Assessment AI Agent')
st.title('💼 Financial Capabilities Assessment AI Agent')
st.markdown('---')

st.markdown('### 📋 Please upload the required borrower documents:')

# Borrower Info
full_name = st.text_input('🧍 Full Name')
address = st.text_area('🏠 Address (as per Govt ID)')
pan_card = st.text_input('🆔 PAN Card Number')
loan_amount = st.number_input('💰 Requested Loan Amount', step=1000)
loan_purpose = st.text_input('📌 Purpose of Loan')

# File Uploads
st.markdown('---')
st.markdown('### 📎 Upload Documents')

cibil_file = st.file_uploader('📄 Upload Latest CIBIL Report (PDF/Image)', type=['pdf', 'png', 'jpg', 'jpeg'])
itr_files = st.file_uploader('📑 Upload ITRs for Last 3 Years (PDFs or Images)', type=['pdf','png', 'jpg', 'jpeg'], accept_multiple_files=True)
collateral = st.text_input('🏡 Any Surety (Gold, Land, Property)?')

# Optional CIBIL score input
cibil_score = st.number_input('💯 Enter Estimated CIBIL Score', min_value=300, max_value=900, step=1)

# OpenAI API Key input (Streamlit Cloud secrets preferred instead)
import streamlit as st

openai_api_key = st.secrets["OPENAI_API_KEY"]

# CIBIL Report Parsing
cibil_text = ""
if cibil_file is not None:
    if cibil_file.type == 'application/pdf':
        cibil_text = extract_text_from_pdf(cibil_file)
    else:
        cibil_text = extract_text_from_image(cibil_file)

    st.markdown('---')
    st.subheader('📊 CIBIL Report Text Extracted')
    st.text_area('Extracted Text:', cibil_text, height=200)

# ITR Report Parsing
itr_texts = []
if itr_files:
    for itr_file in itr_files:
        file_bytes = itr_file.read()
        if itr_file.type == "application/pdf":
            pdf_reader = PdfReader(io.BytesIO(file_bytes))
            text = ""
            for page in pdf_reader.pages:
                if page.extract_text():
                    text += page.extract_text()
        else:
            img = Image.open(io.BytesIO(file_bytes))
            text = pytesseract.image_to_string(img)
        itr_texts.append(text)

# Loan Eligibility Assessment
if st.button("🧾 Assess Loan Eligibility"):
    with st.spinner("Evaluating..."):
        collateral_value = 500000  # You can improve this with input or estimation
        decision = evaluate_loan(
            cibil_score,
            itr_texts,
            loan_amount,
            collateral_value
        )
        report = generate_report(full_name, decision)
        st.text_area("📋 Assessment Report", value=report, height=300)

    st.markdown("⚠️ **Note**: All data is confidential and used only for eligibility evaluation.")
    st.subheader('🧾 ITR Data Summary')
    for idx, text in enumerate(itr_texts):
        st.text_area(f'ITR Year {idx+1}', text[:800], height=150)

# Financial Capability Analyzer
if st.button('🧠 Run Financial Eligibility Check'):
    if cibil_file and itr_files:
        result = analyze_financials(cibil_text, itr_texts, collateral, loan_amount)

        st.markdown('---')
        if result['eligible']:
            st.success('✅ Borrower is Eligible')
            st.markdown(f"**Approved Amount:** ₹{result['approved_amount']}")
            st.markdown(f"**Terms:** {result['terms']}")
        else:
            st.error('❌ Borrower is Not Eligible')
            st.markdown(f"**Reason:** {result['reason']}")

        # Final Report
        report_text = generate_report(full_name, result, include_rejection=True)
        st.markdown('---')
        st.subheader('📄 Final AI Assessment Report')
        st.text_area('Decision Report:', report_text, height=300)
        st.download_button('⬇️ Download Report', data=report_text, file_name='loan_report.txt')

    else:
        st.warning('⚠️ Please upload both CIBIL and ITRs.')

