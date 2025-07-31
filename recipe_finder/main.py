#!/usr/bin/env python3

"""
    This script provides a command-line interface to search for recipes by ingredients or cuisine,
    backbone of the program.
"""
import os
import sys
import time
import webbrowser
import urllib.parse
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

# Use relative imports when running as script
try:
    from recipe_finder import api_client, utils
except ModuleNotFoundError:
    import api_client
    import utils

console = Console()

def clear_screen():
    """Clears the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def display_recipes(recipes):
    """Display a list of recipes in a table, sorted by difficulty."""
    if not recipes:
        console.print("[bold red]No recipes found.[/bold red]")
        return

    # Sort recipes by difficulty: Easy, Medium, Hard
    recipes.sort(key=lambda r: ("Easy", "Medium", "Hard").index(utils.calculate_difficulty(r)))

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("ID", style="dim", width=5)
    table.add_column("Recipe", style="bold")
    table.add_column("Likes", style="green")
    table.add_column("Ingredients", style="cyan")

    for i, recipe in enumerate(recipes):
        likes = recipe.get('aggregateLikes', 'N/A')
        ingredients_count = len(recipe.get('extendedIngredients', []))
        # Handle all the formats we might get from the API
        if ingredients_count == 0 and 'usedIngredientCount' in recipe:
             ingredients_count = recipe.get('usedIngredientCount', 0) + recipe.get('missedIngredientCount', 0)

        table.add_row(
            str(i + 1),
            recipe["title"],
            str(likes),
            f"{ingredients_count} ingredients"
        )
    console.print(table)

def search_by_ingredients():
    """Let users search for recipes using ingredients they already have."""
    clear_screen()
    console.print(Panel("[bold cyan]Search Recipes by Ingredients[/bold cyan]", expand=False, border_style="green"))
    console.print("Enter ingredients separated by commas (e.g., chicken, rice, tomatoes).")
    ingredients_str = console.input("[bold yellow]Ingredients: [/bold yellow]")
    if not ingredients_str:
        console.print("[bold red]Input cannot be empty.[/bold red]")
        console.input("Press Enter to return to the main menu...")
        return

    ingredients = [ing.strip() for ing in ingredients_str.split(',')]
    
    # Check if we already looked this up before
    cache_key = f"ingredients_{','.join(sorted(ingredients))}"
    cached_recipes = utils.get_from_cache(cache_key)

    if cached_recipes:
        recipes = cached_recipes
        console.print("[italic green]Loading recipes from cache...[/italic green]")
    else:
        with console.status("[bold green]Searching for recipes...[/bold green]"):
            recipes_summary = api_client.search_recipes_by_ingredients(ingredients)
            recipes = []
            if recipes_summary:
                # We need full details for sorting and display
                with console.status("[bold green]Fetching recipe details...[/bold green]"):
                    for r in recipes_summary:
                        details = api_client.get_recipe_details(r['id'])
                        if details:
                            recipes.append(details)
                utils.set_in_cache(cache_key, recipes)

    if recipes:
        display_recipes(recipes)
        select_recipe_flow(recipes)
    else:
        console.print("[bold red]Could not find any recipes with those ingredients.[/bold red]")
        console.input("Press Enter to return to the main menu...")

def search_by_cuisine():
    """Search for recipes by type of cuisine - Italian, Chinese, etc."""
    clear_screen()
    console.print(Panel("[bold cyan]Search Recipes by Cuisine[/bold cyan]", expand=False, border_style="green"))
    cuisines = ["Italian", "Chinese", "Mexican", "Indian", "Japanese", "Thai", "French", "Spanish"]
    meal_types = ["main course", "dessert", "appetizer", "breakfast", "soup"]
    
    console.print("[bold cyan]Available Cuisines:[/bold cyan]", ", ".join(cuisines))
    cuisine = console.input("[bold yellow]Choose a cuisine: [/bold yellow]").lower()
    
    if cuisine not in [c.lower() for c in cuisines]:
        console.print("[bold red]Invalid cuisine.[/bold red]")
        console.input("Press Enter to return...")
        return

    console.print("[bold cyan]Available Meal Types (optional):[/bold cyan]", ", ".join(meal_types))
    meal_type = console.input("[bold yellow]Choose a meal type (or press Enter to skip): [/bold yellow]").lower()

    if meal_type and meal_type not in meal_types:
        console.print("[bold red]Invalid meal type.[/bold red]")
        console.input("Press Enter to return...")
        return

    # Same caching strategy as ingredients search
    cache_key = f"cuisine_{cuisine}_{meal_type}"
    cached_recipes = utils.get_from_cache(cache_key)

    if cached_recipes:
        recipes = cached_recipes
        console.print("[italic green]Loading recipes from cache...[/italic green]")
    else:
        with console.status("[bold green]Searching for recipes...[/bold green]"):
            data = api_client.find_recipes_by_cuisine(cuisine, meal_type)
            recipes_summary = data.get('results', []) if data else []
            recipes = []
            if recipes_summary:
                with console.status("[bold green]Fetching recipe details...[/bold green]"):
                    for r in recipes_summary:
                        details = api_client.get_recipe_details(r['id'])
                        if details:
                            recipes.append(details)
                utils.set_in_cache(cache_key, recipes)

    if recipes:
        display_recipes(recipes)
        select_recipe_flow(recipes)
    else:
        console.print("[bold red]Could not find any recipes for this cuisine.[/bold red]")
        console.input("Press Enter to return...")

def view_recipe_details(recipe):
    """Shows all the details for one recipe - ingredients, instructions, etc."""
    favorites = utils.load_favorites()
    is_favorite = any(fav['id'] == recipe['id'] for fav in favorites)

    while True:
        clear_screen()
        console.print(Panel(f"[bold cyan]{recipe['title']}[/bold cyan]", expand=False, border_style="green"))

        # Show basic info first
        info_table = Table(show_header=False, box=None)
        info_table.add_row("Time:", f"{recipe.get('readyInMinutes', 'N/A')} minutes")
        info_table.add_row("Servings:", str(recipe.get('servings', 'N/A')))
        cuisines_list = recipe.get('cuisines', [])
        cuisines_str = ", ".join(cuisines_list) if cuisines_list else 'N/A'
        info_table.add_row("Cuisine:", cuisines_str)
        info_table.add_row("Source:", recipe.get('sourceName', 'N/A'))
        console.print(info_table)

        # Show nutrition info if we have it
        if 'nutrition' in recipe:
            nutrition_info = utils.parse_nutritional_info(recipe['nutrition'])
            health_panel = Panel(
                f"[bold]Calories:[/bold] {nutrition_info['calories']}\n"
                f"[bold]Score:[/bold] {nutrition_info['nutrition_score']}/100\n"
                f"[bold]Metrics:[/bold] {', '.join(nutrition_info['health_metrics'])}",
                title="[bold]Health Info[/bold]",
                border_style="yellow"
            )
            console.print(health_panel)

        # List out all the ingredients
        ingredients_table = Table(title="[bold]Ingredients[/bold]")
        ingredients_table.add_column("Amount")
        ingredients_table.add_column("Name")
        for ing in recipe.get('extendedIngredients', []):
            amount_str = utils.format_ingredient_amount(ing.get('amount'))
            ingredients_table.add_row(f"{amount_str} {ing['unit']}", ing['name'])
        console.print(ingredients_table)

        # Clean up the instructions and number them properly
        instructions = recipe.get('instructions', 'No instructions available.')
        if instructions:
            instructions = instructions.replace('<ol>', '').replace('</ol>', '').replace('<li>', '').replace('</li>', '\n')
            steps = [f"{i+1}. {step.strip()}" for i, step in enumerate(instructions.split('\n')) if step.strip()]
            instructions_text = "\n".join(steps)
        else:
            instructions_text = 'No instructions available.'
        console.print(Panel(instructions_text, title="[bold]Instructions[/bold]"))

        # Give user some options for what to do next
        console.print("\n--- Options ---")
        fav_action = "Remove from favorites" if is_favorite else "Save to favorites"
        console.print(f"1. {fav_action}")
        console.print("2. Share recipe")
        console.print("0. Return to previous menu")
        
        choice = console.input("[bold yellow]Enter your choice: [/bold yellow]")

        if choice == '1':
            if is_favorite:
                favorites = [fav for fav in favorites if fav['id'] != recipe['id']]
                # Clean up the cache when removing recipe from favorites
                details_key = f"details_{recipe['id']}"
                if details_key in utils.api_cache:
                    del utils.api_cache[details_key]
                console.print("[bold green]Recipe removed from favorites![bold green]")
            else:
                favorites.append(recipe)
                console.print("[bold green]Recipe saved to favorites![bold green]")
            utils.save_favorites(favorites)
            is_favorite = not is_favorite
            time.sleep(1)
        elif choice == '2':
            share_recipe(recipe)
        elif choice == '0':
            break
        else:
            console.print("[bold red]Invalid choice.[/bold red]")
            time.sleep(1)

def select_recipe_flow(recipes):
    """Allow user to select a recipe to see details."""
    while True:
        console.print("\n--- Options ---")
        console.print("Enter a recipe number (1-7) to view details.")
        console.print("0. Return to main menu")
        
        choice = console.input("[bold yellow]Enter your choice: [/bold yellow]")
        if choice.isdigit():
            choice_num = int(choice)
            if 0 < choice_num <= len(recipes):
                view_recipe_details(recipes[choice_num - 1])
                # After returning from details, redisplay the list
                clear_screen()
                display_recipes(recipes)
            elif choice_num == 0:
                break
            else:
                console.print("[bold red]Invalid recipe number.[/bold red]")
        else:
            console.print("[bold red]Please enter a number.[/bold red]")

def view_favorites():
    """Displays the list of favorite recipes."""
    while True:
        clear_screen()
        console.print(Panel("[bold cyan]Favorite Recipes[/bold cyan]", expand=False, border_style="green"))
        favorites = utils.load_favorites()
        if not favorites:
            console.print("[bold red]You have no favorite recipes yet.[/bold red]")
            console.input("Press Enter to return to the main menu...")
            return
        display_recipes(favorites)
        
        # Show options before selecting a recipe
        console.print("\n--- Options ---")
        console.print("Enter a recipe number to view details.")
        console.print("0. Return to main menu")
        
        choice = console.input("[bold yellow]Enter your choice: [/bold yellow]")
        if choice.isdigit():
            choice_num = int(choice)
            if 0 < choice_num <= len(favorites):
                view_recipe_details(favorites[choice_num - 1])
                # Reload favorites in case the user removed any
                favorites = utils.load_favorites()
                if not favorites:
                    clear_screen()
                    console.print(Panel("[bold cyan]Favorite Recipes[/bold cyan]", expand=False, border_style="green"))
                    console.print("[bold red]You have no favorite recipes yet.[/bold red]")
                    console.input("Press Enter to return to the main menu...")
                    return
                # Show the updated list
                clear_screen()
                console.print(Panel("[bold cyan]Favorite Recipes[/bold cyan]", expand=False, border_style="green"))
                display_recipes(favorites)
            elif choice_num == 0:
                break
            else:
                console.print("[bold red]Invalid recipe number.[/bold red]")
                time.sleep(1)
        else:
            console.print("[bold red]Please enter a number.[/bold red]")
            time.sleep(1)

def share_recipe(recipe):
    """Displays a menu to share a recipe on different platforms."""
    source_url = recipe.get('sourceUrl', '')
    title = recipe['title']
    summary = recipe.get('summary', 'No description available.')
    # Strip out HTML tags to make the text cleaner
    summary = summary.replace('<b>', '').replace('</b>', '')

    if not source_url:
        console.print("[bold red]Sorry, no shareable link available for this recipe.[/bold red]")
        time.sleep(2)
        return

    while True:
        clear_screen()
        console.print(Panel(f"Share: [bold cyan]{title}[/bold cyan]", border_style="green"))
        console.print("1. Share on Facebook")
        console.print("2. Share on Twitter")
        console.print("3. Share on WhatsApp")
        console.print("4. Share via Email")
        console.print("0. Back to recipe")

        choice = console.input("[bold yellow]Choose a platform: [/bold yellow]")

        url = ""
        if choice == '1':
            url = f"https://www.facebook.com/sharer/sharer.php?u={source_url}"
        elif choice == '2':
            url = f"https://twitter.com/intent/tweet?url={source_url}&text={title}"
        elif choice == '3':
            url = f"https://api.whatsapp.com/send?text={title}%20{source_url}"
        elif choice == '4':
            # Build a nice email with recipe info
            subject = urllib.parse.quote(title)
            ready_in_minutes = recipe.get('readyInMinutes', 'N/A')
            cuisines_list = recipe.get('cuisines', [])
            cuisine_str = cuisines_list[0] if cuisines_list else "delicious"
            body_content = (
                f"Check out this {cuisine_str} recipe for '{title}'!\n"
                f"It's ready in just {ready_in_minutes} minutes.\n\n"
                f"Get the full recipe here: {source_url}"
            )
            body = urllib.parse.quote(body_content, safe='')
            url = f"mailto:?subject={subject}&body={body}"
        elif choice == '0':
            break
        else:
            console.print("[bold red]Invalid choice.[/bold red]")
            time.sleep(1)
            continue
        console.print(f"Opening share link in your browser...")
        webbrowser.open(url)
        time.sleep(1)
        console.input("Press Enter to continue...")

def main_menu():
    """Displays the main menu and handles user input."""
    while True:
        clear_screen()
        console.print(Panel("[bold cyan]Recipe Finder & Meal Planner[/bold cyan]", expand=False, border_style="green"))
        console.print("1. Search recipes by ingredients")
        console.print("2. Search recipes by cuisine")
        console.print("3. View favorite recipes")
        console.print("4. Exit")
        
        choice = console.input("[bold yellow]Enter your choice: [/bold yellow]")
        
        if choice == '1':
            search_by_ingredients()
        elif choice == '2':
            search_by_cuisine()
        elif choice == '3':
            view_favorites()
        elif choice == '4':
            console.print("[bold red]Exiting the application. Goodbye![/bold red]")
            break
        else:
            console.print("[bold red]Invalid choice, please try again.[/bold red]")
            time.sleep(1)

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        console.print("\n\n[bold red]Application interrupted by user. Goodbye![/bold red]")
        sys.exit(0)
