from django.db import models
from users.models import User


class Story(models.Model):

    status_choices = [
    ('draft', 'Draft'),
    ('published', 'Published'),
    ('pending', 'Pending'),
    ('rejected', 'Rejected'),
     
]   
    level_choices = [
    ('beginner', 'Beginner'),   
    ('intermediate', 'Intermediate'),
    ('advanced', 'Advanced'),
    ]

    title = models.CharField(max_length=100)
    content = models.TextField()
    level = models.CharField(max_length=20, choices=level_choices, default='beginner')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='stories')
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=status_choices, default='draft')
    rejection_reason = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title


class Preference(models.Model):
    FONT_SIZE_CHOICES = [
        ('small', 'Small'),
        ('medium', 'Medium'),
        ('large', 'Large'),
        ('x-large', 'Extra Large'),
    ]

    LINE_SPACING_CHOICES = [
        (1.0, 'Normal'),
        (1.5, 'Medium'),
        (2.0, 'Wide'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='preference')
    font_size = models.CharField(max_length=10, choices=FONT_SIZE_CHOICES, default='large')  
    line_spacing = models.FloatField(choices=LINE_SPACING_CHOICES, default=1.5)  

    def __str__(self):
        return f"Preferences for {self.user.username}"



class ReadingProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reading_progress')
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name='reading_progress')
    words_read = models.IntegerField(default=0)
    completed = models.BooleanField(default=False)


    class Meta:
        unique_together = ('user', 'story')  


class DifficultWord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='difficult_words')
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name='difficult_words')
    word = models.CharField(max_length=100)

    class Meta:
        unique_together = ('user', 'story', 'word')




        