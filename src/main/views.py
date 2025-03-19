from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.
from rest_framework import viewsets

def ping(request):
    return JsonResponse({'message': 'pong'})