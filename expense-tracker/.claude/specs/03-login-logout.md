# Spec: Login and Logout

## Overview
This step implements session-based authentication so registered users can sign
in and sign out. It upgrades the stub `GET /login` route to handle `POST`
form submissions, verifies the submitted password against the stored hash,
and stores the user's `id` and `name` in the Flask session on success.
The stub `GET /logout` route is implemented to clear the session and redirect
to the landing page. Together these two routes gate access to all future
logged-in features (profile, expense management) that are defined in later steps.

## Depends on
- Step 01 — Database Setup (`users` table, `get_db()`)
- Step 02 — Registration (`create_user()`, password hashing with werkzeug)

## Routes
- `POST /login` — verifies email + password, sets session, redirects to `/profile` — public
- `GET /logout` — clears session, redirects to `/` — public (no auth required to log out)

## Database changes
No new tables or columns. A new helper `get_user_by_email(email)` will be added
to `database/db.py` to look up a user row by email for the login check.

## Templates
- **Modify:** `templates/login.html`
  - Add `method="POST"` and `action="{{ url_for('login') }}"` to the `<form>`
  - Render flashed messages (error category) above the form
  - Pre-fill the `email` field with the submitted value on failure so the user
    does not have to retype it
  - Password field must NOT be pre-filled on failure

## Files to change
- `app.py` — upgrade `GET /login` to `GET|POST /login`; implement `POST` logic;
  implement `GET /logout`; import `session` from flask; import `check_password_hash`
  from werkzeug.security; import new `get_user_by_email` helper
- `database/db.py` — add `get_user_by_email(email)` helper that returns a single
  user row or `None`
- `templates/login.html` — form action/method + flash message block + sticky email field

## Files to create
None.

## New dependencies
No new dependencies. `werkzeug.security.check_password_hash` is already available
via the existing Flask install.

## Rules for implementation
- No SQLAlchemy or ORMs — raw `sqlite3` only
- Parameterised queries only — never f-strings in SQL
- Password verification must use `werkzeug.security.check_password_hash`
- Use CSS variables — never hardcode hex values in any template or stylesheet
- All templates extend `base.html`
- `get_user_by_email()` must live in `database/db.py`, not inline in the route
- On missing email or password field → flash error, re-render `login.html`
- On email not found OR password mismatch → show the same generic error message
  ("Invalid email or password.") — never reveal which field was wrong
- On success → store `session["user_id"]` and `session["user_name"]`, then
  `redirect(url_for("profile"))`
- `GET /logout` → `session.clear()`, then `redirect(url_for("landing"))`
- Do not implement auth guards on `/profile` in this step — that is Step 4

## Definition of done
- [ ] Submitting valid credentials sets `session["user_id"]` and redirects to `/profile`
- [ ] Submitting an unrecognised email shows "Invalid email or password." and re-renders the form
- [ ] Submitting a wrong password shows "Invalid email or password." and re-renders the form
- [ ] Submitting with an empty email or empty password shows a validation error
- [ ] The email field retains its submitted value after a failed login
- [ ] The password field is always blank after a failed login
- [ ] Visiting `/logout` clears the session and redirects to `/`
- [ ] After logout, `session["user_id"]` is no longer present
- [ ] The login form's `action` uses `url_for('login')`, not a hardcoded URL
- [ ] `pytest` passes with no errors
