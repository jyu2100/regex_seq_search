from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .utils import run_search
import json

# Front-end view
def home(request):
    return render(request, "search/home.html")

# API View
class RegexSearchView(APIView):
    def get(self, request):
        pattern_str = request.query_params.get("pattern")
        uid = request.query_params.get("uid")
        
        try:
            json_str = run_search(pattern_str, uid)
            return Response(json_str)
        except Exception as e:
            json_str = json.dumps({"error": str(e)})
            return Response(json_str, status=400)
