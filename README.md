# Work at olist

This is an API that receives call records and calculates monthly bills for a given telephone number and period.

Challenge source: https://github.com/olist/start-at-olist-backend

## Project Requirements

- Python >= 3.5

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install poetry.

```
pip install poetry
```

With poetry run the following command to install the dependences.

```
poetry install
```
From the project root, go to api and run the migrations.

```
cd api
poetry run python manage.py migrate
```

## Usage

From the project root, go to api and start the server.

```
cd api
poetry run python manage.py runserver
```

Insert data on CallRecord.

Sample data:
* call_id: 70, started at 2016-02-29T12:00:00Z and ended at 2016-02-29T14:00:00Z.
* call_id: 71, started at 2017-12-11T15:07:13Z and ended at 2017-12-11T15:14:56Z.
* call_id: 72, started at 2017-12-12T22:47:56Z and ended at 2017-12-12T22:50:56Z.
* call_id: 73, started at 2017-12-12T21:57:13Z and ended at 2017-12-12T22:10:56Z.
* call_id: 74, started at 2017-12-12T04:57:13Z and ended at 2017-12-12T06:10:56Z.
* call_id: 75, started at 2017-12-13T21:57:13Z and ended at 2017-12-14T22:10:56Z.
* call_id: 76, started at 2017-12-12T15:07:58Z and ended at 2017-12-12T15:12:56Z.
* call_id: 77, started at 2018-02-28T21:57:13Z and ended at 2018-03-01T22:10:56Z.


Make a post request to your server (http://localhost:8000/bill/) with the following content template to get the bill detail.
```
{
    "source": "99988526423",
    "period": "12/2017"
}
```
