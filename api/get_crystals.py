import os
import json
from supabase import create_client

SUPABASE_URL = os.environ.get("https://zgimekjujkxhwmmmtzqh.supabase.co")
SUPABASE_KEY = os.environ.get("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InpnaW1la2p1amt4aHdtbW10enFoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjM3MDA4MjYsImV4cCI6MjA3OTI3NjgyNn0.gOux_AOmrguzFmdf3SF17sjpH5pTPALoTnvYuipGJtA")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def handler(request, context):
    user_id = request.args.get("user_id")
    if not user_id:
        return {"statusCode": 400, "body": json.dumps({"error": "no user_id"})}

    data = supabase.table("crystals").select("crystals").eq("user_id", user_id).execute()
    if data.data:
        crystals = data.data[0]["crystals"]
    else:
        crystals = 0
        supabase.table("crystals").insert({"user_id": user_id, "crystals": 0}).execute()

    return {"statusCode": 200, "body": json.dumps({"crystals": crystals})}
