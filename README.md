# Recipe Finder

A command-line application that discovers and manage recipes found from the Spoonacular API. This tool allows users to search for recipes based on ingredients they have or cuisine, save their favorite recipes for future use, and even share these recipes.

## Features

- Search for recipes by ingredients.
- Search for recipes by cuisine.
- Save favorite recipes locally.
- View a list of saved favorite recipes.
- Share recipies with on socials (Facebook, Twitter, WhatsApp, and Email). # Works only when running locally in your machine ;)

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

2.  **Get a Spoonacular API Key:**
- Go to [Spoonacular API](https://spoonacular.com/food-api/console#Dashboard)
- Sign up for a free account
- You'll receive an email from the Spoonacular team, click accept
- Login to your account
- Head on to the Profile & API Key
- Click on Show/Hide key and copy it manually form the site

3.  **Set up environment variables:**
    Create a `.env` file in the root of the project and add your Spoonacular API key:
    ```
    SPOONACULAR_API_KEY='your_api_key_here'
    ```

## Usage

To run the application, execute the `main.py` script:
Make sure you are in the recipie_finder directory

```bash
  python main.py
```

You will be presented with a main menu for program interaction.

## Deployment

This section outlines the steps for containerizing and deploying the application.

### 1. Dockerization

A `Dockerfile` is provided to containerize the application.
Make sure you have docker installed on your device.

**Build the Docker image:**
```bash
  docker build --build-arg SPOONACULAR_API_KEY=your_api_key_here -t recipe-finder .
```

**Run the Docker container:**
```bash
  docker run -it recipe-finder
```

### 2. Docker Hub

If you want to use my docker image form docker hub.

- Image name: `masalale/recipe-finder:v1.3`
- Link: [Docker Hub Repository](https://hub.docker.com/r/masalale/recipe-finder)


**Pull the image:**
```bash
  docker pull masalale/recipe-finder:v1.3
```

**Run the container:**
```bash
  docker run -it masalale/recipe-finder:v1.3
```
## Deployment Constraints

Due to lab instance constraints, deployment was demonstrated using multiple Docker containers:
- Instance 1 (web01 simulation): Successfully deployed and tested.
- Instance 2 (web02 simulation): Successfully deployed and tested.
This apporiach demonstrated the program works correctly inmultiple indipendent environmnets.

### Deployment Screenshots:

### Load Balancer

As a CLI application users can directly interact with the program throught the terminal, which renders the work of a load balance inapplicable. Load balancers are designed for web applications that handle HTTP requests, not for CLI tools.
Hence this application demonstrated deployment on multiple environments, which satisft the multi-server requirement of the assignment.

## API Attribution

This application uses the `Spoonacular API` for recipies data. Usage of this APU is subject Spoonacular's terms and conditions.

### Security

- API keys are stored in environment variables and not hardcoded
- Sensititve data is not commited to the repository
- Docker build uses build arguments to safely inject the API key.
