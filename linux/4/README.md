# Assignment 4
This assignment requires you to crack passwords using John the Ripper using a dictionary attack (via the [rockyou wordlist](https://github.com/brannondorsey/naive-hashcat/releases/download/data/rockyou.txt))

Notice that a couple of files are provided. These represent the
- passwd file which stores user information (in `/etc/passwd`, and
- shadow file where user passwords are stored in an encrypted format (in `/etc/shadow`)
Using the commands and switches provided by [John](https://www.openwall.com/john/) to decrypt the passwords you observe in the `shadow` file.