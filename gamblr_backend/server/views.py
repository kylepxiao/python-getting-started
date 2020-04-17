from django.contrib.auth.models import User, Group
from django.core.files.storage import FileSystemStorage
from rest_framework import viewsets
from rest_framework import permissions
from gamblr_backend.server.serializers import UserSerializer, GroupSerializer, FileSerializer, JsonSerializer
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .opencv_card_detector.CardDetector import *
from gamblr_backend.settings import *
import cv2
import numpy as np
import gamblr_backend.server.opencv_card_detector.Cards as Cards
import gamblr_backend.server.strategy_agent.tabular as tabular
import json
from django.http import JsonResponse


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]

class FileUploadView(APIView):

    def post(self, request, *args, **kwargs):

      file_serializer = FileSerializer(data=request.data)

      if file_serializer.is_valid():
          file_serializer.save()
          
          file_obj = request.FILES['file']
          image = cv2.imread(os.path.join(MEDIA_ROOT, str(file_obj)), 1)
          results = get_classification(image)
          cards = []
          for result in results:
              values = {
                  'best_rank_match': result.best_rank_match,
                  'best_suit_match': result.best_suit_match,
                  'rank_diff': result.rank_diff,
                  'suit_diff': result.suit_diff
              }
              cards.append(values)
          response = {'cards': cards}

          return JsonResponse(response, status=status.HTTP_201_CREATED)
      else:
          return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class JSONUploadView(APIView):

    def post(self, request, *args, **kwargs):

      json_serializer = JsonSerializer(data=request.data)

      if json_serializer.is_valid():
          json_serializer.save()

          data = json.loads(request.data['json'])

          if data['method'] == 'tabular':
              try:
                move = tabular.get_action(data['dealer_upcard'], data['player_cards'])
                response = {'move': move}
                return JsonResponse(response, status=status.HTTP_201_CREATED)
              except:
                response = {'move': "Insufficient or Incorrectly Formatted Data"}
                return JsonResponse(response, status=status.HTTP_201_CREATED)
          else:
              return Response(json_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
      else:
          return Response(json_serializer.errors, status=status.HTTP_400_BAD_REQUEST)