import os
import json
from supabase import create_client

SUPABASE_URL = os.environ.get("https://zgimekjujkxhwmmmtzqh.supabase.co")
SUPABASE_KEY = os.environey.get("JhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InpnaW1la2p1amt4aHdtbW10enFoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjM3MDA4MjYsImV4cCI6MjA3OTI3NjgyNn0.gOux_AOmrguzFmdf3SF17sjpH5pTPALoTnvYuipGJtA")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def handler(request, context):
    try:
        data = json.loads(request.body)
    except:
        return {"statusCode": 400, "body": json.dumps({"error": "invalid JSON"})}

    user_id = data.get("user_id")
    crystals = data.get("crystals")

    if not user_id or crystals is None:
        return {"statusCode": 400, "body": json.dumps({"error": "invalid data"})}

    # Обновляем или вставляем
    existing = supabase.table("crystals").select("user_id").eq("user_id", user_id).execute()
    if existing.data:
        supabase.table("crystals").update({"crystals": crystals}).eq("user_id", user_id).execute()
    else:
        supabase.table("crystals").insert({"user_id": user_id, "crystals": crystals}).execute()

    return {"statusCode": 200, "body": json.dumps({"status": "ok"})}
