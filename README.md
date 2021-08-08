# fesel-scheduler

# contents
* [structure](#structure)
* [prerequisites](#prerequisites)
* [installation](#installation)
* [execution](#execution)

# structure

this project is structured in a modular way, it is linked to several libraries such as **[opencv, numpy, zmq, multiprocessing, mysql]**
It contains the :
* following directories:
    * db_config
        * contains the database configuration parameters and allows to connect to the database
    * libraries
        * contains all needed functions
    * processing
        * contains the main file      
    * resources
        * contains a sample of videos to test the scheduler
    * source
        * this module allows to to save our simulated public
    * utilities
        * this module helps to create a database and simulate a public
        * it uses numpy and mysql
* following files
    * git config
        * .gitignore
    * project libraries
        * requirements.txt

# prerequisites
* git
* python3
* python3-venv
* mysql-server

# installation
```bash
    git clone https://github.com/searchmapai/fesel-scheduler
    cd fesel-scheduler
    git checkout develop
    git checkout features/your_features_name
    python -m venv env
    source env/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
```

# execution
* Create database
    * Put your mysql-server username and password in db_config/config.py
    * Activate mysql-server
    ```bash
        mysql -u root -p
    ```  
    * Create the database
    ```bash
        source utilities/db.sql
    ```
* Generate Passengers
```bash
    python -m utilities.generate_public
```
* Execute the scheduler
```bash
    pythin -m processing.process
```