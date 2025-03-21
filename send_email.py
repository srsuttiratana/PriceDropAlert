# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def send_mail(email_alert_list):
    for email_item in email_alert_list:
        message = Mail(
            from_email='sarahsuttiratana@gmail.com',
            to_emails='sarahsuttiratana@gmail.com',
            subject='Price Drop Alert',
            html_content='<strong>Sample html content</strong>')
        try:
            # Set the dynamic template ID
            price_difference = email_item.original_price - email_item.sale_price
            price_difference_percentage = (price_difference/email_item.original_price) * 100
            message.dynamic_template_data = {
                'Product_Name': email_item.product_name,
                'Product_URL': email_item.product_url,
                'Original_Price': email_item.currency + str(email_item.original_price),
                'Sale_Price': email_item.currency + str(email_item.sale_price),
                'Discount_Amount': '-' + email_item.currency + "{:.2f}".format(price_difference) + ' (' + "{:.2f}".format(price_difference_percentage) + '%)'
            }
            message.template_id = 'd-9058e6d5e3cb48609f015324fccffe27'
            sg = SendGridAPIClient(os.environ.get("SENDGRID_API_KEY"))
            response = sg.send(message)
            print(response.status_code)
            print(response.body)
            print(response.headers)
        except Exception as e:
            print(e.message)