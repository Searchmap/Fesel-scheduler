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
    git clone https://github.com/Metsearch/multimodal-hand-gesture-recognition
    cd multimodal-hand-gesture-recognition
    git checkout -b develop
    git pull origin develop
    git checkout features/your_features_name
    python -m venv env
    source env/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
```

# execution
```bash
    python -m utilities.generate_public
    python -m utilities.create_db
    pythin -m processing.process
```