from django.contrib import admin

from .models import Favourite
from .models import Media

#register with admin site!!
admin.site.register(Media)
admin.site.register(Favourite)
