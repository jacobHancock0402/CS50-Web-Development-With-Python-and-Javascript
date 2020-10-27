from django.contrib import admin

# Register your models here.
from .models import Auction
from .models import Comments


admin.site.register(Auction)
admin.site.register(Comments)