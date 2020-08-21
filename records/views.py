import json
from django.db.models import Q
from django.contrib.auth.models import User
from django.http.response import JsonResponse
from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view
from .models import List, Word
from .serializers import ListSerializer, WordSerializer


@api_view(["GET"])
def word_search(request):
    user = request.user
    query = request.GET.get("query")
    if not user.is_authenticated:
        return JsonResponse({"error": "authentication were not provided"}, status=401)
    if not query:
        return JsonResponse({'error': "enter search query"}, status=400)
    offset = int(request.GET.get("offset", 0))
    limit = int(request.GET.get('limit', 10))
    qs = Word.objects.filter(Q(text__icontains=query)|Q(origin_title__icontains=query), user=user).distinct()
    results = WordSerializer(qs, many=True).data
    return JsonResponse({"results": results}, status=200)


class ListViewSet(viewsets.ModelViewSet):
    serializer_class = ListSerializer
    queryset = List.objects.all()
    permission_classes = [
      permissions.IsAuthenticated,
      ]
    def get_queryset(self):
        qs = List.objects.all()
        return qs
    def perform_create(self, serializer):
        serializer.save(user=request.user)

class WordViewSet(viewsets.ModelViewSet):
    serializer_class = WordSerializer
    queryset =  Word.objects.all()
    permission_classes = [
      permissions.IsAuthenticated,
      ]

    def get_queryset(self):
        user = self.request.user
        query = self.request.GET.get("query")
        offset = int(self.request.GET.get("offset", 0))
        limit = int(self.request.GET.get('limit', 10))
        if query is not None:
            qs = Word.objects.filter(Q(text__icontains=query)|Q(origin_title__icontains=query), user=user).distinct()[offset: limit+offset]
        else:
            qs = user.words.all();
        return qs

    def create(self, request, *args, **kwargs):
        data = json.loads(request.body)
        user = request.user
        list_data = data.get('list_data');
        word_data = data.get('word_data');
        list_id = word_data.get('list_id');
        wordlist = None
        list_created = False
        if list_data.get('name'):
            list_serializer = ListSerializer(data=list_data)
            if list_serializer.is_valid():
                wordlist = list_serializer.save(user=user)
                list_created = True
            else:
                return JsonResponse({"list_errors": list_serializer.errors}, status=401)
        elif list_id:
            wordlist = List.objects.get(id=list_id)
        word_serilizer = WordSerializer(data=word_data)
        if word_serilizer.is_valid():
            word_serilizer.save(user=user, wordlist=wordlist)
        else:
            return JsonResponse({"word_errors": word_serilizer.errors}, status=401)
        return JsonResponse({
            'word_data': word_serilizer.data,
            "list_data": list_serializer.data if list_created else {},
        }, status=201)
    
    