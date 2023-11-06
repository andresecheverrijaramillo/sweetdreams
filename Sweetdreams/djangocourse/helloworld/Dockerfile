FROM python:3.8

# Create app directory
WORKDIR /usr/src/app

# Copy the Django app source to the working directory
COPY . .

# Install Requirements
RUN pip install -r requirements.txt

# Expose the required port
EXPOSE 8000

# Specify the command to run the Django app
CMD ["sudo python3 manage.py runserver 0.0.0.0:8000"]