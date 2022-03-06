from django.forms import ModelForm, DateInput
from .models import SpendingTrs


class CustDateInput(DateInput):
    input_type = 'date'


class SpendingTrsForm(ModelForm):
    class Meta:
        model = SpendingTrs
        exclude = ()
        widgets = {
            'date': CustDateInput(),
        }