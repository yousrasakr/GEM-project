from django.shortcuts import render
from rest_framework import viewsets
from .models import Statue
from .serializers import StatueSerializer

class StatueViewSet(viewsets.ModelViewSet):
    queryset = Statue.objects.all()
    serializer_class = StatueSerializer

