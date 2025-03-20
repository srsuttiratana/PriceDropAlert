# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

message = Mail(
    from_email='sarahsuttiratana@gmail.com',
    to_emails='sarahsuttiratana@gmail.com',
    subject='Price Drop Alert',
    html_content='<strong>Sample html content</strong>')
try:
    # Set the dynamic template ID
    message.dynamic_template_data = {
        'Product_Name': 'Ribbed Cropped Bra Top',
        'Product_URL': 'https://www.uniqlo.com/us/en/products/E473983-000/00?colorDisplayCode=02&sizeDisplayCode=003',
        'Original_Price': '29.90',
        'Sale_Price': '14.90',
        'Discount_Amount': '15.00'
    }
    message.template_id = 'd-9058e6d5e3cb48609f015324fccffe27'
    sg = SendGridAPIClient(os.environ.get("SENDGRID_API_KEY"))
    response = sg.send(message)
    print(response.status_code)
    print(response.body)
    print(response.headers)
except Exception as e:
    print(e.message)