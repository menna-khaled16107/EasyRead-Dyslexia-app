from rest_framework import serializers
from .models import Story,Preference, ReadingProgress, DifficultWord
class StorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Story
        fields=['title','content','level','rejection_reason','status','author','created_at']
        read_only_fields = [ 'created_at','rejection_reason', 'status','author']



class PreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model=Preference
        fields='__all__'

class ReadingProgressSerializer(serializers.ModelSerializer):
    progress = serializers.SerializerMethodField()

    class Meta:
        model = ReadingProgress
        fields = ['user', 'story', 'words_read', 'completed', 'progress']
        read_only_fields=['progress']

    def get_progress(self, obj):
        content = len(obj.story.content.split())
        progress = min(round((obj.words_read / content) * 100, 2), 100)
        return progress

  


class DifficultWordSerializer(serializers.ModelSerializer):
    class Meta:
        model = DifficultWord
        fields = '__all__'
        read_only_fields = ['meaning', 'user']






