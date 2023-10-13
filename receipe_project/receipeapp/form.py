from django import forms

from .models import Recipe,Rating

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'ingredients': forms.Textarea(attrs={'class': 'form-control'}),
            'instructions': forms.Textarea(attrs={'class': 'form-control'}),
            'prep_time': forms.TextInput(attrs={'class': 'form-control'}),
            'difficulty': forms.Select(attrs={'class': 'form-control'}),
            'vegetarian': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'image': forms.FileInput(attrs={'class': 'form-control'})
        }

class RatingForm(forms.ModelForm):
    class Meta:
        model=Rating
        fields=['rating']
        rating = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'rating-widget'}))

class RecipeUpdateForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = '__all__'