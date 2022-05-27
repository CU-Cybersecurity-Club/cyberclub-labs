# Simple SQL Injection Lab

This lab is meant for practicing simple SQL injection. The login page is vulnerable to SQL injection which allows for auth bypass. The profile page is vulnerable to multi-statement SQL injection which allows for arbitrarily modifying any table in the database. In particular, the grades for each course can be modified.

## Setup instructions
The lab should be easy to set up on any machine that has docker installed and python version 3.8 or later (if using the `run.py` script). The containers expect to be given passwords for the MySQL root and webapp users. The `run.py` script takes care of generating new random passwords each time it's run and launches the containers using those random passwords.

The recommended approach to setting up this lab is:

    1) Navigate to this directory
    2) Run `docker-compose build` to build the required images
    3) Run `python run.py`

If you optionally want to run the tests to make sure the lab is working, you can follow the same steps but replace the final command with `python run.py --test`.
