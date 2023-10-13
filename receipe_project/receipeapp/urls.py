# urls.py
from django.urls import path
from . import views
from .views import RecipeListView, RecipeCreateView, RecipeSearchView,  RecipeUpdateView,RecipeRatingListView

urlpatterns = [
    path('recipes/', RecipeListView.as_view(), name='recipe-list'),
    path('recipes/create/', RecipeCreateView.as_view(), name='recipe-create'),
    path("",views.Receipe_list,name='list-recipe'),
    path('create/',views.Receipe_create,name='create_recipe'),
    path('recipe/search/',RecipeSearchView.as_view(),name='search'),
    path('search/',views.search_items,name='search-item'),
    path('recipes/detail/<int:pk>/',views.RecipeDetailView.as_view(),name='detail_view'),
    path('detail-page/<int:recipe_id>/',views.Detail_view,name='detail'),
    path('recipes/update/<int:pk>/', RecipeUpdateView.as_view(), name='recipe-update'),
    path('update/<int:recipe_id>/',views.Update_view,name='update'),
    path('recipes/delete/<int:pk>/', views.RecipeDeleteView.as_view(), name='recipe-delete'),
    path('delete/<int:recipe_id>/', views.delete_view, name='delete'),
    path('ratings/', RecipeRatingListView.as_view(), name='rating-list'),
    path('rating/<int:recipe_id>',views.Rating_page,name='rating')



]
