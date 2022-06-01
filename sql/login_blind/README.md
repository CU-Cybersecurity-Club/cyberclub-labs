# Blind SQL Injection Lab

This lab is meant for practicing blind SQL injection. This lab is the same webapp as the simple SQL injection lab, but with a few changes. The previous SQL injection vulnerabilities have been fixed, but a new one has been introduced. Now the webapp stores the previous page a user visits along with their user-agent. When the user logs in from a particular device, they expect to be directed to the last page they visited from that device (or rather from the last device with the same user-agent). This functionality is vulnerable to SQL injection, but does not directly leak information. Instead, if the SQL query used to retrieve the last page is invalid or returns a page that's not allowlisted, the user is by default redirected to the index page.


## Setup instructions
The lab should be easy to set up on any machine that has docker installed and python version 3.8 or later (if using the `run.py` script). The containers expect to be given passwords for the MySQL root and webapp users. The `run.py` script takes care of generating new random passwords each time it's run and launches the containers using those random passwords.

The recommended approach to setting up this lab is:

    1) Navigate to this directory
    2) Run `docker compose build` to build the required images
    3) Run `python run.py`

If you optionally want to run the tests to make sure the lab is working, you can follow the same steps but replace the final command with `python run.py --test`.

## Labs

### Lab 1: Login as admin
The developers of the gradebook application found out about the SQL injection vulnerabilities in their previous version and have fixed the root causes by using prepared statements. However, they forgot the time honored principle YAGNI (You Ain't Gonna Need It) and introduced a new feature which, on login, tries to restore the user to the last page they visited. Since users may tend to visit different pages on their phones and computers, the devs opted to track the last page visited per user and user-agent. You think the devs may not have learned their lesson last time. Try to recover the password for the `admin` user. Then login as the admin user to complete this lab.

For this lab you can login as `alice` using the password: `super_secret_password`.
