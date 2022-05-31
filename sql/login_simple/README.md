# Simple SQL Injection Lab

This lab is meant for practicing simple SQL injection. The login page is vulnerable to SQL injection which allows for auth bypass. The profile page is vulnerable to multi-statement SQL injection which allows for arbitrarily modifying any table in the database. In particular, the grades for each course can be modified.

## Setup instructions
The lab should be easy to set up on any machine that has docker installed and python version 3.8 or later (if using the `run.py` script). The containers expect to be given passwords for the MySQL root and webapp users. The `run.py` script takes care of generating new random passwords each time it's run and launches the containers using those random passwords.

The recommended approach to setting up this lab is:

    1) Navigate to this directory
    2) Run `docker compose build` to build the required images
    3) Run `python run.py`

If you optionally want to run the tests to make sure the lab is working, you can follow the same steps but replace the final command with `python run.py --test`.

## Labs

### Lab 1: Login to the application
Suppose you want to login to the gradebook to see Alice's grades. You know she uses the username `alice`, but you don't know her password. You think the login page may be vulnerable to a SQL Injection attack. Login to the application as Alice to complete this lab.

### Lab 2: Change Alice's grades
Now that you're logged in as Alice, you should be able to see Alice's grades. It just so happens that you want to make sure Alice gets a 4.0 GPA this semester. To complete this lab, change Alice's grades to all A's so she has a 4.0 GPA for the semester.
