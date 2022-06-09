# Interview questions
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