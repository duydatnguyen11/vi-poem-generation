# Use a lightweight Python base image
FROM python:3.9-slim 

# Create a non-root user
RUN groupadd -r mlk2 && useradd -r -g mlk2 project1

# Set working directory in the container
WORKDIR /app

# Define virtual environment
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV

# Install build dependencies
# RUN apt-get update && apt-get install -y --no-install-recommends build-essential

# Copy and install dependencies
COPY ./requirements.txt /app
RUN $VIRTUAL_ENV/bin/pip install --upgrade pip && $VIRTUAL_ENV/bin/pip install -r requirements.txt

# Copy the poem app to workspace
COPY /app   /app

# Set ownerships and permissions for the app directory
RUN chown -R project1:mlk2 /app 
RUN chmod -R 755 /app  

# Create the home directory and set ownership
RUN mkdir -p /home/project1 && chown -R project1:mlk2 /home/project1 

# Switch to the non-root user
USER project1

# Activate virtual environment
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Expose port for documentation purposes
EXPOSE 30000

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "30000"]
