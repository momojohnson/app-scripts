
from datetime import datetime
from datetime import timedelta

import boto3
import sendgrid
import os
from sendgrid.helpers.mail import *


dynamdb = boto3.resource('dynamodb')
table = dynamdb.Table('campaigns')
data = table.scan()

# Send email to a paritcular user base on certain criteria
def send_email(client_email):
    sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('API_KEY'))
    from_email = Email("mo12g13@gmail.com")
    to_email = Email(client_email)
    subject = "Notification Regarding Your Campaign with Dow Jones"
    content = Content("text/plain", "This is a test notification regarding your campaign with Dow Jones Ads")
    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    print(response.status_code)
    print(response.body)
    print("Email Sent")

# Check notification status and send an email to a particular user
def check_notification_status():
    for item in range(len(data.get("Items"))):
        start_date = datetime.strptime(data.get("Items")[item].get("campaignStartDate"), '%Y-%m-%d').date()
        end_date = datetime.strptime(data.get("Items")[item].get("campaignEndDate"), '%Y-%m-%d').date()
        substracted_days = timedelta(days=7)
        todays_date = datetime.today().date()
        remaining_days = todays_date + substracted_days

        if remaining_days >= end_date:
            print(str(remaining_days) +"        "+ str(end_date))
            print("This campaign ends in seven days or has passed it ends date")
            print(todays_date-substracted_days)

        # print(start_date < end_date)
        # if data.get("Items")[item].get()
        # print(data.get("Items")[item].get('email'))
        # send_email(data.get("Items")[item].get('email'))


if __name__ == '__main__':
    check_notification_status()
    # send_email('momo.johnson1987@gmail.com')
