FROM python:3.9-alpine

# Install SQLite and other required dependencies
RUN apk --no-cache add sqlite

# Set the working directory
WORKDIR /app 

# Copy requirements.txt file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy your SQLite database file into the container
COPY ntsoekhe.db .

# Copy the application code into the container
COPY app.py .
COPY create_patient.html .

# Expose the port on which the API will run
#EXPOSE 80

# Command to run when the container starts
CMD ["python", "app.py", "--host=0.0.0.0"]