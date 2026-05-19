import sqlite3
from datetime import datetime
from flask import Flask, render_template, request, flash, redirect, url_for, session, abort
from werkzeug.security import check_password_hash
from database.db import get_db, init_db, seed_db, create_user, get_user_by_email, get_user_by_id

app = Flask(__name__)
app.secret_key = "dev-secret-change-in-prod"

with app.app_context():
    init_db()
    seed_db()


# ------------------------------------------------------------------ #
# Routes                                                              #
# ------------------------------------------------------------------ #

@app.route("/")
def landing():
    return render_template("landing.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name     = request.form.get("name", "").strip()
        email    = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        if not name or not email or not password:
            flash("All fields are required.", "error")
            return render_template("register.html")

        if len(password) < 8:
            flash("Password must be at least 8 characters.", "error")
            return render_template("register.html")

        try:
            create_user(name, email, password)
        except sqlite3.IntegrityError:
            flash("An account with that email already exists.", "error")
            return render_template("register.html")

        flash("Account created! Please sign in.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email    = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        if not email or not password:
            flash("Invalid email or password.", "error")
            return render_template("login.html")

        user = get_user_by_email(email)

        if user is None or not check_password_hash(user["password_hash"], password):
            flash("Invalid email or password.", "error")
            return render_template("login.html")

        session["user_id"]   = user["id"]
        session["user_name"] = user["name"]
        return redirect(url_for("profile"))

    return render_template("login.html")


# ------------------------------------------------------------------ #
# Placeholder routes — students will implement these                  #
# ------------------------------------------------------------------ #

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("landing"))


@app.route("/profile")
def profile():
    if not session.get("user_id"):
        return redirect(url_for("login"))

    user = get_user_by_id(session["user_id"])
    if user is None:
        abort(404)

    member_since = datetime.strptime(user["created_at"], "%Y-%m-%d %H:%M:%S").strftime("%B %Y")

    stats = {
        "total_spent": "$847.50",
        "transaction_count": 12,
        "top_category": "Food",
    }

    transactions = [
        {"date": "May 15, 2026", "description": "Grocery shopping",        "category": "Food",          "amount": "$65.00"},
        {"date": "May 12, 2026", "description": "Monthly electricity bill", "category": "Bills",         "amount": "$120.00"},
        {"date": "May 10, 2026", "description": "Metro card top-up",        "category": "Transport",     "amount": "$30.00"},
        {"date": "May 08, 2026", "description": "Dinner with friends",      "category": "Food",          "amount": "$48.00"},
        {"date": "May 05, 2026", "description": "Movie tickets",            "category": "Entertainment", "amount": "$25.00"},
    ]

    categories = [
        {"name": "Food",          "total": "$223.50", "pct": 80},
        {"name": "Bills",         "total": "$180.00", "pct": 64},
        {"name": "Shopping",      "total": "$95.00",  "pct": 34},
        {"name": "Transport",     "total": "$95.00",  "pct": 34},
        {"name": "Health",        "total": "$89.00",  "pct": 32},
        {"name": "Entertainment", "total": "$75.00",  "pct": 27},
    ]

    return render_template("profile.html",
        user=user,
        member_since=member_since,
        stats=stats,
        transactions=transactions,
        categories=categories,
    )


@app.route("/expenses/add")
def add_expense():
    return "Add expense — coming in Step 7"


@app.route("/expenses/<int:id>/edit")
def edit_expense(id):
    return "Edit expense — coming in Step 8"


@app.route("/expenses/<int:id>/delete")
def delete_expense(id):
    return "Delete expense — coming in Step 9"


if __name__ == "__main__":
    app.run(debug=True, port=5001)
