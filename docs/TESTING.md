# Testing

## Automated testing

Run the complete suite from the project root:

```bash
python manage.py test
```

The suite in `bookings/tests.py` covers:

- automatic `Client` profile creation for regular users and superusers;
- the assessor-admin booking-page flow;
- native date, time, and number form controls;
- past dates, opening hours, and party-size validation;
- create, read, update, cancel, and permanent delete operations;
- releasing a table after cancellation;
- confirmation before deletion; and
- preventing one user from editing or deleting another user's reservation.

Also run Django's configuration and migration checks:

```bash
python manage.py check
python manage.py makemigrations --check --dry-run
```

## Manual acceptance tests

| Area | Steps | Expected result |
|---|---|---|
| Signup | Submit valid account and profile details | Account and linked profile are created; user is logged in |
| Invalid signup | Reuse an existing email | Inline error explains that the email already exists |
| Admin-created user | Create a superuser, log into the public site, open Book a table | Booking page opens; no signup redirect loop occurs |
| Date input | Open the booking page | A native date picker appears and dates before today are unavailable |
| Time input | Open the booking page | A native time control communicates the 12:00–22:00 range |
| Party size | Enter 0 or 13 guests | Form displays a clear 1–12 guest validation error |
| Create | Submit an available future booking | Confirmation appears and booking is listed |
| Double booking | Fill all suitable tables for one slot, then repeat | No-availability feedback appears; no duplicate is saved |
| Edit | Change the party size on an existing booking | Booking updates without treating itself as a conflict |
| Cancel | Select Cancel on a confirmed booking | Status changes to Cancelled and its table becomes available |
| Delete | Select Delete permanently, then keep reservation | Record remains |
| Delete confirmed | Select Delete permanently and confirm | Record is removed from the database and list |
| Authorisation | Request another user's edit/delete URL | Server returns 404 and the record remains unchanged |
| Responsive UI | Test at 320px, 768px, and desktop width | Navigation, forms, cards, and buttons remain readable and usable |
| Logout | Select Log out | Session ends and authenticated navigation disappears |

## Validator checks

- HTML: validate rendered pages with the W3C Nu HTML Checker.
- CSS: validate `bookings/static/bookings/css/style.css` with the W3C CSS Validator.
- Python: run a PEP 8 checker such as `pycodestyle bookings config` and document any accepted warnings.

Existing validator screenshots are stored in `assets/images/`.
