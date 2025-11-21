import json
from pathlib import Path

def handler(request):
    if request.method != "POST":
        return {"error": "POST only"}

    data = request.json()

    user_id = str(data.get("user_id"))
    crystals = data.get("crystals")

    if not user_id or crystals is None:
        return {"error": "invalid data"}

    db_path = Path(__file__).resolve().parents[1] / "db.json"

    if not db_path.exists():
        db_path.write_text("{}")

    db = json.loads(db_path.read_text())

    db[user_id] = crystals

    db_path.write_text(json.dumps(db, indent=2))

    return {"status": "saved"}
