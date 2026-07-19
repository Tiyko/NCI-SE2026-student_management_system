# Student Event Management System (NCI - ANI - Software Engineering)
 
run " docker compose up --build " to compose image and then use link http://localhost:8080/ to view website
 
## Introduction
 
The student event management system is designed and created by the ANI group consisting of Aidas Kibas, Nerijus Kmitas, and Ionut Ciobanu. The core principal of the application is that the user can sign up, browse events, book an event they are interested in, and then attend the event without having to constantly communicate with somebody over the details of the event. Event organisers and admin can create and manage events.
 
The website is built using the Django framework, containerised with Docker, hosted on a free-tier PostgreSQL database (Neon), and follows an agile methodology approach for development using Jira for sprint tracking.

This application is only a prototype and does not include major functions such as a payment method.
 
## Table of Contents
 
- [Introduction](#introduction)
- [User Experience](#user-experience)
    - [Project Goal](#project-goal)
    - [User Stories](#user-stories)
    - [Scope](#scope)
    - [Agile Methodology](#agile-methodology)
- [Design](#design)
    - [Use Case Diagram](#use-case-diagram)
    - [Database Schema](#database-schema)
- [Features](#features)
- [Future Features](#future-features)
- [Testing](#testing)
- [Technologies Used](#technologies-used)
- [Python Packages](#python-packages)
- [Deployment](#deployment)
    - [Docker Setup](#docker-setup)
    - [Database Hosting (Neon)](#database-hosting-neon)
    - [Fork Repository](#to-fork-this-repository)
    - [Cloning](#cloning-this-project)
- [Credits](#credits)
- [Acknowledgements](#acknowledgements)
 
<br>
 
## User Experience
<br>
 
### Project Goal
 
The goal of the student event management system is to simplify event organisation and communication between organisers and students attending the events. Those who have the app can browse upcoming events and book their place.
 
### User Stories

Student:
1. I want to be able to sign up for the application and have my own account.
2. I want to login to the application using my details.
3. I want to browse available student events.
4. I want to be able to book an event i am interested in.
5. I want to be able to see my booking.
6. I want to be able to refund my booking if i am no longer attending.
7. I want to be able to log off the application.

Organiser:
1. I want to be able to create the event by entering the required information.
2. I want to be able to request an event to the admin so they can approve it.

Admin:
1. I want to be able to create the event by entering the required information.
2. I want to be able to either approve or reject incoming requests.
3. I want to be able to manage events so that i can delete completed events.
<br>
 
### Scope
 
User Registration and Authentication
- Users can create an account and log in to the website.
- Users can reset their passwords if forgotten.
- Login accepts either email or username.
 
Event Discovery and Booking
- Users can browse available basketball events without logging in.
- Users can select and join an event, subject to availability.
- Users can register their vehicle to reserve parking for a specific event.
 
Booking Management
- Users can view all their current bookings.
- Users can cancel one or multiple bookings, with confirmation prompts.
 
Event Management (Organisers Only)
- Organisers can create new events by entering event details.
- Organisers can delete existing events, protected by password confirmation.
- Deleted events are immediately removed from the public event list.
 
User Profile
- Users can view and edit their personal details, including changing their password.
- Users receive validation feedback if entered details are incorrect.
 
<br>
 
### Agile Methodology
 
The development of Hoop and Go follows an agile methodology approach using weekly sprint cycles. Each sprint focuses on delivering specific features drawn from the Requirements Specification, tracked through Jira with a rotating Scrum Master each sprint. All user stories, sprint backlogs, and progress can be accessed via our Jira board [here](https://aidaskibas17.atlassian.net/jira/software/projects/SCRUM/summary).
 
Our GitHub repository is linked to Jira so that branches, commits, and pull requests are tracked directly against their corresponding Jira issue.
 
<br>
 
## Design
 
### Use Case Diagram
 
The core functional requirements are represented by 8 use cases: Login, Register New User, Register Vehicle, Select Event, Manage Booking, Change Details, Create Event, and Delete Event, as detailed in our Requirements Specification.
 
### Database Schema
 
The core entities are User, Event, Booking, and Payment (future feature), linked as follows: a User can organise many Events, a User can make many Bookings, an Event can have many Bookings, and a Booking may generate one Payment.
 
<br>
 
## Features
 
- User registration and login (email or username)
- Password reset flow
- Browse and search available basketball events
- Join an event with real-time capacity checks
- Register a vehicle for free event parking
- View and manage (cancel) bookings
- Edit personal account details
- Organiser-only event creation and deletion, password-protected
- **Stripe payment integration** for paid events, allowing organisers to charge entry fees and users to pay securely at checkout.
- "Every 10th event free" loyalty incentive once payments are introduced.
 
<br>
 
## Future Features
 
<br>
 
## Testing
<br>
 
## Technologies Used
 
- Python
- Django
- PostgreSQL (hosted on Neon)
- Docker & Docker Compose
- django-allauth (authentication)
- Bootstrap 5 (via django-crispy-forms)
- GitHub (version control)
- Jira (sprint planning and issue tracking)
 
<br>
 
## Python Packages
 
- Django
- django-allauth
- django-crispy-forms
- dj-database-url
- psycopg2-binary
- python-decouple
- gunicorn
 
<br>
 
## Deployment
 
### Docker Setup
 
This project runs inside Docker for consistent environments across all team members' machines.
 
1. Clone the repository (see below).
2. Create a `.env` file at the project root using `.env.example` as a template.
3. Run `docker compose build` followed by `docker compose up`.
4. Run migrations: `docker compose exec web python manage.py migrate`.
5. Create a superuser: `docker compose exec web python manage.py createsuperuser`.
6. Visit `http://localhost:8080` to view the running application.
 
### Database Hosting (Neon)
 
The project's PostgreSQL database is hosted for free on [Neon](Neon — Postgres backends for apps and agents). All team members connect to the same shared database via a `DATABASE_URL` environment variable, kept out of version control via `.gitignore`.
 
### To Fork This Repository
 
1. Log in to GitHub.
2. Navigate to the repository page.
3. Click the "Fork" button in the top right.
 
### Cloning This Project
 
1. Log in to GitHub.
2. Navigate to the repository page.
3. Click "Code" and copy the HTTPS URL.
4. Open a terminal and run `git clone <copied-url>`.
 
<br>
 
## Credits
 
- Aidas Kibas
- Michal Pokojny
- Nerijus Kmitas
- Ionut Ciobanu
 
<br>
 
## Acknowledgements
 
- National College of Ireland, Team Project module, lectured by Sumit Tripathi.
 
Jira
 
