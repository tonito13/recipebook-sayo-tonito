from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView

from .models import Recipe, RecipeImage
from .forms import RecipeForm, RecipeImageForm

class RecipeListView(ListView):
    model = Recipe
    template_name = 'recipe_list.html'

class RecipeDetailView(LoginRequiredMixin, DetailView):
    model = Recipe
    template_name = 'recipe_detail.html'
    redirect_field_name = 'object'

def recipe_list(request):
    recipes = Recipe.objects.all()
    ctx = {
        "recipes" : recipes
    }
    return render(request, 'recipe_list.html', ctx)

def recipe_detail(request, pk):
    ctx = {
        "recipe" : Recipe.objects.get(pk=pk)
    }
    return render(request, 'recipe_detail.html', ctx)

def add_recipe(request):
    form = RecipeForm()

    if request.method == "POST":
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect(reverse('ledger:recipes-list'))
        else:
            form = RecipeForm()
            
    ctx = {'form': form}

    return render(request, 'add_recipe.html', ctx)

def add_image(request, pk):
    recipe = Recipe.objects.get(pk=pk)
    form = RecipeImageForm()

    if request.method == "POST":
        form = RecipeImageForm(request.POST, request.FILES)
        if form.is_valid():
            recipe_image = form.save(commit=False) 
            recipe_image.recipe = recipe 
            recipe_image.save()  
            return redirect(reverse('ledger:recipe-detail', args=[pk]))
    ctx = {
        'form': form,
        'object': recipe
    }

    return render(request, 'add_image.html', ctx)
