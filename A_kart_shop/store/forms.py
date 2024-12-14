from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'review_text']
        widgets = {
            'rating': forms.Select(choices=[(1, '1 Star'), (2, '2 Stars'), (3, '3 Stars'), (4, '4 Stars'), (5, '5 Stars')], 
                                   attrs={'class': 'form-select'}),
            'review_text': forms.Textarea(attrs={'placeholder': 'Write your review here...', 'class': 'form-control'}),
        }
