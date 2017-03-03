# tornado_random_number

Simple tornado app that attempts to fetch a JSON with a random number and renders that number.

## Setup

Create a virtual environment. For instance:

> python3 -m venv random_number_venv

Activate it:

> . random_number_venv/bin/activate

Install the requirements:

> pip install -r requirements.txt

## Run the app

> python random_number.py

## Run the tests

> python -m tornado.testing test_random_number.py
