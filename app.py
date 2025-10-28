"""
Simple Ticket Booking Web Application
=====================================

This Flask-based application serves as a very minimal proof‑of‑concept for a
ticket booking system.  In a real‑world scenario this application would
include authentication, payment processing and a persistent database, but
those concerns are beyond the scope of this assignment.  The goal here is
to have a working web application that can be containerised, built and
deployed through an automated DevOps workflow.

Endpoints
---------

* **GET /** – Displays a welcome message.
* **GET /book** – Presents a form for booking a ticket.
* **POST /book** – Accepts form data and returns a simple confirmation.

Run this application locally with ``python app.py``.  By default it binds
to port 5000.
"""

from flask import Flask, render_template_string, request

# Create the Flask application
app = Flask(__name__)

# Basic HTML templates defined inline for simplicity
INDEX_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <title>Ticket Booking</title>
</head>
<body>
    <h1>Welcome to the Ticket Booking App</h1>
    <p>Book a ticket using the form below.</p>
    <a href="/book">Book Now</a>
</body>
</html>
"""

BOOK_FORM_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <title>Book a Ticket</title>
</head>
<body>
    <h1>Book a Ticket</h1>
    <form method="post">
        <label for="name">Name:</label>
        <input type="text" id="name" name="name" required />
        <br />
        <label for="event">Event:</label>
        <input type="text" id="event" name="event" required />
        <br />
        <label for="quantity">Number of tickets:</label>
        <input type="number" id="quantity" name="quantity" min="1" value="1" />
        <br />
        <button type="submit">Submit</button>
    </form>
    <a href="/">Back to Home</a>
</body>
</html>
"""

CONFIRMATION_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <title>Booking Confirmation</title>
</head>
<body>
    <h1>Thank you, {{ name }}!</h1>
    <p>You have successfully booked {{ quantity }} ticket(s) for {{ event }}.</p>
    <a href="/">Return to Home</a>
</body>
</html>
"""


@app.route("/")
def index() -> str:
    """Render the home page."""
    return render_template_string(INDEX_HTML)


@app.route("/book", methods=["GET", "POST"])
def book() -> str:
    """Display booking form and handle submissions."""
    if request.method == "POST":
        name = request.form.get("name")
        event = request.form.get("event")
        quantity = request.form.get("quantity")
        return render_template_string(CONFIRMATION_HTML, name=name, event=event, quantity=quantity)
    return render_template_string(BOOK_FORM_HTML)


if __name__ == "__main__":
    # When run directly, start the Flask development server on port 5000.
    # In production the port should be configured through the environment (e.g. by a process manager).
    app.run(host="0.0.0.0", port=5000, debug=False)
