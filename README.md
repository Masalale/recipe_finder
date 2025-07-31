# Recipe Finder

A command-line application that discovers and manage recipes found from the Spoonacular API. This tool allows users to search for recipes based on ingredients they have or cuisine, save their favorite recipes for future use, and even share these recipes.

## Features

- Search for recipes by ingredients.
- Search for recipes by cuisine.
- Save favorite recipes locally.
- View a list of saved favorite recipes.
- Share recipies with on socials (Facebook, Twitter, WhatsApp, and Email).

## Project Structure

- `main.py`: The main entry point for the command-line interface (CLI).
- `api_client.py`: Handles all communication with the Spoonacular API.
- `utils.py`: Contains helper functions for data processing and formatting.
- `config.py`: Manages configuration, including API keys.
- `requirements.txt`: Lists the Python dependencies for the project.
- `favorites.json`: Stores the user's saved recipes.

## Local Setup

To run this application locally, follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd recipe_finder
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Set up environment variables:**
    Create a `.env` file in the root of the project and add your Spoonacular API key:
    ```
    SPOONACULAR_API_KEY='your_api_key_here'
    ```

## Usage

To run the application, execute the `main.py` script:

```bash
  python main.py
```

You will be presented with a main menu for program interaction.

## Deployment

This section outlines the steps for containerizing and deploying the application.

### 1. Dockerization

A `Dockerfile` is provided to containerize the application.

**Build the Docker image:**
```bash
  docker build -t recipe-finder .
```

**Run the Docker container:**
```bash
  docker run -it --env-file .env recipe-finder
```

### 2. Docker Hub

The image will be pushed to a public Docker Hub repository.

**Tag the image:**
```bash
  docker tag recipe-finder <your-dockerhub-username>/recipe-finder:latest
```

**Push the image:**
```bash
  docker push <your-dockerhub-username>/recipe-finder:latest
```
