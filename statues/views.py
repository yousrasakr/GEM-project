from django.shortcuts import render
from rest_framework import viewsets
from .models import Statue
from .serializers import StatueSerializer
from django.views.decorators.csrf import csrf_exempt

class StatueViewSet(viewsets.ModelViewSet):
    queryset = Statue.objects.all()
    serializer_class = StatueSerializer

import requests
import json
from django.http import JsonResponse

@csrf_exempt
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
            timeout=10
        )

        ai_response = response.json().get("response", "")

        return JsonResponse({"response": ai_response})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)