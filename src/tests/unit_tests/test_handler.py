from src.main import lambda_handler


def test_handler_happy_path():
    test_event = {"x": 1, "y": 1}
    result = lambda_handler(event=test_event, context={})
    assert result["result"] == 2


def test_handler_invalid_input_type():
    test_event = {"x": "1", "y": 1}
    result = lambda_handler(event=test_event, context={})
    assert result["result"] == 2

    test_event = {"x": "1", "y": "1"}
    result = lambda_handler(event=test_event, context={})
    assert result["result"] == 2

    test_event = {"x": "1"}
    result = lambda_handler(event=test_event, context={})
    assert result["result"] == 1


def test_handler_no_input():
    result = lambda_handler(event={}, context={})
    assert result["result"] == 0


def test_handler_invalid_input():
    test_event = {"x": "invalid", "y": "invalid"}
    result = lambda_handler(event=test_event, context={})
    assert result["statusCode"] == 400
    assert result["error"] == "invalid input"
