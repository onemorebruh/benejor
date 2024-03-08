# Benejor

* status - DEV

## Description

benejor is a simple telegrambot on python and mysql
it saves users' passwords. this bot was made to help user in password management by generating and saving passwords.



## Instalation
1. `git clone https://github.com/onemorebruh/benejor.git`
2. create database and user
3. give privileges to this user
2. `sudo ./get_started`
3. enter all data script asks
4. run the controller.py

## Functions

```python
from functions import charge, generate_password, encrypt, decrypt
from config import *

password = generate_password(True,
                             True)  # the first True is for such symbols as */a etc and the second True is for upper words
print(password)  # something like 'sailBUILDMEAThundredsizeHARDFOODyoung!BRANCH'

print(encrypt("sailBUILDMEAThundredsizeHARDFOODyoung!BRANCH", 12345)) # something like 116C99A108C112E71D86C75D79C72D82D70C67A87A108B122C111D102D117B105E105A116E107D125B105E77B66F84B71C74C84A80A70C124A115C122E111B105B36E70C87B66A80F70D76E

print(decrypt("116C99A108C112E71D86C75D79C72D82D70C67A87A108B122C111D102D117B105E105A116E107D125B105E77B66F84B71C74C84A80A70C124A115C122E111B105B36E70C87B66A80F70D76E", 12345))
```

## Configuration
- python:3.8.10
- mysql:8.0.26
- ubuntu:20.04

## TODO

Deploy
- [ ] replace `get_started` script with Dockerfile and config file

Rewrite on aiogram
- [ ] write markups
- [ ] implemets same algoritm as before
- [ ] configure HTML parsing

UX
- [ ] add `copy password` button
