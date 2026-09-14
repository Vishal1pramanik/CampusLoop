from django.contrib import admin
from .models import Listing, ItemRequest, Message

admin.site.register(Listing)
admin.site.register(ItemRequest)
admin.site.register(Message)