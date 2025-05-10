import smtplib
from email.message import EmailMessage
from fpdf import FPDF
import os

# Email map for product heads
email_map = {
    "HL": "@example.com",
    "PL": "pl_person@example.com",
    "INSURANCE": "insurance_person@example.com"
}

# Questionnaire
def get_lead_details():
    product = input("Enter product type (HL/PL/Insurance): ").strip().upper()

    details = {"product": product}
    details["name"] = input("Enter lead's name: ")
    details["phone"] = input("Enter phone number: ")

    if product == "HL":
        details["monthly_income"] = input("Enter monthly income: ")
        details["property_type"] = input("Enter property type: ")
        details["loan_amount"] = input("Enter loan amount: ")

    elif product == "PL":
        details["company_name"] = input("Enter company name: ")
        details["salary_type"] = input("Salary credit type (Bank/Cash): ")
        details["loan_amount"] = input("Enter required loan amount: ")

    elif product == "INSURANCE":
        details["insurance_type"] = input("Type of Insurance (Health/Life/Vehicle): ")
        details["sum_assured"] = input("Enter sum assured: ")
        details["age"] = input("Enter age: ")

    else:
        print("Invalid product type.")
        return None

    return details

# PDF generation
def generate_pdf(details, filename="lead_details.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Lead Details - {details['product']}", ln=True, align='C')
    pdf.ln(10)

    for key, value in details.items():
        if key != "product":
            label = key.replace('_', ' ').capitalize()
            pdf.cell(200, 10, txt=f"{label}: {value}", ln=True)

    pdf.output(filename)
    return filename

# Email sending
def send_email_with_attachment(to_email, subject, body, attachment_path):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = 'your_email@example.com'
    msg['To'] = to_email
    msg.set_content(body)

    # Attach PDF
    with open(attachment_path, 'rb') as f:
        file_data = f.read()
        file_name = os.path.basename(attachment_path)
    msg.add_attachment(file_data, maintype='application', subtype='pdf', filename=file_name)

    # Send
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login('saisuchithgandla@example.com', 'your_password')  # Use App Password if Gmail
        smtp.send_message(msg)

# Main logic
if __name__ == "__main__":
    lead = get_lead_details()
    if lead:
        product = lead["product"]
        recipient = email_map.get(product)
        if recipient:
            pdf_file = generate_pdf(lead)
            email_body = f"Please find the attached lead details for {product}."
            send_email_with_attachment(recipient, f"New {product} Lead", email_body, pdf_file)
            print("✅ Email with PDF sent successfully.")
            os.remove(pdf_file)  # Optional: clean up
        else:
            print("❌ No email found for this product.")