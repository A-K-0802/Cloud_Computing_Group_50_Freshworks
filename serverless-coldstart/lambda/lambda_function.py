import json, os, uuid
from datetime import datetime, timezone
from decimal import Decimal
import boto3

table = boto3.resource("dynamodb").Table(os.environ["TABLE_NAME"])
_is_cold = True  # module-level: runs once per new execution environment

def _resp(code, body):
    return {"statusCode": code,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps(body)}

def lambda_handler(event, context):
    global _is_cold
    was_cold, _is_cold = _is_cold, False
    try:
        payload = json.loads(event.get("body") or "{}", parse_float=Decimal)
    except json.JSONDecodeError:
        return _resp(400, {"error": "Invalid JSON"})

    item = {
        "id": str(uuid.uuid4()),
        "created_at": datetime.now(timezone.utc).isoformat(),
        "payload": payload,
    }
    table.put_item(Item=item)
    return _resp(201, {"id": item["id"], "cold_start": was_cold})