from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.utils import timezone
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from website.forms import UserForm, UserProfileForm
from .models import User, Tag, Recipe, UserProfile, Comment
from .forms import RecipeForm, CommentForm

def home(request):
    recipes = Recipe.objects.all().order_by('-date') 
    paginator = Paginator(recipes, 6)  #6recipes at a time
    page_number = request.GET.get('page')
    try:
        recipes = paginator.page(page_number)
    except PageNotAnInteger:
        recipes = paginator.page(1)
    except EmptyPage:
        recipes = paginator.page(paginator.num_pages)

    return render(request, 'website/home.html', {'recipes': recipes})

def tags(request):
    return render(request, 'website/tags.html')

def recipe_view(request):
    return render(request, 'website/recipe_view.html')

def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = UserProfile(user=user)
            profile.save()

            registered = True

    else:
        user_form = UserForm()

    return render(request,
                'website/register.html',
                context = {'user_form': user_form,
                            'registered': registered})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                next = request.POST.get('after_login')
                if next is not None:
                    return redirect(next)
                else:
                    return redirect(reverse('website:home'))
            else:
                return render(request, 'website/login.html', context = {"error": True, "error_message": "Your account has been disabled."})
        else:
            return render(request, 'website/login.html', context = {"error": True, "error_message": "Incorrect username or password."})
    else:
        after_login = request.GET.get('next')
        if after_login is not None:
            context = {"next": True, "after_login": after_login}
        else:
            context = {"next": False}
        return render(request, 'website/login.html', context = context)
    
@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('website:home'))

@login_required
def profile(request):
    user_profile = request.user.profile

    user_recipes_queryset = Recipe.objects.filter(poster=request.user).order_by('-date')
    paginator = Paginator(user_recipes_queryset, 6) 
    page_number = request.GET.get('page')

    try:
        user_recipes = paginator.page(page_number)
    except PageNotAnInteger:
        user_recipes = paginator.page(1)
    except EmptyPage:
        user_recipes = paginator.page(paginator.num_pages)
    
    total_likes = sum(recipe.likes.count() for recipe in user_recipes_queryset)

    return render(request, 'website/profile.html', {
        'user_profile': user_profile,
        'user_recipes': user_recipes,
        'total_likes': total_likes,

    })


@login_required
def liked_recipes(request):
    user_profile = request.user.profile
    user_recipes_queryset = Recipe.objects.filter(poster=request.user).order_by('-date')
    total_likes = sum(recipe.likes.count() for recipe in user_recipes_queryset)

    liked_recipes_queryset = request.user.liked_recipes.all().order_by('-date')
    paginator = Paginator(liked_recipes_queryset, 6)
    page_number = request.GET.get('page')
    user_recipes = user_recipes_queryset.count
    try:
        liked_recipes = paginator.page(page_number)
    except PageNotAnInteger:
        liked_recipes = paginator.page(1)
    except EmptyPage:
        liked_recipes = paginator.page(paginator.num_pages)

    return render(request, 'website/liked.html', {
        'user_profile': user_profile,
        'liked_recipes': liked_recipes,
        'user_recipes': user_recipes,
        'total_likes': total_likes,
    })


def tags_view(request):
    query = request.GET.get('tags', '')  # Get search query from URL parameters
    recipes = Recipe.objects.all().order_by('-date') 

    if query:
        recipes = recipes.filter(tags__name__icontains=query)  # Filter recipes by tag name

    paginator = Paginator(recipes, 6)  
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
        newTitle = request.POST["title"][0:128]
        newDescription = request.POST["description"][0:512]
        recipe = Recipe(title=newTitle, description=newDescription, ingredients=request.POST["ingredients"], instructions=request.POST["instructions"], picture=request.FILES["picture"])
        recipe.poster = request.user  # Set the author of the recipe
        recipe.date = timezone.now()
        recipe.save()
        
        tags = request.POST["tags"].split(",")
        for tag in tags:
            if tag == "":
                continue
            
            else:
                recipe.tags.add(Tag.objects.get(pk=int(tag)))

        return HttpResponse(recipe.pk) # We need the client side to redirect to the new recipe page

    return render(request, 'website/create_recipe.html', {'tags': serializers.serialize("json", Tag.objects.all())})

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

  
@login_required
def edit_profile(request):
    user_profile = request.user.profile  #get profile

    if request.method == 'POST':  
        profile_form = UserProfileForm(request.POST, request.FILES, instance=user_profile) #set profile
        username = request.POST.get("new_username") #new username
        new_password = request.POST.get('new_password') #new password
        old_password = request.POST.get('old_password')
        action = request.POST.get('action')  # Action checker to allow changing only one part

        if action == 'change_username' and username != request.user.username: #check its a different username 
            if not User.objects.filter(username=username).exists():   #check if username is free
                request.user.username = username
                request.user.save()  
                return redirect('website:profile')
    
        elif action == 'change_password':
            if check_password(old_password, request.user.password):  #Check old password
                request.user.set_password(new_password)  # Set new password
                request.user.save()
                return redirect(reverse('website:profile'))

        elif action == 'save_profile' and profile_form.is_valid():  #Profile Save
            profile_form.save()
            return redirect('website:profile')  

    else:
        profile_form = UserProfileForm(instance=user_profile)  #Return users data

    return render(request, 'website/edit_profile.html', {'profile_form': profile_form, 'user': request.user,
    })

@login_required
def delete_account(request):
    if request.method == "POST":
        user = request.user
        user.delete()
        return redirect('website:home')
    return render(request, 'website/delete_account.html')

@login_required
def delete_recipe(request, recipe_id):
    if request.method == 'POST':
        recipe = get_object_or_404(Recipe, id=recipe_id)
        if recipe.poster == request.user:
            recipe.delete()
            return redirect('website:home')
        else:
            return HttpResponse("Cannot delete recipe", status=401)

def view_recipe(request, recipe_id):
    try:
        recipe = Recipe.objects.get(id=recipe_id)
        ingredients = recipe.ingredients.split("\n")
        instructions = recipe.instructions.split("\n")
        comments = recipe.comments.all()
        comment_count = comments.count()
        form = CommentForm()
        
        if request.method == "POST":
             form = CommentForm(request.POST)
             if form.is_valid():
                comment = form.save(commit=False)
                comment.poster = request.user
                comment.recipe = recipe
                comment.save()
                return redirect('website:view_recipe', recipe_id = recipe.id)
             else:
                form = CommentForm()

                
    except Recipe.DoesNotExist:
        return render(request, '404.html', status=404)
    
    context = {'recipe': recipe, 'ingredients': ingredients, 'instructions': instructions, 'comments': comments, 'form': form, 'comment_count': comment_count}
    return render(request, 'website/recipe_view.html', context)

def delete_comment(request,comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.poster == request.user:
        comment.delete()
        return redirect('website:view_recipe',recipe_id=comment.recipe.id)
    else:
        return HttpResponse("Cannot delete comment", status=404)


@login_required
def like_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    user = request.user

    if user in recipe.likes.all():
        recipe.likes.remove(user)
        liked = False
    else:
        recipe.likes.add(user)
        liked = True

    return JsonResponse({"liked": liked, "likes_count": recipe.likes.count()})
