from django.contrib import admin
from movie_app.models import *


class PostAdmin(admin.ModelAdmin):
    list_display = ("title",  "duration", "creation_date")
    list_display_links = ("title",)
    search_fields = ("title", "description")


admin.site.register(Director)
admin.site.register(Movie, PostAdmin)
admin.site.register(Review)
