from django import forms
from .models import ItemRequest, Listing


class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = [
            'title',
            'description',
            'category',
            'condition',
            'price',
            'exchange_type',
        ]

class ItemRequestForm(forms.ModelForm):
    class Meta:
        model = ItemRequest
        fields = ['message']