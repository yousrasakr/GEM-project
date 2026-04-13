from django.shortcuts import render
from rest_framework import viewsets
from .models import Statue
from .serializers import StatueSerializer
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import requests
import json
import os


AI_URL = os.getenv("AI_URL", "http://127.0.0.1:5000")

class StatueViewSet(viewsets.ModelViewSet):
    queryset = Statue.objects.all()
    serializer_class = StatueSerializer


@csrf_exempt
def chatbot(request):
    if request.method != "POST":
        return JsonResponse({"error": "Only POST method allowed"}, status=405)

    try:
        data = json.loads(request.body)
        user_message = data.get("message")
        statue_id = data.get("statue_id")

        if not user_message:
            return JsonResponse({"error": "Message is required"}, status=400)

        # 🔗 Send request to AI server
        response = requests.post(
            f"{AI_URL}/chat",
            json={
                "message": user_message,
                "statue_id": statue_id
            },
            timeout=10
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

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


# -----------------------------
# Speak API (Audio + Lipsync)
# -----------------------------
@csrf_exempt
def speak(request):
    if request.method != "POST":
        return JsonResponse({"error": "Only POST method allowed"}, status=405)

    try:
        data = json.loads(request.body)
        text = data.get("text")

        if not text:
            return JsonResponse({"error": "Text is required"}, status=400)

        # 🔗 Send request to AI server
        response = requests.post(
            f"{AI_URL}/speak",
            json={"text": text},
            timeout=15
        )

        if response.status_code != 200:
            return JsonResponse({
                "error": "AI speech error",
                "details": response.text
            }, status=500)

        return JsonResponse(response.json())

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)