import json

def handler(request, context):
    try:
        data = json.loads(request.body)
    except:
        return {"statusCode": 400, "body": json.dumps({"error": "invalid JSON"})}

    user_id = data.get("user_id")
    if not user_id:
        return {"statusCode": 400, "body": json.dumps({"error": "no user_id"})}

    # Здесь можно вставить реальную проверку через Telegram API
    # Пока просто имитируем, что пользователь подписан
    subscribed = True  # True или False
    reward = 50        # Количество кристаллов за подписку

    return {
        "statusCode": 200,
        "body": json.dumps({
            "subscribed": subscribed,
            "reward": reward
        })
    }
