#!/usr/bin/env python3
"""
create_dynamodb_table.py

Creates a DynamoDB table named 'Employees' with primary key 'emp_id'.
This script will also insert a sample item (emp_id, phone_number, email)
to demonstrate types: phone_number as Number and email as String.

Usage:
    . .venv/bin/activate
    python create_dynamodb_table.py

Note: DynamoDB is schemaless for non-key attributes; only the key is
defined in the table schema. Uniqueness is enforced for the primary key.
"""
import time
import boto3
import botocore

TABLE_NAME = "Employees"
SAMPLE_ITEM = {
    'emp_id': 'E001',
    # DynamoDB number values are sent as strings when using the low-level client
    'phone_number': 1234567890,
    'email': 'user@example.com',
}


def table_exists(dynamodb_client, name: str) -> bool:
    try:
        dynamodb_client.describe_table(TableName=name)
        return True
    except botocore.exceptions.ClientError as e:
        code = e.response.get('Error', {}).get('Code')
        if code in ('ResourceNotFoundException', 'ValidationException'):
            return False
        raise


def create_table(dynamodb_client, name: str):
    if table_exists(dynamodb_client, name):
        print(f"Table '{name}' already exists.")
        return

    print(f"Creating table '{name}' (primary key: emp_id (S))...")
    response = dynamodb_client.create_table(
        TableName=name,
        KeySchema=[
            { 'AttributeName': 'emp_id', 'KeyType': 'HASH' },
        ],
        AttributeDefinitions=[
            { 'AttributeName': 'emp_id', 'AttributeType': 'S' },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5,
        }
    )
    print('Create table API accepted, waiting for ACTIVE status...')
    waiter = dynamodb_client.get_waiter('table_exists')
    waiter.wait(TableName=name)
    print(f"Table '{name}' is now ACTIVE.")


def put_sample_item(dynamodb_client, name: str, item: dict):
    print('Inserting sample item (will use conditional write to avoid overwrite)...')
    # Convert numeric Python types to DynamoDB expected format via boto3's high-level resource
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(name)
    try:
        table.put_item(
            Item={
                'emp_id': item['emp_id'],
                'phone_number': item['phone_number'],
                'email': item['email'],
            },
            ConditionExpression='attribute_not_exists(emp_id)'
        )
        print('Sample item inserted successfully.')
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
            print('Sample item already exists (not overwritten).')
        else:
            raise


def main():
    # Use the default boto3 client configuration (reads ~/.aws/credentials or env vars)
    dynamodb_client = boto3.client('dynamodb')

    try:
        create_table(dynamodb_client, TABLE_NAME)
        put_sample_item(dynamodb_client, TABLE_NAME, SAMPLE_ITEM)
        print('Done.')
    except botocore.exceptions.ClientError as e:
        print('AWS ClientError:', e)
    except Exception as e:
        print('Error:', type(e).__name__, e)


if __name__ == '__main__':
    main()
