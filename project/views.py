import requests
import json
from django.http import JsonResponse

def chatbot(request):
    if request.method != "POST":
        return JsonResponse({"error": "Only POST method allowed"}, status=405)

    try:
        data = json.loads(request.body)
        user_message = data.get("message")

        if not user_message:
            return JsonResponse({"error": "Message is required"}, status=400)

        response = requests.post(
            "http://127.0.0.1:5000/chat",
            json={"message": user_message},
            timeout=10   # ⬅️ prevents hanging
        )

        if response.status_code != 200:
            return JsonResponse({
                "error": "AI server error",
                "details": response.text
            }, status=500)

        ai_response = response.json().get("response", "")

        return JsonResponse({
            "response": ai_response
        })

    except requests.exceptions.RequestException:
        return JsonResponse({
            "error": "Cannot connect to AI server. Is it running?"
        }, status=500)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)