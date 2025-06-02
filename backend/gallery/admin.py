from django.contrib import admin

from .models import Gallery, Keyword, UserAccount

admin.site.register(Keyword)
admin.site.register(Gallery)
admin.site.register(UserAccount)
