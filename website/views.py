from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.utils import timezone
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from website.forms import UserForm, RecipeForm, CommentForm
from .models import User, Tag, Recipe, UserProfile, Comment

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
                    return redirect('website:profile', username=user.username)

            else:
                return render(request, 'website/login.html', context = {"error": True, "error_message": "Your account has been disabled."})
        else:
            return render(request, 'website/login.html', context = {"error": True, "error_message": "Incorrect username or password."})
    else:
        context = {}
        if 'password_changed' in request.session and request.session['password_changed'] == True:
            request.session['password_changed'] = False
            context["error"] = True
            context["error_message"] = "Password changed successfully. Please log in again."

        after_login = request.GET.get('next')
        if after_login is not None:
            context["next"] = True
            context["after_login"] = after_login
        else:
            context["next"] = False

        return render(request, 'website/login.html', context = context)
    
@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('website:home'))

# website/views.py
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from .models import Recipe

def profile(request, username):
    user_obj = get_object_or_404(User, username=username)
    is_own_profile = request.user == user_obj

    recipes_queryset = Recipe.objects.filter(poster=user_obj).order_by('-date')
    paginator = Paginator(recipes_queryset, 6)
    page_number = request.GET.get('page')
    user_recipes = paginator.get_page(page_number)
    total_likes = sum(recipe.likes.count() for recipe in recipes_queryset)

    return render(request, 'website/profile.html', {
        'user_profile': user_obj.profile,
        'user_recipes': user_recipes,
        'total_likes': total_likes,
        'is_own_profile': is_own_profile,
        'liked_page': False,
    })


def profile_liked(request, username):
    user_obj = get_object_or_404(User, username=username)
    is_own_profile = request.user == user_obj

    liked_queryset = user_obj.liked_recipes.all().order_by('-date')
    paginator = Paginator(liked_queryset, 6)
    page_number = request.GET.get('page')
    liked_recipes = paginator.get_page(page_number)
    created_recipe_count = Recipe.objects.filter(poster=user_obj).count()

    total_likes = sum(recipe.likes.count() for recipe in Recipe.objects.filter(poster=user_obj))

    return render(request, 'website/liked.html', {
        'user_profile': user_obj.profile,
        'liked_recipes': liked_recipes,
        'total_likes': total_likes,
        'is_own_profile': is_own_profile,
        'liked_page': True,
        'created_recipe_count': created_recipe_count,  
    })


def tags_view(request):
    query = request.GET.get('tags', '')  # Get search query from URL parameters
    recipes = Recipe.objects.all().order_by('-date') 

    if query:
        tags = query.split("|")
        for tag in tags:
            recipes = recipes.filter(tags__name__icontains=tag)  # Filter recipes by tag name

    paginator = Paginator(recipes, 6)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'recipes': page_obj,
        'query': query,
        'tags': serializers.serialize("json", Tag.objects.all())
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

        return HttpResponse(reverse('website:view_recipe', kwargs={'recipe_id': recipe.pk}), status=201)  # return the recipe page url

    return render(request, 'website/create_recipe.html', {'tags': serializers.serialize("json", Tag.objects.all())})

@login_required
def edit_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    print(recipe.instructions.split("\n"))
    if (recipe.poster != request.user):
        return redirect(reverse('website:view_recipe', kwargs={'recipe_id': recipe_id}), status=401)

    if request.method == 'POST':
        newTitle = request.POST["title"][0:128]
        newDescription = request.POST["description"][0:512]

        recipe.title = newTitle
        recipe.description=newDescription
        recipe.ingredients=request.POST["ingredients"]
        recipe.instructions=request.POST["instructions"]
        if (len(request.FILES) > 0):
            recipe.picture=request.FILES["picture"]
        
        recipe.save()
        
        tags = request.POST["tags"].split(",")
        for tag in tags:
            if tag == "":
                continue
            else:
                recipe.tags.add(Tag.objects.get(pk=int(tag)))

        return HttpResponse(reverse('website:view_recipe', kwargs={'recipe_id': recipe_id}), status=201) # return the recipe page url

    return render(request, 'website/edit_recipe.html', 
                  {'recipe': recipe, 
                   'tags': serializers.serialize("json", Tag.objects.all()), 
                   'ingredients': recipe.ingredients.split("\n"),
                   'instructions': recipe.instructions.split("\n"),
                   'recipetags': serializers.serialize("json", recipe.tags.all())})

  
@login_required
def edit_profile(request):
    user_profile = request.user.profile  #get profile
    context = {}

    if request.method == 'POST':  
        username = request.POST.get("new_username") #new username
        new_password = request.POST.get('new_password') #new password
        old_password = request.POST.get('old_password')
        bio = request.POST.get('bio')
        new_picture = request.POST.get('new_picture')
        action = request.POST.get('action')  # Action checker to allow changing only one part

        if action == 'change_username':
            if username != request.user.username: #check its a different username 
                if not User.objects.filter(username=username).exists():   #check if username is free
                    request.user.username = username
                    request.user.save()  
                    return redirect('website:profile', username=username)
                else:
                    context["username_error"] = True
                    context["username_error_message"] = "That username is already taken. Please choose another username."
                    context["badusername"] = username
            else:
                context["username_error"] = True
                context["username_error_message"] = "That is already your username."
                context["badusername"] = username
    
        elif action == 'change_password':
            if check_password(old_password, request.user.password): #Check old password
                request.user.set_password(new_password)  # Set new password
                request.user.save()
                request.session['password_changed'] = True
                return redirect(reverse('website:login'))
            else:
                context["password_error"] = True

        elif action == 'save_profile':  #Profile Save
            user_profile.bio = bio
            if (new_picture == "true"):
                user_profile.picture = request.FILES["picture"]
            user_profile.save()  
            return HttpResponse(reverse('website:profile', kwargs={'username': request.user.username}), status=201)

    context['user'] = request.user

    return render(request, 'website/edit_profile.html', context)

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
        comments = recipe.comments.all().order_by('-date') 
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
