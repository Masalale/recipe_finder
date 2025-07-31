# Use python 3.13 slim as our base image
FROM python:alpine

# Goes to the program directory
WORKDIR /app

# Copy the dependencies
COPY requirements.txt .

# Install program dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the program
COPY . .

# Set environment variable via build-arg
ARG SPOONACULAR_API_KEY
ENV SPOONACULAR_API_KEY=$SPOONACULAR_API_KEY

# Command to run the program in interactive mode
CMD ["python", "-u", "main.py"]

