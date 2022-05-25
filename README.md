Routes:
```
$ python -m flask routes
Endpoint        Methods    Rule
--------------  ---------  -----------------------
all_handler     GET        /all
sign_handler    GET, POST  /sign
static          GET        /static/<path:filename>
verify_handler  GET, POST  /verify
```
