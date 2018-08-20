import boto3
import uuid
from faker import Faker
from datetime import datetime
from datetime import timedelta

# Create a table if a table doesn't exist
def create_table(table_name):
    dynamodb = boto3.client("dynamodb")
    tables = dynamodb.list_tables()["TableNames"]
    if table_name not in tables:
        table_name = dynamodb.create_table(
            TableName = table_name,
            KeySchema = [
                {
                    "AttributeName": "id",
                    "KeyType": "HASH"
                    },
                {
                    "AttributeName": "campaignName",
                    "KeyType": "RANGE"
                }
                ],
            AttributeDefinitions = [
                {
                    "AttributeName": "id",
                    "AttributeType": "S"
                },
                {
                    "AttributeName": "campaignName",
                    "AttributeType": "S"
                },
                ],
            ProvisionedThroughput = {
                "ReadCapacityUnits": 1,
                "WriteCapacityUnits": 1
                },
            )
        print("Table has been successfully created")

    else:
        print("{} table already exist in database".format(table_name))


# Check if table exist. If table exist, insert table records
def insert_records_into_table(table_name, dict_items):
    dynamodb = boto3.client('dynamodb')
    current_tables = dynamodb.list_tables().get("TableNames")
    if table_name in current_tables:
        dynamodb_resource = boto3.resource("dynamodb")
        table = dynamodb_resource.Table(table_name)
        table.put_item(
            Item = dict_items
            )
    else:
        print("{} table doesn't exist".format(table_name))

if __name__ == '__main__':
    create_table("campaigns")
    fake = Faker()
    number_of_day = 0
    for i in range(30):
        number_of_day += 2
        days = timedelta(days=number_of_day)
        campaign_start_date = datetime.now()
        campgaign_end_date = campaign_start_date + days
        insert_records_into_table('campaigns', {
            "id": str(uuid.uuid4()),
            "campaignName": fake.company(),
            "address": fake.address(),
            "campaignStartDate": str(campaign_start_date.date()),
            "campaignEndDate": str(campgaign_end_date.date()),
            "email": "momo.johnson1987@gmail.com"
        })
