# Benejor

* status - DEV
* version - 2.0.0

## Description

Benejor is a simple telegram bot on python and mysql.
It saves users' passwords. This bot was made to help user in password management by generating and saving passwords.

## Structure
```
|-`config.py` - configuration file
|-`database_interaction.py` - functions bot uses for working with database
|-`dispatcher.py` - routes messages
|-`dump.sql` - database dump
|-`handlers/` - directory with ligic of bot
|   |-`__init__.py` - init file
|   |-`handler_commands.py` - contain logic of commands such as `/start`
|   |-`handler_find_password.py` - contain logic of the finding password in database
|   |-`handler_random_password.py` - contain logic of getting random password
|   |-`handler_settings.py` - contain logic of changing settings of password generator
|   |-`handler_write.py` - contain logic of writing new password into database
|-`header.py` contain variables which have to be inited but should not be in `main.py`
|-`main.py` - main file to run bot
|-`markups.py` - file with markups used in bot
|-`message_handling_state.py` - states for FSM
|-`pass_gen_lib.py` - library i wrote for generating passwords
|-`README.md` - file you are reading right now
|-`requirements.txt` - file with python packages to install
|-`test.py` - file with tests
|-`usersettings.py` - enum with settings user have
```
## Installation
1. `git clone https://github.com/onemorebruh/benejor.git`
2. create database and user
3. give privileges to this user
4. load dump to database
5. fill config.py with required data
6. install python requirements
7. run the main.py

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

| program | version |
|---------|---------|
| python  | 3.9.2   |
| mariadb | 10.5.28 |
| debian  | 11      |

## TODO

Dockerize
- [ ] replace `get_started` script with Dockerfile and config file
- [ ] replace mysql with sqlite

Rewrite on aiogram
- [x] write markups
- [x] implements same algorithm as before
- [x] configure HTML parse mode

UX
- [x] copy password by click
- [x] make generator settings button show info and buttons to change settings
