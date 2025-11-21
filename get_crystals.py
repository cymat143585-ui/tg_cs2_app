import json
from pathlib import Path

def handler(request):
    user_id = request.query_params.get("user_id")

    if not user_id:
        return {"error": "no user_id"}

    db_path = Path(__file__).resolve().parents[1] / "db.json"

    if not db_path.exists():
        db_path.write_text("{}")

    db = json.loads(db_path.read_text())

    crystals = db.get(user_id, 0)

    return {"crystals": crystals}
