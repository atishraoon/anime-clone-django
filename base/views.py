from django.shortcuts import render, redirect , get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy
from django.views.generic import TemplateView , View  
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse
from django.http import JsonResponse
from django.core.files.storage import default_storage

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import RedirectView
from django.contrib.auth.models import User
import json
from django.views.generic.detail import DetailView
from django.http import Http404

#import models.py
from base.models import *
 


# -------------------------------------------------------------------------------------------------------
# remvoe one anime from anime list
class RemoveAnime(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        user = request.user
        anime_id = request.POST.get('anime_id')

        # Ensure anime_id is valid
        try:
            anime = Anime.objects.get(id=anime_id)
        except Anime.DoesNotExist:
            return JsonResponse({"success": False, "error": "Anime not found."}, status=404)

        # Remove the specific anime from the user's AnimeList
        deleted_count, _ = AnimeList.objects.filter(user=user, anime=anime).delete()

        # Return success response
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            if deleted_count > 0:
                return JsonResponse({"success": True})
            else:
                return JsonResponse({"success": False, "error": "Anime not found in your list."}, status=404)
        else:
            return redirect(reverse('profile'))





# remove all the watchlist inside associated with logined profile 
class RemoveAllAnime(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        user = request.user
     
        AnimeList.objects.filter(user=user).delete()

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({"success": True})
        else:
            return redirect(reverse('profile'))


# add anime in anime list
class AddAnime(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        user = request.user
        anime_id = request.POST.get('anime_id')

        # Fetch the anime instance and add it to the user's list
        anime = get_object_or_404(Anime, id=anime_id)
        AnimeList.objects.create(user=user, anime=anime, status='pending')

        # Return a JSON response or redirect to the same page
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({"success": True})
        else:
            return redirect(reverse('profile')) 



class BaseProfileEdit(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        user = request.user

        # Fetch the logged-in user's profile
        profile = get_object_or_404(UserProfile, user=user)

        # Update the profile name and picture
        name = request.POST.get('profile_edit')
        profile_pic = request.FILES.get('profile_pic')

        if name:
            profile.name = name
        if profile_pic:
            # Delete the old profile picture if it exists
            if profile.profile_pic and default_storage.exists(profile.profile_pic.path):
                default_storage.delete(profile.profile_pic.path)
            profile.profile_pic = profile_pic

        profile.save()

        # Return a JSON response or redirect to the profile page
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({"success": True})
        else:
            return redirect(reverse('profile'))

# -------------------------------------------------------------------------------------------------------
# profile and watchlist
class BaseProfile(LoginRequiredMixin, TemplateView):
    template_name = "base/profile_wishlist.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get the logged-in user
        user = self.request.user
       

        # Fetch the user profile or set to None if it doesn't exist
        user_profile = UserProfile.objects.filter(user=user).first()
        context['user_profile'] = user_profile

        # Fetch the anime list associated with the user
        anime_list = AnimeList.objects.filter(user=user)
        context['anime_list'] = anime_list

        return context 

   


# -------------------------------------------------------------------------------------------------------
# anime search
def search(request):
    query = request.GET.get('q', '')  
    if query:
       
        animes = Anime.objects.filter(
            title__icontains=query
        ) | Anime.objects.filter(
            category__icontains=query
        )
    else:
        animes = Anime.objects.all() 

    context = {
        'animes': animes,
        'query': query,
    }
    return render(request, 'base/search.html', context)
  
# -------------------------------------------------------------------------------------------------------


class BaseAnimeWatch(LoginRequiredMixin,DetailView):
    model = Anime
    template_name = 'base/watch.html'
    context_object_name = 'anime'
    slug_field = 'title'
    slug_url_kwarg = 'title'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        anime = context['anime']

     
        allepisodes = anime.episodes.all()
        context['allepisodes'] = allepisodes

       
        context['episodes_json'] = json.dumps([
            {
                "name": ep.name,
                "episode_no": ep.episode_no,
                "video_url": ep.video_url,
            }
            for ep in allepisodes
        ])

       
        episode_no = self.kwargs.get('episode_no')

        if episode_no:
           
            episode = allepisodes.filter(episode_no=episode_no).first()
            if episode:
                context['episode'] = episode
            else:
                
                raise Http404("Episode not found")
        else:
           
            context['episode'] = allepisodes.first() if allepisodes.exists() else None

        context['allanimes'] = Anime.objects.all()

        return context



# def BaseAnimeWatch(request, title, episode_no):

#     allanimes = Anime.objects.all()
#     anime = get_object_or_404(Anime, title=title)

#     allepisodes = anime.episodes.all()
#     episode = anime.episodes.filter(episode_no=episode_no).first()

  
#     if not episode:
#         return render(request, 'error_page.html', {'message': 'Episode not found'})

#     # Pass the context to the template
#     context = {
#         'anime': anime,
#         'allanimes':allanimes,
#         'episode': episode,
#         'allepisodes': allepisodes, 
#     }
    
#     return render(request, 'base/watch.html', context)




# -------------------------------------------------------------------------------------------------------

#detail page
class BaseAnimeDetail(DetailView):
    model = Anime
    template_name = "base/detail.html"
    context_object_name = "anime"
    slug_field = "title"
    slug_url_kwarg = "title"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['allanimes'] = Anime.objects.all()
        return context


# -------------------------------------------------------------------------------------------------------

#home page
class BaseHome(ListView):  
    model = Anime
    template_name = "base/home.html"
    context_object_name = 'anime'


# -----------------------------------------------------------------------------------------------------


#login
class BaseLogin(LoginView):  
    template_name = "base/login.html"  
    fields = ['username', 'password']
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('home') 


#logout
class LogoutView(RedirectView):
    url = '/home'  
    
    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)     


#register
class BaseRegister(FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(BaseRegister, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('home')
        return super(BaseRegister, self).get(*args, **kwargs)


# -----------------------------------------------------------------------------------------------------

