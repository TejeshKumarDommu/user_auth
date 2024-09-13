# Flask/FastAPI Authentication and User Dashboard Application

This project is a Flask/FastAPI-based web application for user authentication and role-based access control, designed to work with SQLite or another lightweight database. The application has four roles: **Superadmin**, **Admin**, **Superuser**, and **User**, each with specific permissions. The app uses JWT for secure authentication and authorization.

## Features

- **User Authentication:** Secure user login system using JWT (JSON Web Tokens).
- **Role-based Access Control (RBAC):** Different permissions for each user role (Superadmin, Admin, Superuser, and User).
- **User Dashboard:** Dynamic user dashboard for users to view specific information based on their roles.
- **Database Integration:** Lightweight SQLite database for storing user credentials and roles.
- **AWS Deployment:** Application is designed to run on AWS EC2 Free Tier.
- **No JavaScript:** Frontend is built without the use of JavaScript.
  
## Project Structure

.
├── app.py             # Main application file to run the Flask/FastAPI server
├── db_setup.py        # Script to set up the database and initialize tables
├── templates/         # Folder containing HTML templates
├── static/            # Folder containing static files (CSS, images, etc.)
└── README.md          # This file


## Requirements

Python 3.8+
Flask/FastAPI
SQLite3
PyJWT

## Set up Virtual Environment

-for creating virtual environment
python -3 venv .venv

-To activate virtual environment
.venv/scripts/activate

-To deacttivate
deactivate

-First, setup the database
python db_setup.py

-To run the flask app
python app.py

Flask runs on : http://127.0.0.1:8000/

##AWS EC2 Deployment
To deploy this application to AWS EC2 Free Tier:

##Launch an EC2 Instance:

Choose a t2.micro instance type.
Use a public-facing security group to allow traffic on ports 80 (HTTP) and 22 (SSH).
SSH into the instance.
Install Required Dependencies on EC2:

sudo apt-get update
sudo apt-get install python3-pip
sudo apt-get install python3-venv


##Transfer the Application to EC2:

Use scp or other methods to transfer your project files to the instance.
Run the Application: Inside the instance, activate the virtual environment and run the application.

source venv/bin/activate
python app.py

#Access the Application:
Link: http://<EC2_PUBLIC_IP>:8000