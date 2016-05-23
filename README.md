[![travis-ci](https://travis-ci.org/respondcreate/median-microservice.svg?branch=master)](https://travis-ci.org/respondcreate/median-microservice/) [![coveralls](https://img.shields.io/coveralls/respondcreate/median-microservice.svg?style=flat)](https://coveralls.io/github/respondcreate/median-microservice)

# Median Microservice

A simple [Flask](http://flask.pocoo.org/)-powered microservice that calculates the median of integers.

## Endpoints

- `/put` (POST/PUT): Store an integer for one minute. Expects a JSON object in the following structure:

    ```json
    {
        "int": <integer>
    }
    ```
- `/median` (GET): Initiate a median calculation request for all stored integers received over the last minute. Returns a JSON object in the following format:

    ```json
    {
        "job_id": <job_id>,
        "url": <url_for_result>
    }
    ```
- `/median-results/<job_id>` (GET): See results of a median calculation request.

    - HTTP 200: Calculation complete. Returns a JSON object in the following format:

        ```json
        {
            "message": "Calculation complete!",
            "median": <median>
        }
        ```

    - HTTP 202: Calculation not-yet complete. Returns a JSON object in the following format:

        ```json
        {
            "message": "Still processing..."
        }
        ```

## Local Development Setup

### Dependencies:

* Redis 3.0.x
* Python 2.7.x
    * `Flask==0.10.1`
    * `numpy==1.11.0`
    * `redis==2.10.5`
    * `rq==0.5.6`

### Installation Instructions

1. Clone this repo to your local machine:

    ```bash
    $ git clone git@github.com:respondcreate/median-microservice.git
    ```

2. Create a new virtual environment and install dependencies:

    ```bash
    $ cd median-microservice
    $ virtualenv ENV
    $ source ENV/bin/activate
    $ cd web/
    $ pip install -r requirements.txt
    ```

3. Start-up the microservice:

    ```bash
    $ python app.py
    ```

4. Open a new shell, activate the virtualenv and start the redis queue consumer (worker.py):

    ```bash
    $ cd median-microservice
    $ source ENV/bin/activate
    $ cd web/
    $ python worker.py
    ```

Now visit http://127.0.0.1:5000/put/50 to put your first integer (50) into the microservice!

## Running Tests

Run tests with this command (be sure your virtualenv is activated before running):

```bash
$ python web/app_tests.py
```

## Docker Commands

The following commands assume you have both `docker-machine` and `docker-compose` installed.

### Building a docker-machine

1. Create a machine with docker-machine:

    Locally, with virtualbox:

    ```bash
    $ docker-machine create -d virtualbox median-microservice
    ```
    
    On DigitalOcean (assumes you have a valid DigitalOcean token set to the DO_TOKEN environment variable):
        
    ```bash
    $ docker-machine create -d digitalocean --digitalocean-access-token=$DO_TOKEN median-microservice
    ```

    On Amazon AWS (assumes you have `~/.aws/credentials` set appropriately):
        
    ```bash
    $ docker-machine create --driver amazonec2 --amazonec2-zone=b docker-demo
    ```

2. Make the median-microservice docker machine your 'current' one:
    
    ```bash
    $ eval "$(docker-machine env median-microservice)"
    ```

### Spinning up with `docker-compose`

1. First, build:

    ```bash
    $ docker-compose build
    ```

2. Spin up the server:

    With development settings:

    ```bash
    $ docker-compose up -d
    ```

    With production settings:

    ```bash
    $ docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
    ```
