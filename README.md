# Interview questions
## Part 1 | Technical Questions
 1) `int`, `str`, `float`, `bool`, `bytes`, `bytearray`, `list`, `dict`, `set`, `frozenset`, `tuple`.
 2) Arrays, `tuple` - immutable, `list` - mutable.
 3) References instance of current object (inside a method).
 4) Function called on initialization of an object.
 5) `pass` - empty block, `break` - interrupts execution of a loop, `continue` - skips single iteration of a loop.
 6) A way to access a part of a list (e.g., only elements 2 - 10).
 7) Function that modifies behavior of another function or class, for example, by wrapping it.
 8) In-line creation of list/tuple/dict/set from an interator.
 9) Single-line anonymous function.
 10) By using `class` keyword:
```
class MyClass:
    pass
```

 11) 
```
def my_function(*args):
    pass
```

 12)
```
def is_unique(list_to_check: List[int]) -> bool:
    return len(set(list_to_check)) == len(list_to_check)
``` 

## Part 2 | Technical Test
 1) b) False.
 2) No option is correct, `str(func)` will be printed. If you meant `print(lst)`, the answer is c) [0].
 3) c) (8, 9).
 4) `++` is not incrementation operator in Python, the result is a).
 5) Tricky :) It's c) [4, 3, 2, 1]. 

## Part 3
### Part 3.1  | Password generator
To launch, run 
`python3.7 run_pwgen.py <wordlist>`
e.g., `python3.7 run_pwgen.py Pack my box with five dozen liquor jugs`.

Wordlist requirements:
 - minimally 8 characterse
 - wordlist must contain whole English alphabet (a-z), case-insensitive


### Part 3.2  | Runner
To launch, run 
`python3.7 run_runner.py --exec <command to run> --file <csv file path>`
e.g., `python3.7 run_runner.py --exec 'sleep 10' --file output.csv`.

Parameter `--file` is optional, call with `-h` to get more info.

### Part 3.3  | Contacts
Run `python3.7 run_contacts.py --help` to get list of operations (such as create or list).

Run `python3.7 run_contacts.py <operation> --help` to parameters of individual operations.

#### Example commands
```
python3.7 run_contacts.py create --name "User One" --address "Address One" --phone "+420123123123" --email "email1@address.com"
python3.7 run_contacts.py create --name "User Two" --address "Address Two" --phone "+420123123123" --email "email2@address.com"
python3.7 run_contacts.py create --name "User Three" --address "Address Three" --phone "+420123123123" --email "email3@address.com"

python3.7 run_contacts.py list

python3.7 run_contacts.py get 1
python3.7 run_contacts.py delete 1
python3.7 run_contacts.py get 1

python3.7 run_contacts.py get 2
python3.7 run_contacts.py modify 2 --name "Other Name" --phone "123321123"
python3.7 run_contacts.py get 2

python3.7 run_contacts.py get 999

python3.7 run_contacts.py modify 999
```