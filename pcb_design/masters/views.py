from django.shortcuts import render
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class Components(APIView):
    # Write a logic like, If we have compinent Id in Url Path Param
    # Then Fetch Component Id alone 
    # Else Fetch All components

    # Add permission class as others
    def get(self, request):
        pass