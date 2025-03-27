from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import UserProfile, Tag, Recipe, Comment
from .forms import UserForm, RecipeForm, CommentForm
from django.utils import timezone

class ModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testuser')
        self.tag = Tag.objects.create(name='Pasta')
        self.recipe = Recipe.objects.create(
            title='Test Recipe',
            description='test recipe description.',
            ingredients='Salt, Flour, Eggs',
            instructions='Mix and boil.',
            poster=self.user,
            date=timezone.now()
        )
        self.recipe.tags.add(self.tag)
        self.comment = Comment.objects.create(text='wow', poster=self.user, recipe=self.recipe)

    def test_user_profile_creation(self):
        profile = UserProfile.objects.create(user=self.user)
        self.assertEqual(profile.user.username, 'testuser')

    def test_recipe_str(self):
        self.assertEqual(str(self.recipe), 'Test Recipe')

    def test_comment_str(self):
        self.assertEqual(str(self.comment), 'wow')
    
    def test_invalid_recipe(self):
        invalid_recipe = Recipe(title='', description='', ingredients='', instructions='', poster=self.user, date=timezone.now())
        with self.assertRaises(Exception):
            invalid_recipe.full_clean()
            invalid_recipe.save()

class FormTests(TestCase):
    def test_valid_user_form(self):
        form = UserForm(data={'username': 'Testuser', 'email': 'testuser@gmail.com', 'password': 'testuser'})
        self.assertTrue(form.is_valid())

    def test_invalid_user_form(self):
        form = UserForm(data={'username': '', 'email': 'email', 'password': ''})
        self.assertFalse(form.is_valid())
    
    def test_valid_recipe_form(self):
        form = RecipeForm(data={
            'title': 'Recipe',
            'description': 'A very nice recipe',
            'ingredients': 'Water, Cheese, Salt',
            'instructions': 'Mix all ingredients then cook'
        })
        self.assertTrue(form.is_valid())
    
    def test_invalid_recipe_form(self):
        form = RecipeForm(data={'title': '', 'description': '', 'ingredients': '', 'instructions': ''})
        self.assertFalse(form.is_valid())

class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testuser')
        self.profile = UserProfile.objects.create(user=self.user)
        self.recipe = Recipe.objects.create(
            title='Test Recipe',
            description='test recipe description.',
            ingredients='Water, Flour, Eggs',
            instructions='Put ingredients together then cook',
            poster=self.user,
            date=timezone.now()
        )
    
    def test_home_view(self):
        response = self.client.get(reverse('website:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'website/home.html')

    def test_profile_view(self):
        response = self.client.get(reverse('website:profile', args=['testuser']))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'website/profile.html')

    def test_create_recipe_if_not_logged_in(self):
        response = self.client.get(reverse('website:create_recipe'))
        self.assertNotEqual(response.status_code, 200)
    
    def test_view_recipe(self):
        response = self.client.get(reverse('website:view_recipe', args=[self.recipe.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'website/recipe_view.html')
    
    def test_view_nonexistent_recipe(self):
        response = self.client.get(reverse('website:view_recipe', args=[9999]))
        self.assertEqual(response.status_code, 404)
    
    def test_create_recipe_authenticated(self):
        self.client.login(username='testuser', password='testuser')
        response = self.client.get(reverse('website:create_recipe'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'website/create_recipe.html')


