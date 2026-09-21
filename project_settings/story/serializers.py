from rest_framework import serializers
from .models import Story,Preference, ReadingProgress, DifficultWord

class StorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Story
        fields=['title','content','category']
        read_only_fields = [ 'created_at','rejection_reason', 'status','author']



class PreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model=Preference
        fields='__all__'

class ReadingProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReadingProgress
        fields = '__all__'


class DifficultWordSerializer(serializers.ModelSerializer):
    class Meta:
        model = DifficultWord
        fields = '__all__'







