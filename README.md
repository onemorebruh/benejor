# Benejor

* status - DEV
* version - 2.0.0

## Description

Benejor is a simple telegram bot on python and mysql.
It saves users' passwords. This bot was made to help user in password management by generating and saving passwords.

## Structure
```
|-`main.py` - main file to run bot
|-`.env` - config file of bot
|-`dependenices` - directory with dependencies of bot
|   |-`requirements.txt` - file with python packages to install
|   |-`directory.txt` - file with words password generator uses (can be modified without aftermath)
|-`pass_gen_lib.py` - library i wrote for generating passwords
|-`markups.py` - file with markups used in bot
|-`README.md` - file you are reading right now
|-`test.py` - file with tests
|-`env.example` - example of `.env` file
```
## Installation
1. `git clone https://github.com/onemorebruh/benejor.git`
2. create database and user
3. give privileges to this user
4. `sudo ./get_started`
5. enter all data script asks
6. run the controller.py

## Usage

### pass_gen_lib

```python
from pass_gen_lib import generate_password, encrypt, decrypt

password = generate_password(True,
                             True)  # the first True is for such symbols as */ and etc, the second True is for upper words
print(password)  # something like 'sailBUILDMEAThundredsizeHARDFOODyoung!BRANCH'

print(encrypt("sailBUILDMEAThundredsizeHARDFOODyoung!BRANCH", 12345)) # something like 116C99A108C112E71D86C75D79C72D82D70C67A87A108B122C111D102D117B105E105A116E107D125B105E77B66F84B71C74C84A80A70C124A115C122E111B105B36E70C87B66A80F70D76E

print(decrypt("116C99A108C112E71D86C75D79C72D82D70C67A87A108B122C111D102D117B105E105A116E107D125B105E77B66F84B71C74C84A80A70C124A115C122E111B105B36E70C87B66A80F70D76E", 12345))
```

## Configuration
- python:3.8.10
- mysql:8.0.26
- ubuntu:20.04

## TODO

Dockerize
- [ ] replace `get_started` script with Dockerfile and config file
- [ ] replace mysql with sqlite

Rewrite on aiogram
- [x] write markups
- [ ] implements same algorithm as before
- [x] configure HTML parse mode

UX
- [x] copy password by click
- [x] make generator settings button show info and buttons to change settings
