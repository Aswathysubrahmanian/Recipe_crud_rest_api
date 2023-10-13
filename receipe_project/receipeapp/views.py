from functools import reduce

from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import filters
from rest_framework import viewsets, status, generics

from rest_framework import generics
from rest_framework.generics import UpdateAPIView, DestroyAPIView
from rest_framework.response import Response
import requests

from .form import RecipeForm, RatingForm, RecipeUpdateForm
from .models import Recipe, Rating
from .serializers import RecipeSerializer, RatingSerializer, RecipeDetailSerializer

#list view
class RecipeListView(generics.ListAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

def Receipe_list(request):
    api_url = 'http://127.0.0.1:8000/recipes/'

    try:
        response = requests.get(api_url)

        if response.status_code == 200:
            api_data = response.json()
            print(api_data)

            return render(request, 'index.html', {'api_data': api_data})
        else:
            return render(request,'index.html',{'error': 'API request failed'}, status=500)

    except :

        return render(request,'index.html',{'error': 'API request failed'}, status=500)


#create view

class RecipeCreateView(generics.CreateAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


def Receipe_create(request):
    api_url = 'http://127.0.0.1:8000/recipes/create/'
    print(api_url)
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        print("form is:", form)
        if form.is_valid():
                data = {
                    'name': form.cleaned_data['name'],
                    'description': form.cleaned_data['description'],
                    'ingredients': form.cleaned_data['ingredients'],
                    'instructions': form.cleaned_data['instructions'],
                    'prep_time': form.cleaned_data['prep_time'],
                    'difficulty': form.cleaned_data['difficulty'],
                    'vegetarian': form.cleaned_data['vegetarian'],
                    'image': form.cleaned_data['image'],
                }
                form.save()
                image = request.FILES['image']
                files = {'images': (image.name, image.file, image.content_type)}

                response = requests.post(api_url, data=data, files=files)
                print(response.status_code)
                if response.status_code == 400:  # Assuming 201 indicates a successful creation

                    return redirect('list-recipe')
                else:
                    return render(request, 'create.html', {'error': 'API request failed'}, status=500)
    else:
            # Render the initial form
            form = RecipeForm()
            return render(request, 'create.html', {'form': form})
    return render(request,'create.html')





#search view


class CustomSearchFilter(filters.SearchFilter):
    search_param = 'custom_search'
    search_fields = ['name']

    def get_search_terms(self, request):
        params = request.query_params.get(self.search_param, '').split()
        return [param for param in params if param]

    def filter_queryset(self, request, queryset, view):
        search_terms = self.get_search_terms(request)
        if not search_terms:
            return queryset

        queries = Q()  # Create an empty Q object to build the query dynamically
        for term in search_terms:
            for field in self.search_fields:
                queries |= Q(**{field + '__icontains': term})

        queryset = queryset.filter(queries)
        return queryset

class RecipeSearchView(generics.ListAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    filter_backends = [CustomSearchFilter]
    search_fields = ['name']
    search_param = 'custom_search'



def search_items(request):
    query= request.POST.get('search')
    if query:
        api_url=f'http://127.0.0.1:8000/recipe/search/?search={query}'
        response = requests.get(api_url)
        if response.status_code == 200:
            api_data = response.json()
            return render(request, 'search_results.html', {"api_data": api_data})
        else:
            return render(request, 'search_results.html', {'error': 'API request failed'}, status=500)
    else:
        return render(request, 'search_results.html', {'error': 'Search query is required'}, status=400)



# Details view

class RecipeDetailView(generics.RetrieveAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeDetailSerializer

def Detail_view(request,recipe_id):
    api_url=f'http://127.0.0.1:8000/recipes/detail/{recipe_id}'
    response = requests.get(api_url)

    if response.status_code == 200:
        api_data = response.json()
        ingredients_list = api_data.get('ingredients', '').split(',')
        instruction_list = api_data.get('instructions', '').split('Step')

        return render(request, 'detailspage.html', {'api_data': api_data, 'ingredients_list': ingredients_list,'instruction_list':instruction_list})


#update view

class RecipeUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer


    def get_object(self):

            obj = self.queryset.get(pk=self.kwargs['pk'])
            return obj

def Update_view(request, recipe_id):
    api_url = f'http://127.0.0.1:8000/recipes/update/{recipe_id}/'


        # Retrieve the existing recipe data
    response = requests.get(api_url)
    existing_recipe_data = response.json()

    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
                # Create a dictionary to send the form data as multipart/form-data
            multipart_form_data = {}

                # Populate the multipart_form_data dictionary with the form data
            for key, value in form.cleaned_data.items():
                multipart_form_data[key] = value

                # Handle the image field as a file upload
            image = request.FILES['image']
            multipart_form_data['image'] = (image.name, image, image.content_type)

                # Send a PUT request to update the recipe using multipart/form-data
            response = requests.put(api_url, data=multipart_form_data, files={'image': multipart_form_data['image']})

            if response.status_code == 200:
                    return redirect('list-recipe')
            else:
                    return render(request, 'update.html', {'error': 'API request failed'}, status=500)
    else:
            # Pre-fill the form with the existing data
        form = RecipeForm(initial=existing_recipe_data)


    return render(request, 'update.html', {'form': form})


# delete view


class RecipeDeleteView(DestroyAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

def delete_view(request,recipe_id):
    if request.method == 'POST':
        api_url=f'http://127.0.0.1:8000/recipes/delete/{recipe_id}/'
        print(api_url)
        response = requests.delete(api_url)
        print(response)
        if response.status_code == 204:
            return redirect("list-recipe")
    return render(request,'delete.html')


#Rating

class RecipeRatingListView(generics.ListCreateAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer


def Rating_page(request,recipe_id):
    api_url = f'http://127.0.0.1:8000/ratings/{recipe_id}'

    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            rating = form.cleaned_data['rating']
            recipe = Recipe.objects.get(pk=recipe_id)  # Retrieve the recipe
            Rating.objects.create(recipe=recipe, rating=rating)

            # Send a rating to the API
            data = {
                'recipe_id': recipe_id,
                'rating': rating,
            }

            response = requests.post(api_url, json=data)
            if response.status_code == 201:  # Assuming 201 indicates a successful creation
                rating_data = response.json()
                print('Rating created:', rating_data)
                return redirect('detail')
            else:
                print('Failed to create the rating')
        else:
            print('Invalid form data')
    else:
        print('GET request to rating page')
    return render(request,'detailspage.html')





