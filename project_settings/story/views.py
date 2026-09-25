from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from .serializers import ReadingProgressSerializer, StorySerializer, PreferenceSerializer
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
    filterset_fields = ['title']
    search_fields = ['title', 'content']
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class StoryRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Story.objects.all()
    serializer_class = StorySerializer
    permission_classes = [IsAuthenticated, IsOwner | IsAdmin]       


@action (detail=True ,methods=['post'], permission_classes=[IsAuthenticated, IsOwner])
def submit_for_review(self, request, pk=None):
    story = self.get_object()
    if story.status == 'draft':
        story.status = 'pending'
        story.save()
        return Response({'status': 'Story submitted for review'}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Only draft stories can be submitted for review'}, status=status.HTTP_400_BAD_REQUEST) 

@action (detail=True ,methods=['post'], permission_classes=[IsAuthenticated, IsAdmin])
def approve_story(self, request, pk=None):
    story = self.get_object()
    if story.status == 'pending':
        story.status = 'published'
        story.save()
        return Response({'status':'Story approved and published'}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Only admin   can approve stories'}, status=status.HTTP_400_BAD_REQUEST)


@action (detail=True ,methods=['post'], permission_classes=[IsAuthenticated, IsAdmin])
def reject_story(self, request, pk=None):
    story = self.get_object()
    rejection_reason = request.data.get('rejection_reason', '')
    if story.status == 'pending':
        story.status = 'rejected'
        story.rejection_reason = rejection_reason
        story.save()
        return Response({'status':'Story rejected'}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Only admin can reject stories'}, status=status.HTTP_400_BAD_REQUEST)



class PreferenceRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = PreferenceSerializer
    permission_classes = [IsAuthenticated]
    def get_object(self):
        return Preference.objects.get(user=self.request.user)

class HistoryListView(generics.ListAPIView):
    serializer_class = ReadingProgressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.is_staff:
            return ReadingProgress.objects.all()
        return ReadingProgress.objects.filter(user=self.request.user)













