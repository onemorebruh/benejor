# TODO
[] encrypting with id as a key
[x] password generating algoritm
- [x] add more special symbols
- [x] make random letters upper
[x] setup mysql
- [x] move dictionary to database
[x] connect to mysql via python
[x] make cli interface so program will works like if it is in telegram
- [x] make abbility to find password in db
- [x] make abbility to write passwords into db(new and old
- [x] make abbility to update old passwords
- [] make abbility to add words into dictionary and use this words for password generating
- [x] turn all users actions to functions so they can be tested
[] connect it all to the telegram bot
[] make docker container
[in progress] unit tests
- [x] `pasword_generator` test
- [] `telegram_bot` test
- [x] `find` test
- [x] `write` test
- [x] `update_password` test
- [x] rewrite find, write, update functions so they will be better at tests
- [] fix pronlem -> none pf tests lunches.(script is like empty)
> possible reasons for such error
> 1. global variables
> 2. too many tests in one file
