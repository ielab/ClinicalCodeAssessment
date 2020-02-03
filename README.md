# Clinical Code Assessment

- Need to have elastic search running and setup the configurations in the Config file
    - `PROGRESSES` is the index for saving user's progress
    - `ES` is the index used to search for UMLS

- Run Python project by using the following command:
    - Development Env:
        - `python3 main.py -d` or `python3 main.py --dev`
    - Production Env:
        - `python3 main.py -p` or `python3 main.py --prod`
    - Both will run on port specified in config file

- The web interface is located at web/index.html
