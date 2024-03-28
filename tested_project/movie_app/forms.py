import self
from django import forms
from . models import Movie,Category
from .models import Review
class movieform(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['user', 'name','slug', 'desc', 'date', 'img', 'category', 'cast', 'available', 'trailer_link']
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = [ 'content', 'rating']

    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)
        self.fields['content'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Write your review'})
        self.fields['rating'].widget = forms.HiddenInput()

        def clean_rating(self):
            rating = self.cleaned_data.get('rating', None)  # Check if rating is present
            if rating is None or rating < 1 or rating > 5:
                raise forms.ValidationError("Invalid rating.")
            return rating
