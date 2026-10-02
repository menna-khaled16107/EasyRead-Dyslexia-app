from django.urls import path
from .views import *



urlpatterns = [ 
path('stories/', StoryListCreateView.as_view(), name='story_list_create'),
path('stories/<int:pk>/', StoryRetrieveUpdateDestroyView.as_view(), name='story_retrieve_update_destroy'),
path('stories/<int:pk>/submit/', submit_for_review, name='submit'),
path('stories/<int:pk>/approve/', approve_story, name='approve'),
path('stories/<int:pk>/reject/', reject_story, name='reject'),

path('preferences/<int:pk>/', PreferenceRetrieveUpdateView.as_view(), name='preference_Settings'),
path('history/', HistoryListView.as_view(), name='user_history'),
path('difficult-words/', DifficultWordListCreateView.as_view(), name='difficult_words'),
path('reading_progreess/',ReadingProgressList.as_view(),name='MyReading'),
path('reading_progreess/<int:pk>/',ReadingProgressDetail.as_view(),name='MyReading'),
path('recommended-stories/',Recommended.as_view,name='Rcommended_stories'),

]


























