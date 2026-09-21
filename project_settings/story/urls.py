from django.urls import path
from .views import *



urlpatterns = [ 
path('stories/', StoryListCreateView.as_view(), name='story_list_create'),
path('stories/<int:pk>/', StoryRetrieveUpdateDestroyView.as_view(), name='story_retrieve_update_destroy'),
path('stories/<int:pk>/submit/', submit_for_review, name='submit'),
path('stories/<int:pk>/approve/', approve_story, name='approve'),
path('stories/<int:pk>/reject/', reject_story, name='reject'),
path('preferences/', PreferenceRetrieveUpdateView.as_view(), name='settings_preferences'),

]


























