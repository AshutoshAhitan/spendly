# Spec: Registration

## Overview
This step wires up the user registration form so that new visitors can create
an account. It adds the `POST /register` route, a `create_user()` DB helper,
input validation, and flash-message feedback. Successful registration redirects
the user to the login page. This is the first step that writes to the database
at runtime and the first that requires `app.secret_key` (needed for Flask flash
messages).

## Depends on
- Step 01 — Database Setup (`users` table, `get_db()`, `init_db()`)

## Routes
- `POST /register` — validates form data, hashes password, inserts user row, redirects — public

## Database changes
No new tables or columns. The existing `users` table (id, name, email,
password_hash, created_at) is sufficient. A new helper `create_user()` will
be added to `database/db.py` to encapsulate the INSERT.

## Templates
- **Modify:** `templates/register.html`
  - Add `method="POST"` and `action="{{ url_for('register') }}"` to the `<form>`
  - Render flashed messages (success and error categories) above the form
  - Pre-fill `name` and `email` fields with submitted values on validation error
    so the user does not have to retype them

## Files to change
- `app.py` — add `POST /register` route; import `session`, `flash`, `redirect`,
  `url_for`, `request`; set `app.secret_key`
- `database/db.py` — add `create_user(name, email, password)` helper
- `templates/register.html` — form action/method + flash message block + sticky fields

## Files to create
None.

## New dependencies
No new dependencies. `werkzeug.security.generate_password_hash` is already
available via the existing Flask install.

## Rules for implementation
- No SQLAlchemy or ORMs — raw `sqlite3` only
- Parameterised queries only — never f-strings in SQL
- Passwords hashed with `werkzeug.security.generate_password_hash` before INSERT
- Use CSS variables — never hardcode hex values in any template or stylesheet
- All templates must extend `base.html`
- `create_user()` must live in `database/db.py`, not inline in the route
- Duplicate email must be caught and reported as a flash error (check for
  `sqlite3.IntegrityError` on the UNIQUE constraint)
- Validate that name, email, and password are all non-empty before hitting the DB
- Validate that password is at least 8 characters
- On any validation error, re-render `register.html` (do not redirect) so sticky
  field values are available
- On success, flash a success message and `redirect(url_for('login'))`
- `app.secret_key` must be set before any `flash()` call; use a fixed dev string
  for now (e.g. `"dev-secret-change-in-prod"`)

## Definition of done
- [ ] Submitting the form with valid data creates a new row in the `users` table
- [ ] The new user's password is stored as a hash, never plaintext
- [ ] Submitting with an already-registered email shows an error flash message and
      does not create a duplicate row
- [ ] Submitting with any empty field shows a validation error and re-renders the form
- [ ] Submitting with a password shorter than 8 characters shows a validation error
- [ ] Name and email fields retain their submitted values after a validation error
- [ ] Successful registration redirects to `/login` with a success flash message
- [ ] The registration form's `action` uses `url_for('register')`, not a hardcoded URL
- [ ] `pytest` passes with no errors
