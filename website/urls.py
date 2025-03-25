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
path('edit-post/<int:recipe_id>/', views.edit_recipe, name='edit_recipe'),
path('delete-account/', views.delete_account, name='delete_account'),
path('view-post/<int:recipe_id>/', views.view_recipe, name='view_recipe'),
path('like/<int:recipe_id>/', views.like_recipe, name='like_recipe'),
path('delete-comment/<int:comment_id>/',views.delete_comment,name='delete_comment'),
path('delete-recipe/<int:recipe_id>/', views.delete_recipe, name='delete_recipe'),
path('profile/edit/', views.edit_profile, name='edit_profile'),

]
