from django.urls import path
from website import views

app_name = 'website'

urlpatterns = [
path('', views.home, name='home'),
path('register/', views.register, name='register'),
path('login/', views.user_login, name='login'),
path('logout/', views.user_logout, name='logout'),
path('tags/', views.tags_view, name='tags'),
path('profile/', views.profile, name='profile'),
path('create-post/', views.create_recipe, name='create_recipe'),
path('edit_recipe/<int:recipe_id>/', views.edit_recipe, name='edit_recipe'),
path('delete-account/', views.delete_account, name='delete_account'),

]
