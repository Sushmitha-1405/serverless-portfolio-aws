import json
import os
import boto3

ses = boto3.client("ses", region_name="ap-southeast-2")
EMAIL = os.environ["EMAIL"]


def reply(status, message):
    return {
        "statusCode": status,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"message": message}),
    }


def lambda_handler(event, context):
    try:
        data = json.loads(event.get("body") or "{}")
    except json.JSONDecodeError:
        return reply(400, "Invalid request")

    name = str(data.get("name", "")).replace("\n", " ").strip()
    sender = str(data.get("email", "")).replace("\n", " ").strip()
    message = str(data.get("message", "")).strip()

    if not name or not sender or not message:
        return reply(400, "All fields are required")
    if "@" not in sender or len(name) > 100 or len(sender) > 200 or len(message) > 2000:
        return reply(400, "Invalid input")

    try:
        ses.send_email(
            Source=EMAIL,
            Destination={"ToAddresses": [EMAIL]},
            ReplyToAddresses=[sender],
            Message={
                "Subject": {"Data": "Portfolio message from " + name},
                "Body": {"Text": {"Data": "From: " + name + " <" + sender + ">\n\n" + message}},
            },
        )
    except Exception as e:
        print(e)
        return reply(500, "Could not send message")

    return reply(200, "Message sent")
