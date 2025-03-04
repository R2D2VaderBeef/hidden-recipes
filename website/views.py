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



def home(request):
    return render(request, 'website/home.html')

def tags(request):
    return render(request, 'website/tags.html')


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
                return HttpResponse("Your account is disabled.")
        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
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
            return redirect('website:profile')  # Redirect to the profile page after saving
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
            form.save_m2m()  # Save the many-to-many relationships (tags)
            return redirect('website:home')  # Redirect to homepage after saving
    else:
        form = RecipeForm()

    return render(request, 'website/create_recipe.html', {'form': form})


@login_required
def edit_recipe(request, recipe_id):
    recipe = Recipe.objects.get(id=recipe_id, poster_id=request.user)

    if request.method == 'POST':
        form = RecipeForm(request.POST, instance=recipe)
        if form.is_valid():
            form.save()  # Save changes to the recipe
            return redirect('website:profile')  # Redirect to the profile page after saving
    else:
        form = RecipeForm(instance=recipe)

    return render(request, 'website/edit_recipe.html', {'form': form, 'recipe': recipe})
