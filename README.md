🍽️ Restaurant Booking System
📌 Overview

The Restaurant Booking System is a full-stack web application built using Django that allows users to create accounts, book tables, manage reservations, and view booking history.

The application is designed to simulate a real-world restaurant reservation system with user authentication, table allocation logic, and data validation.

🎯 Project Goals
Provide users with an easy way to book restaurant tables
Prevent double bookings through backend logic
Allow users to manage (edit/cancel) their reservations
Ensure data integrity with strong validation
Deliver a clean and user-friendly interface
👤 User Stories
As a user, I want to:
Create an account so I can manage bookings
Log in and log out securely
Book a table for a specific date and time
View my reservations
Edit my reservation if plans change
Cancel my booking if needed
🚀 Features
🔐 Authentication
User registration (signup)
Login/logout functionality
Only authenticated users can make bookings
📅 Booking System
Book tables based on:
Date
Time
Number of guests
Automatic table assignment based on availability
🔄 Reservation Management
View all personal reservations
Edit (reschedule) bookings
Cancel bookings
Cancelled bookings free up table availability
🧠 Validation & Logic
Prevent booking in the past
Prevent booking earlier times on the same day
Limit guest numbers (1–12)
Prevent editing cancelled reservations
Prevent double booking using confirmed status filtering
🎨 User Interface
Clean navigation bar
Card-based reservation display
Status badges (Confirmed / Cancelled)
Flash messages for feedback
Responsive layout
🗄️ Database Structure
Models Used:
User (Django built-in)
Client
Linked to User
Stores personal details
Table
Table number
Capacity
Reservation
Client (ForeignKey)
Table (ForeignKey)
Date
Time
Guests
Status (Confirmed / Cancelled)
🧪 Testing
Manual Testing
Feature	Test Action	Expected Result	Pass
Signup	Valid data	Account created	✅
Login	Correct credentials	Login successful	✅
Booking	Valid input	Reservation created	✅
Booking	Past date	Error shown	✅
Booking	Past time	Error shown	✅
Booking	Too many guests	Error shown	✅
Edit Booking	Change details	Updated successfully	✅
Cancel Booking	Click cancel	Status updated	✅
Rebooking	Cancel then rebook	Table available again	✅
Security	Access other user data	Blocked	✅
Validation Testing
Past date booking blocked
Past time booking blocked
Guest limits enforced
Cancelled bookings cannot be edited
Only confirmed bookings block tables
Browser Testing

Tested on:

Google Chrome ✅
Microsoft Edge ✅
🐞 Bugs & Fixes
Bug	Fix
Admin duplicate registration	Removed duplicate model registration
NoReverseMatch errors	Corrected URL names
CSS not loading	Fixed static file linking
Edit cancelled booking	Added backend validation
Table not freeing after cancel	Filtered by confirmed bookings only
🌐 Validation
HTML Validation

W3C Validator was used to validate HTML.

⚠️ Note: Django template syntax such as {% url %} may show warnings, which is expected and does not affect functionality.

## Validation

### HTML Validation
![W3C HTML Validation](assets/images/html-validation.png)

### CSS Validation
![CSS Validation](assets/images/css-validation.png)

🚀 Deployment
Local Deployment
Clone repository:
git clone <https://github.com/OviO17/restaurant-booking-system>
Navigate to project:
cd restaurant-booking
Create virtual environment:
python -m venv venv
Activate environment:
.\venv\Scripts\Activate.ps1
Install dependencies:
pip install -r requirements.txt
Run migrations:
python manage.py migrate
Run server:
python manage.py runserver