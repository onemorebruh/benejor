# benejor

* status - DEV

## description

benejor is a simple telegrambot on python and mysql
it saves users' passwords. this bot was made to help user in password management by generating and saving passwords.

## avalibale functions
- generate password
- write password into database
- find passwords in database
- update old passwords

## instalation
1. `git clone https://github.com/onemorebruh/benejor.git`
2. create database and user
3. give privileges to this user
2. `sudo ./get_started`
3. enter all data script asks
4. run the controller.py

## usage

```python
from functions import charge, generate_password

password = generate_password(True,
                             True)  # the first True is for such symbols as */a etc and the second True is for upper words
print(password)  # something like 'sailBUILDMEAThundredsizeHARDFOODyoung!BRANCH'
```

## configuration
- python:3.8.10
- mysql:8.0.26
- ubuntu:20.04

# TODO
[x] make dictionary loads once per script launch only
[x] encrypting and decrypting functions for passwords
[] dockerize it

