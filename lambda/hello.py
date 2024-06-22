def handler(event, context):
    print("request:", event)
    return {"statusCode": 200, "body": f"Hello, CDK! You've hit {event['path']}\n"}
