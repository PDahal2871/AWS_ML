from django.forms import ModelForm
from .models import *

class AWSForm(ModelForm):
    class Meta:
        model=Aws
        fields = '__all__'
