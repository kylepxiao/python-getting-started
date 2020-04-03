from django.contrib.auth.models import User, Group
from django.core.files.storage import FileSystemStorage
from rest_framework import viewsets
from rest_framework import permissions
from gamblr_backend.server.serializers import UserSerializer, GroupSerializer
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import FileSerializer
from .opencv_card_detector.CardDetector import *
from gamblr_backend.settings import *
import cv2
import numpy as np
import gamblr_backend.server.opencv_card_detector.Cards as Cards
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
    parser_class = (FileUploadParser,)

    def post(self, request, *args, **kwargs):

      file_serializer = FileSerializer(data=request.data)

      if file_serializer.is_valid():
          file_serializer.save()
          
          #image = cv2.imdecode(np.fromstring(request.FILES['file'].read(), np.uint8), cv2.IMREAD_UNCHANGED)
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
          #fs = FileSystemStorage()
          #filename = fs.save(file_obj.name, file_obj)
          #uploaded_file_url = fs.url(filename)

          #image = cv2.imread(uploaded_file_url, 1)

          #return Response(file_serializer.data, status=status.HTTP_201_CREATED)
          return JsonResponse(response, status=status.HTTP_201_CREATED)
      else:
          return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)