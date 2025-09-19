# Step 1: Start from a specific, stable Python version.
# We use 'slim' because it's a smaller, more secure base image.
FROM python:3.9-slim

# Step 2: Set the working directory inside the container.
# This is where our application code will live.
WORKDIR /app

# Step 3: Install necessary system-level dependencies.
# 'build-essential' provides the C++ compiler tools that eth-brownie needs.
# We clean up the package manager cache afterwards to keep the image small.
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Step 4: Copy and install Python dependencies.
# We copy only the requirements file first to take advantage of Docker's layer caching.
# This means Docker won't reinstall all the libraries every time you change your code.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Step 5: Copy your application code into the container.
# This copies the contents of your local 'data_service/app' folder into the container's '/app' directory.
COPY ./app .

# Step 6: Expose the port the application will run on.
# This tells Docker that the container will listen on port 8000.
EXPOSE 8000

# Step 7: Define the command to run when the container starts.
# This starts the Uvicorn server, making the API accessible.
# '--host 0.0.0.0' is crucial to allow connections from outside the container.
CMD ["uvicorn", "data_service:app", "--host", "0.0.0.0", "--port", "8000"]

