# School Bus Application

This is a complete demo of a system for automating the pickup and drop off of school students similar to Uber. The bus driver will see the locations of all the students that he/she needs to pickup on a map and will see the optimum route to pickup all students and then take them to the school. A student side application will allow him/her to cancel pickup, in which case the bus will update the travel route to the new optimum one.

[App Demo](https://sleepy-everglades-39783.herokuapp.com/)

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

You need to make sure to have the following installed before setting up this app demo:

* [Python](http://install.python-guide.org)
* [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)
* [Postgres](https://devcenter.heroku.com/articles/heroku-postgresql#local-setup)
* [Pip](https://pip.pypa.io/en/stable/installing/)

### Installing

In order to install and run this application demo on your local machine, kindly perform the following steps:

```sh
$ git clone git@github.com:heroku/python-getting-started.git
$ cd python-getting-started

$ pipenv install

$ createdb python_getting_started

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

* [Dropwizard](http://www.dropwizard.io/1.0.2/docs/) - The web framework used
* [Maven](https://maven.apache.org/) - Dependency Management
* [ROME](https://rometools.github.io/rome/) - Used to generate RSS Feeds

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Authors

* **Billie Thompson** - *Initial work* - [PurpleBooth](https://github.com/PurpleBooth)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## Documentation

For more information about using Python on Heroku, see these Dev Center articles:

- [Python on Heroku](https://devcenter.heroku.com/categories/python)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc
