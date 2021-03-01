# Lumkani test project

## Run program
Program works only with UNIX operation systems
install virtualenv and run the command (python 3.7.5 required)
```
$ virtualenv -p python3 venv
```
then activate vitrualenv
```
$ source venv/bin/activate
```
you should enter input data file in `inputs` directory
after that you can run the program
```
$ python main.py <input.csv> <directory_name>
```
the results should appear in `results/<directory_name>`

## Run tests:
to run tests you should enter next command:
```
$ python -m unittest tests/test_handlers.py
```

 
