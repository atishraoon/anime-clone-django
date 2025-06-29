from django.contrib import admin
from .models import Genre, Anime, Episode , UserProfile,AnimeList
 
admin.site.register(Genre)
# class GenreAdmin(admin.ModelAdmin):
#     list_display = ('id', 'name')
#     search_fields = ('name',)

 
admin.site.register(Anime)
class AnimeAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'description')
    list_filter = ('category', 'genres')
    search_fields = ('title', 'description')
    filter_horizontal = ('genres',)  # Allows better UI for many-to-many fields


admin.site.register(Episode)
# class EpisodeAdmin(admin.ModelAdmin):
#     list_display = ('id', 'anime', 'name', 'video_url')
#     search_fields = ('name', 'video_url')
#     list_filter = ('anime',)


admin.site.register(UserProfile)
admin.site.register(AnimeList) 