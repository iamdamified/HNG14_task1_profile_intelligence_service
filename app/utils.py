import uuid, time
from datetime import datetime, timezone

def uuid7():
    ts = int(time.time() * 1000)
    rand = uuid.uuid4().int >> 80
    return str(uuid.UUID(int=(ts << 80) | rand))

def utc_now():
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

def age_group(age: int) -> str:
    if age <= 12:
        return "child"
    if age <= 19:
        return "teenager"
    if age <= 59:
        return "adult"
    return "senior"