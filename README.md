# Restaurant Booking System

## Overview

The Restaurant Booking System is a full-stack web application built using Django that allows users to create accounts, book tables, manage reservations, and view booking history.

The application simulates a real-world restaurant reservation system with user authentication, table allocation logic, and strong data validation.

---

## Live Project

https://restaurant-booking-system-kell.onrender.com
---

## User Experience (UX)

### Design Goals

- Simple and intuitive booking process  
- Clear navigation between pages  
- Immediate feedback through messages  
- Clean and readable layout  

### User Flow

1. User signs up or logs in  
2. User books a table  
3. User views reservations  
4. User edits or cancels booking  

---

## Technologies Used

### Languages
- Python  
- HTML  
- CSS  

### Frameworks & Libraries
- Django  
- Gunicorn  
- WhiteNoise  

### Database
- PostgreSQL (Render)

### Tools & Platforms
- Git & GitHub  
- Render (deployment)  
- VS Code  

---

## Agile Planning

This project was planned using user stories to guide development.

Key user stories included:
- User can create an account  
- User can log in and log out  
- User can book a table  
- User can edit a reservation  
- User can cancel a reservation  

Development was completed in stages, focusing on:

1. Authentication  
2. Booking system  
3. Reservation management  
4. Validation and UI improvements  

---

## Features

### Authentication

- User registration  
- Login and logout functionality  
- Only authenticated users can access booking features  

### Booking System

- Book tables by date, time, and number of guests  
- Automatic table assignment based on availability  
- Prevents double bookings  

### Reservation Management

- View personal reservations  
- Edit bookings  
- Cancel bookings  
- Cancelled bookings free up table availability  

### Validation and Logic

- Prevents past date bookings  
- Prevents past time bookings on the same day  
- Limits guest numbers from 1 to 12  
- Prevents editing cancelled reservations  
- Only confirmed bookings block table availability  

### User Interface

- Navigation bar  
- Card-style reservation display  
- Status indicators  
- Feedback messages  
- Responsive layout  

---

## Screenshots

### Home Page  
![Home](assets/images/home.png)

### Booking Page  
![Booking](assets/images/booking.png)

### Reservations Page  
![Reservations](assets/images/reservations.png)

---

## Database Structure

### Models

#### User  
Django built-in authentication model  

#### Client  
- Linked to User  
- Stores personal details  

#### Table  
- Table number  
- Capacity  

#### Reservation  
- Client (ForeignKey)  
- Table (ForeignKey)  
- Date  
- Time  
- Guests  
- Status (Confirmed / Cancelled)  

---

## Testing

Testing was carried out manually across all core features to ensure functionality, validation, and user security.

### Manual Testing

| Feature | Test Action | Expected Result | Result |
|--------|------------|---------------|--------|
| Signup | Valid data | Account created | Pass ✅ |
| Login | Correct credentials | Login successful | Pass ✅ |
| Booking | Valid input | Reservation created | Pass ✅ |
| Booking | Past date | Error shown | Pass ✅ |
| Booking | Past time | Error shown | Pass ✅ |
| Booking | Too many guests | Error shown | Pass ✅ |
| Edit Booking | Change details | Updated successfully | Pass ✅ |
| Cancel Booking | Click cancel | Status updated | Pass ✅ |
| Rebooking | Cancel then rebook | Table available again | Pass ✅ |
| Security | Access another user data | Blocked | Pass ✅ |

### Validation Testing

- Past date booking blocked  
- Past time booking blocked  
- Guest limits enforced  
- Cancelled bookings cannot be edited  
- Only confirmed bookings block tables  

---

## Bugs and Fixes

| Bug | Fix |
|-----|-----|
| Duplicate admin registration | Removed duplicate registration |
| URL errors | Fixed URL patterns |
| Static files not loading | Configured WhiteNoise and static settings |
| Cancelled bookings editable | Added backend validation |
| Tables not freeing after cancel | Filtered by confirmed bookings only |

---

## Validation

### HTML Validation

W3C Validator was used to validate HTML.

Note: Django template syntax such as `{% url %}` may show warnings, which is expected.

![HTML Validation](assets/images/html-validation.png)

### CSS Validation

![CSS Validation](assets/images/css-validation.png)

---

## Deployment

### Local Deployment

```bash
git clone https://github.com/OviO17/restaurant-booking-system
cd restaurant-booking
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver