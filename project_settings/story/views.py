from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
import requests
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from .serializers import ReadingProgressSerializer, StorySerializer, PreferenceSerializer, DifficultWordSerializer
from .models import Story, Preference, ReadingProgress, DifficultWord
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from users.permissions import IsOwner, IsAdmin


class StoryListCreateView(generics.ListCreateAPIView):
    queryset = Story.objects.all()
    serializer_class = StorySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['title','level']
    search_fields = ['title', 'author']
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class StoryRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Story.objects.all()
    serializer_class = StorySerializer
    permission_classes = [IsAuthenticated, IsOwner | IsAdmin]       


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsOwner])
def submit_for_review(request, pk):
    story = get_object_or_404(Story, pk=pk)
    if story.status == 'draft':
        story.status = 'pending'
        story.save()
        return Response({'status': 'Story submitted for review'}, status=status.HTTP_200_OK)
    return Response({'error': 'Only draft stories can be submitted for review'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdmin])
def approve_story(request, pk):
    story = get_object_or_404(Story, pk=pk)
    if story.status == 'pending':
        story.status = 'published'
        story.save()
        return Response({'status': 'Story approved and published'}, status=status.HTTP_200_OK)
    return Response({'error': 'Only admin can approve stories'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdmin])
def reject_story(request, pk):
    story = get_object_or_404(Story, pk=pk)
    rejection_reason = request.data.get('rejection_reason', '')
    if story.status == 'pending':
        story.status = 'rejected'
        story.rejection_reason = rejection_reason
        story.save()
        return Response({'status': 'Story rejected'}, status=status.HTTP_200_OK)
    return Response({'error': 'Only admin can reject stories'}, status=status.HTTP_400_BAD_REQUEST)


class PreferenceRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = PreferenceSerializer
    permission_classes = [IsAuthenticated]
    def get_object(self):
        return get_object_or_404(Preference, user=self.request.user)

class HistoryListView(generics.ListAPIView):
    serializer_class = ReadingProgressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return ReadingProgress.objects.all()
        return ReadingProgress.objects.filter(user=self.request.user)



def getMeaning(word):
    try:
        response = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}")
        if response.status_code == 200:
            data = response.json()
            return data[0]['meanings'][0]['definitions'][0]['definition']
    except Exception:
        pass
    return None


class DifficultWordListCreateView(generics.ListCreateAPIView):
    serializer_class = DifficultWordSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return DifficultWord.objects.all()
        return DifficultWord.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        word = serializer.validated_data.get('word')
        meaning = getMeaning(word)
        serializer.save(user=self.request.user, meaning=meaning)



class ReadingProgressDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset=ReadingProgress.objects.all()
    serializer_class=ReadingProgressSerializer
    permission_classes=[IsAuthenticated]


class ReadingProgressList(generics.ListCreateAPIView):
    queryset=ReadingProgress.objects.all()
    serializer_class=ReadingProgressSerializer
    permission_classes=[IsAuthenticated]


def Recommendations (progress):
    if progress<30:
        level='beginner'
    elif progress<70:
        level='intermediate' 
    else:
        level='advanced'       
    return Story.objects.filter(level=level )



class Recommended(generics.ListAPIView):
    serializer_class=StorySerializer
    permission_classes=[IsAuthenticated]

    def get_queryset(self):
        x=self.request.user
        records=ReadingProgress.objects.filter(user=x)

        if len(records)==0:
            return Story.objects.filter (level='beginner') 
        count=0
        total=0
        for x in records:
            tot_progress=min(round((x.words_read/len(x.story.content.split()) ) * 100, 2), 100)
            total+=tot_progress
            count+=1
        if count==0:
            return     Story.objects.filter (level='beginner') 
        return Recommendations(total/count)
        


