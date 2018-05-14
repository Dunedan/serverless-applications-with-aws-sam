def handler(event, context):
    return {
        "headers": {"content-type": "text/plain"},
        "body": "Hello World"
    }
