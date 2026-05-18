Read database/db.py to find the db connection pattern and database filename.

Then write and run a Python script that:

1. Connects to the database using the get_db() pattern from db.py
2. Deletes all records from the expenses table first (to respect the foreign key constraint), then all records from the users table
3. Uses parameterised-safe DELETE statements (no WHERE clause needed)
4. Resets the AUTOINCREMENT counters for both tables by deleting their entries from sqlite_sequence
5. Runs everything in a single transaction — roll back if anything fails
6. Prints confirmation:
   - Number of rows deleted from expenses
   - Number of rows deleted from users
   - Confirmation that sequences were reset
