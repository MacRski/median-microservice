[![travis-ci](https://travis-ci.org/respondcreate/median-microservice.svg?branch=master)](https://travis-ci.org/respondcreate/median-microservice/) [![coveralls](https://img.shields.io/coveralls/respondcreate/median-microservice.svg?style=flat)](https://coveralls.io/github/respondcreate/median-microservice)

# Median Microservice

A simple [Flask](http://flask.pocoo.org/)-powered microservice that calculates the median of integers.

## Example Server

* URL: http://104.131.52.223
* CPU: Single
* RAM: 512MB

## Endpoints

- `/put/<int>` (GET): Store an integer for one minute.
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
    $ python worker.py
    ```

Now visit http://127.0.0.1:5000/put/50 to put your first integer (50) into the microservice!

## Running Tests

Run tests with this command (be sure your virtualenv is activated before running):

```bash
$ python app_tests.py
```
