# Clinical Code Assessment

- Need to have elastic search running and setup the configurations in the Config file
    - `PROGRESSES` is the index for saving user's progress
    - `DATA` is the index for saving and updating the file content
    - Both index need to be created at server setup time
    - `ES` is the index used to search for UMLS

- Run Python project by using the following command:
    - Development Env:
        - `python3 main.py -d` or `python3 main.py --dev`
    - Production Env:
        - `python3 main.py -p` or `python3 main.py --prod`
    - Both will run on port specified in config file

- The web interface is located at web/index.html

- The data source in the `data` folder need to be in `csv`/`CSV`/`txt` format
- The data will be updated once an hour automatically, a log file named `update_log` will be created and record each update time and successful or not
- A file named `index_id` is for recording the unique id of the data in index, it will be updated each time if a new data index is created, for the most of time, this will be the same, and update the file will only update the existing data index by using this `index_id`, not create new index.
