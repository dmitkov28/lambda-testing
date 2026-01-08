def lambda_handler(event: dict, context: dict):
    try:
        x = int(event.get("x", 0))
        y = int(event.get("y", 0))
        result = x + y
        return {"statusCode": 200, "result": result}
    except ValueError:
        return {"statusCode": 400, "error": "invalid input"}
