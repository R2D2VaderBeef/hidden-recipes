from django.shortcuts import render
from django.http import HttpResponse

from website.forms import UserForm, UserProfileForm

from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required


from django.shortcuts import render
from .models import Tag, Recipe
from django.core.paginator import Paginator
from .forms import RecipeForm

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required


def home(request):
    recipes = Recipe.objects.all().order_by('-id')  # Get all recipes, newest first
    return render(request, 'website/home.html', {'recipes': recipes})

def tags(request):
    return render(request, 'website/tags.html')

def recipe_view(request):
    return render(request, 'website/recipe_view.html')

def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()
            registered = True
            
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()


    return render(request,
                'website/register.html',
                context = {'user_form': user_form,
                            'profile_form': profile_form,
                            'registered': registered})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('website:home'))
            else:
                return render(request, 'website/login.html', context = {"error": True, "error_message": "Your account has been disabled."})
        else:
            return render(request, 'website/login.html', context = {"error": True, "error_message": "Incorrect username or password."})
    else:
        return render(request, 'website/login.html')
    
@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('website:home'))

@login_required
def profile(request):
    # Get the user's profile
    user_profile = request.user.userprofile

    user_recipes = Recipe.objects.filter(poster_id=request.user)

    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance=user_profile)

        if profile_form.is_valid():
            profile_form.save()
            return redirect('website:profile')
    else:
        profile_form = UserProfileForm(instance=user_profile)

    return render(request, 'website/profile.html', {
        'profile_form': profile_form,
        'user_recipes': user_recipes  
    })

@login_required
def delete_account(request):
    if request.method == "POST":
        user = request.user
        user.delete()        
        return redirect('website:home')
    return render(request,'website/delete_account.html')



def tags_view(request):
    query = request.GET.get('q', '')  # Get search query from URL parameters
    recipes = Recipe.objects.all()

    if query:
        recipes = recipes.filter(tags__name__icontains=query)  # Filter recipes by tag name

    paginator = Paginator(recipes, 2)  # Paginate results (2 recipes per page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'recipes': page_obj,
        'query': query,
    }
    return render(request, 'website/tags.html', context)



@login_required
def create_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.poster = request.user  # Set the author of the recipe
            recipe.save()  
            form.save_m2m() 
            return redirect('website:home') 
    else:
        form = RecipeForm()

    return render(request, 'website/create_recipe.html', {'form': form})


@login_required
def edit_recipe(request, recipe_id):
    recipe = Recipe.objects.get(id=recipe_id, poster_id=request.user)

    if request.method == 'POST':
        form = RecipeForm(request.POST, instance=recipe)
        if form.is_valid():
            form.save()  
            return redirect('website:profile')  
    else:
        form = RecipeForm(instance=recipe)

    return render(request, 'website/edit_recipe.html', {'form': form, 'recipe': recipe})



def view_recipe(request, recipe_id):
    try:
        recipe = Recipe.objects.get(id=recipe_id)
    except Recipe.DoesNotExist:
        return HttpResponse("Recipe not found", status=404)

    context = {'recipe': recipe}
    return render(request, 'website/recipe_view.html', context)


@login_required
def like_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    user = request.user

    if user in recipe.likes.all():
        recipe.likes.remove(user)  # Unlike if already liked
        liked = False
    else:
        recipe.likes.add(user)  # Like if not already liked
        liked = True

    return JsonResponse({"liked": liked, "likes_count": recipe.likes.count()})
