from django.forms import ModelForm
from .models import Recipe

#Form for recipes input
class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = '__all__'
        exclude = ['host']