from django.contrib import admin

from .models import *

admin.site.register(Tag)
admin.site.register(Tutorial)
admin.site.register(Category)

admin.site.register(Subscriber)
admin.site.register(Item)


