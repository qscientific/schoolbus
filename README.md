# School Bus Application

This is a complete demo of a system for automating the pickup and drop off of school students similar to Uber. The bus driver will see the locations of all the students that he/she needs to pickup on a map and will see the optimum route to pickup all students and then take them to the school. A student side application will allow him/her to cancel pickup, in which case the bus will update the travel route to the new optimum one.

[App Demo](https://sleepy-everglades-39783.herokuapp.com/) - Used best with Chrome on a smartphone and allow location access.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

You need to make sure to have the following installed before setting up this app demo:

* [Python 2.7](http://install.python-guide.org)
* [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)
* [Postgres](https://devcenter.heroku.com/articles/heroku-postgresql#local-setup)
* [Pip](https://pip.pypa.io/en/stable/installing/)

### Installing

In order to install and run this application demo on your local machine, kindly perform the following steps:

```sh
$ git clone git@github.com:qatarsc/schoolbus.git
$ cd schoolbus

$ pipenv install

$ pip install -r requirements.txt

$ createdb schoolbus

$ python manage.py migrate
$ python manage.py collectstatic

$ heroku local
```

Your app should now be running on [localhost:5000](http://localhost:5000/).

## Deployment

These are the steps to deply this application on heroku:

```sh
$ heroku create
$ git push heroku master

$ heroku run python manage.py migrate
$ heroku open
```

## Built With

* [Python 2.7](https://www.python.org/download/releases/2.7/) - The backend programming language
* [Django](https://www.djangoproject.com/) - The backend framework used
* [Heroku](https://www.heroku.com/) - The cloud application platform used for deployment
* [Bootstrap](https://getbootstrap.com/) - The frontend framework used
* [Sublime Text](https://www.sublimetext.com/) - The code editor used

## Authors

* **Maher Khan** - *Initial work* - [github profile: maher460](https://github.com/maher460)

## Documentation

For more information about using Python on Heroku, see these Dev Center articles:

- [Python on Heroku](https://devcenter.heroku.com/categories/python)

## License

This project is licensed under the MIT License

## Acknowledgments

* Hats off to the team who presented this application in Kuwait and won medals!
