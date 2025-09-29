from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .utils import run_search

# Front-end view
def home(request):
    return render(request, "search/home.html")

# API View
class RegexSearchView(APIView):
    def get(self, request):
        pattern_str = request.query_params.get("pattern")
        uid = request.query_params.get("uid")
        
        try:
            result = run_search(pattern_str, uid)
            return Response(result)
        except Exception as e:
            json_str = {"detail": str(e)}
            return Response(json_str, status=status.HTTP_400_BAD_REQUEST)
