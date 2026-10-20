import json
import boto3

table = boto3.resource("dynamodb").Table("portfolio-visitors")

def lambda_handler(event, context):
    result = table.update_item(
        Key={"id": "visitors"},
        UpdateExpression="ADD visit_count :inc",
        ExpressionAttributeValues={":inc": 1},
        ReturnValues="UPDATED_NEW",
    )
    count = int(result["Attributes"]["visit_count"])
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"count": count}),
    }
