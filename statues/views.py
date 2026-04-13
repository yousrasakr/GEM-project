from django.shortcuts import render
from rest_framework import viewsets
from .models import Statue
from .serializers import StatueSerializer
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import requests
import json
import os


# 🔗 AI Server URL (local for now, change later in deployment)
AI_URL = os.getenv("AI_URL", "http://127.0.0.1:5000")


# -----------------------------
# Statue API (CRUD)
# -----------------------------
class StatueViewSet(viewsets.ModelViewSet):
    queryset = Statue.objects.all()
    serializer_class = StatueSerializer


# -----------------------------
# Chatbot API
# -----------------------------
@csrf_exempt
def chatbot(request):
    if request.method != "POST":
        return JsonResponse({"error": "Only POST method allowed"}, status=405)

    try:
        # ✅ Read request body
        data = json.loads(request.body)

        # ✅ Extract fields
        user_message = data.get("message")
        statue_id = data.get("statue_id")

        if not user_message:
            return JsonResponse({"error": "Message is required"}, status=400)

        # 🔗 Send to AI server
        response = requests.post(
            f"{AI_URL}/chat",
            json={
                "message": user_message,
                "statue_id": statue_id
            },
            timeout=10
        )

        # ❗ Handle AI errors
        if response.status_code != 200:
            return JsonResponse({
                "error": "AI server error",
                "details": response.text
            }, status=500)

        # ✅ Extract AI response
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


# -----------------------------
# Speak API (Audio + Lipsync)
# -----------------------------
@csrf_exempt
def speak(request):
    if request.method != "POST":
        return JsonResponse({"error": "Only POST method allowed"}, status=405)

    try:
        # ✅ Read request body
        data = json.loads(request.body)

        # ✅ Extract text
        text = data.get("text")

        if not text:
            return JsonResponse({"error": "Text is required"}, status=400)

        # 🔗 Send to AI server
        response = requests.post(
            f"{AI_URL}/speak",
            json={"text": text},
            timeout=15
        )

        # ❗ Handle AI errors
        if response.status_code != 200:
            return JsonResponse({
                "error": "AI speech error",
                "details": response.text
            }, status=500)

        # ✅ Return full AI response (audio + lipsync)
        return JsonResponse(response.json())

    except requests.exceptions.RequestException:
        return JsonResponse({
            "error": "Cannot connect to AI server. Is it running?"
        }, status=500)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)