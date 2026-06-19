from django.shortcuts import render, reverse


DATA = {
    'omlet': {
        'яйца, шт': 2,
        'молоко, л': 0.1,
        'соль, ч.л.': 0.5,
    },
    'pasta': {
        'макароны, г': 0.3,
        'сыр, г': 0.05,
    },
    'buter': {
        'хлеб, ломтик': 1,
        'колбаса, ломтик': 1,
        'сыр, ломтик': 1,
        'помидор, ломтик': 1,
    },
    # можете добавить свои рецепты ;)
}

def home_view(request):
    template_name = 'calculator/home.html'

    pages = {
        'Омлет': reverse('recipe_view', kwargs={'recipe_name': 'omlet'}),
        'Паста': reverse('recipe_view', kwargs={'recipe_name': 'pasta'}),
        'Бутерброд': reverse('recipe_view', kwargs={'recipe_name': 'buter'})
    }
    
    context = {
        'pages': pages
    }
    return render(request, template_name, context)

def recipe_view(request, recipe_name):
    # Получаем количество порций из GET-запроса (например, /omlet/?servings=5)
    # Если параметр не передан, по умолчанию берем 1 порцию
    servings = int(request.GET.get('servings', 1))
    
    # Достаем рецепт из нашего словаря DATA
    recipe = DATA.get(recipe_name)
    
    context = {}
    if recipe:
        # Умножаем количество каждого ингредиента на количество порций
        scaled_recipe = {ingredient: amount * servings for ingredient, amount in recipe.items()}
        context['recipe'] = scaled_recipe

    return render(request, 'calculator/index.html', context)
