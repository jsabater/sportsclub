# Athletics sports club

This project is a web application that mimics, at very small scale, an athletics club for kids, to be used by vocational trainingstudents to learn:

1. How to securely deploy web applications into production environments using a CI/CD pipeline.
2. How to create front-end web applications that use a REST API as back-end.

> [!CAUTION]
> This project contains multiple security flaws, intended for students to be found, exploited and corrected. Therefore, do not use it in a production environment.


## Tech stack

This project is a headless application built using the following technolgies:

* [Django Ninja](https://django-ninja.dev/) to create the REST API (using Pydantic for validations).
* [Django's ORM](https://docs.djangoproject.com/en/stable/topics/db/models/) for the model.
* [Django's admin panel](https://docs.djangoproject.com/en/stable/ref/contrib/admin/) to create a back-office where to manage application settings and browse and modify data.
* [PostgreSQL](https://postgresql.org/) for the database server.
* [NGINX](https://nginx.org/) as reverse proxy and load balancer.
* [Docker Compose](https://docs.docker.com/compose/) to define and manage the containerised services.

To keep things simple, access to the database and tests will not use asynchronous methods. Moreover, the application neither includes authentication nor authorisation.

> Each student can fork the project on Github so that he or she can start making modifications.


## Security

A CI/CD pipeline is a security-enabling framework, serving as the backbone for *DevSecOps*. Some of its benefits are:

* Automated security integration.
* Reduced human error.
* Faster patching.

> Most of [the twelve factors](https://www.12factor.net/) are used in this example repository, therefore can be used to teach good security practices.

Via the application in this repository, not only can students learn how to securely build a CI/CD pipeline, but also security concepts related to web applications, such as:

* Data-protection using an `Auditory` base class that includes auditory attributes and methods. It supports soft-deletion and restoration, and datetimes for creation, modification and deletion of records. It is an incomplete implementation so that students can expand it after doing some research.
* Use of `environment variables` to store configuration, via the `.env` file and the `environ` package.
* Execution of application as stateless process.
* Strict separation of build and run stages.
* Explicit declaration and isolation of dependencies, based on the provided, miserable `requirements.txt`.
* Keeping development and production as similar as possible.
* Maximize robustness with fast startup and graceful shutdown.
* CORS headers.
* Public ID separate from internal ID (primary key).
* Validation of input data via schemas.
* Blue/Green deployments.
* Makefile to automate tasks.

> Authentication is enabled in the admin panel using cookie-based sessions, but the endpoints do not support any form of authentication.

Regarding security integration in the CI pipeline, this application only includes linting via [Ruff](https://docs.astral.sh/ruff/). Students are meant to add additional jobs that run more security tools, such as [pip-audit](https://pypi.org/project/pip-audit/), [CodeQL](https://codeql.github.com/), [Prek](https://github.com/j178/prek) + [Gitleaks](https://github.com/gitleaks/gitleaks), or [Vulture](https://pypi.org/project/vulture/), [Trufflehog](https://github.com/trufflesecurity/trufflehog), [Hadolint](https://github.com/hadolint/hadolint) among others.


## The model

This is the list of models or entities it has, with a  brief description of each one:

* `Auditory`: a base class that includes auditory attributes and methods.
* `Person`: a base class that includes basic attributes of a person, used by athletes and coaches.
* `Address`: a weak entity that stores postal addresses, used by athletes, coaches and venues.
* `Venue`: locations where sports are practised. Uses an `ENUM` to type them (see below).
* `Athlete`: people practising sports.
* `Coach`: people training athletes.
* `Activity`: a scheduled activity. Uses polymorphism to have `Competition` and `Training`.

The following disciplines are supported (from all the practised ones):

* Sprints. Short-distance races, typically from 60 to 100 metres, focused on maximum speed.
* Long-distance running. Races over 500 metres or more, testing endurance and stamina.
* Relays. Team races where runners pass a baton, combining speed and coordination.
* High jump. Athletes leap over a horizontal bar without knocking it down.
* Long jump. Athletes sprint and jump into a sandpit, aiming for maximum distance.


## Apps

The project has four apps, and models are spread among them:

| App          | Models                                |
|--------------|---------------------------------------|
| `core`       | `Address`, `Auditory`                 |
| `inventory`  | `VenueType`, `Venue`                  |
| `people`     | `Person`, `Athlete`, `Coach`          |
| `scheduling` | `Activity`, `Competition`, `Training` |

> The `core` application also includes `/ping` and `/health` endpoints.


## Structure of each app

We will slightly modify the default structure of each app so that:

| Module  | Default location | New location | Notes                                |
|---------|------------------|--------------|--------------------------------------|
| Admin   | `admin.py`       | `admin/`     | One file per entity                  |
| Models  | `models.py`      | `models/`    | One file per entity                  |
| API     |                  | `api/`       | One file per entity                  |
| Schemas |                  | `schemas/`   | One file per entity                  |
| Tests   | `tests.py`       | `tests/`     | One file per type of test and entity |

Taking `core` as an example, we will see a structure similar to this:

```
sportsclub/
└── core
    ├── admin.py
    ├── apps.py
    ├── __init__.py
    ├── migrations
    │   └── __init__.py
    ├── models.py
    │   ├── __init__.py
    │   ├── address.py
    │   ├── audit.py
    │   └── managers.py
    ├── tests
    │   ├── __init__.py
    │   ├── test_api_addresses.py
    │   ├── test_models_address.py
    │   ├── test_models_audit.py
    │   ├── test_models.py
    │   └── test_schemas.py
    └── views.py
```

> Acceptance tests are meant to be added by students.


## Person base class

In the `people` app we define the abstract, or base, class `Person`, which is then used by the `Athlete` and `Coach` entities. This class has four attributes:

* `first_name`, to store the first name of the person.
* `last_name`, to store the last name of the person.
* `email`, to store the e-mail address of the person.
* `phone`, to store the phone number of the person, using international format, e.g., `+34.<number>`.

And it inherits from the `Auditory` class, so the auditory fields are already be present in the `Athlete` and `Coach` models.

## VenueType class

Venue is a broad term that encompasses any location where an activity takes place. Venues can be of type:

* `Stadium`: Used for competitions, often featuring an outdoor track and field events with spectator seating.
* `Gymnasium`, or Gym: Used for indoor training sessions.
* `Track`: Used for both training and competition in running events and relays.
* `Field`: The open area within a stadium or track facility where field events (e.g., long jump) are held.

We define the `VenueType` class in the `inventory/models/venue.py` file, to be used in the `Venue` model, using the `models.TextChoices` base class, which inherits from `enum.ENUM`.

Django Admin automatically generates a dropdown menu for `venue_type`, so we can filter and query easily.

## Polymorphism

Taking the `Activity` entity as example, we can see that it is typed:

* `Training`. A practice session aimed at skill development. Has coaches, participants, and a focus area.
* `Competition`. A competitive event with athletes and coaches, usually with a score result.

We will model this using *abstract base class inheritance* for each activity type.


### Abstract vs Multi-table Inheritance

Django supports two forms of model inheritance:

| Aspect              | Abstract Base Class (`abstract = True`)          | Multi-table Inheritance                          |
| ------------------- | ------------------------------------------------ | ------------------------------------------------ |
| Parent table        | No table created                                 | Parent table is created                          |
| Child tables        | Each child has all fields                        | Child tables link to parent via foreign key      |
| Querying parent     | Not possible                                     | Returns all subclass instances                   |
| Performance         | Faster (no JOINs)                                | Slower (requires JOINs)                          |
| Polymorphic queries | Must query each subclass separately              | Can query parent to get all types                |
| Use case            | Code reuse without shared table                  | True polymorphism with unified querying          |

We chose abstract base class inheritance for `Activity` because:

1. `Competition` and `Training` are queried and managed separately in the API.
2. No need for a unified "all activities" query in our use case.
3. Better performance without JOIN overhead.
4. Simpler database schema and fixtures.

If you needed to query all activities together (e.g., a calendar showing both trainings and competitions), multi-table inheritance would be more appropriate, allowing `Activity.objects.all()` to return mixed results.

## Installation

Clone the repository into your projects directory:

```bash
cd ~/Projects/ 
git clone https://github.com/sportsclub/sportsclub.git
```

Taking the `.env.example` file as reference, create a `.env` file in the project root and adapt it to your needs. This is the standard convention and will serve as a single source of truth throughout our project (Django, Docker Compose, CI/CD, shell scripts, etc.):

```bash
cd ~/Projects/sportsclub
cp .env.example .env
```

Next, [install Docker](https://docs.docker.com/engine/install/), if you have not already, and use Compose to bring up the environment:

```bash
docker compose up --build --detach
```

Now initialise the database:

```bash
make init-db
```

And load the test data (fixtures):

```bash
make load-fixtures
```

Finally, create a superuser:

```bash
make create-superuser
```

## Development environment

If you want students to play around with the code, they should set up a more complete environment, including a virtual environment. Start by installing the system dependencies:

```bash
sudo apt-get install --yes curl jq python3-venv
```

Then clone the repository into your projects directory:

```bash
cd ~/Projects/ 
git clone https://github.com/sportsclub/sportsclub.git
```

Then create and activate the virtual environment:

```bash
# Create and activate a virtual environment
python3 -m venv ~/Projects/sportsclub/.venv
source ~/Projects/sportsclub/.venv/bin/activate
```

Upgrade Pip:

```bash
pip install --upgrade pip
```

Now install the dependencies:

```bash
pip install --requirement ~/Projects/sportsclub/requirements.txt
```

> This project does not use `uv` on purpose, so students can research about `.lock` and `.in` files, then implement a solution.

Taking the `.env.example` file as reference, create a `.env` file in the project root and adapt it to your needs. This is the standard convention and will serve as a single source of truth throughout our project (Django, Docker Compose, CI/CD, shell scripts, etc.):

```bash
cd ~/Projects/sportsclub
cp .env.example .env
```

Now initialise the database:

```bash
make init-db
```

And load the test data (fixtures):

```bash
make load-fixtures
```

Finally, create a superuser:

```bash
make create-superuser
```

Whenever we need to reset the database, we can do so using the following command:

```bash
cd ~/Projects/sportsclub
make reset-all
```

We can now start Django's built-in development server:

```bash
cd ~/Projects/sportsclub/sportsclub
python manage.py runserver
```

And load the home page at http://127.0.0.1:8000/.


## Test data

Django has a native mechanism to load test data, a.k.a., fixtures, into the database. Files in JSON or YAML formats with test data can be created inside the `fixtures/` subdirectory of each Django app, and loaded via `python manage.py loaddata`. Advantages of using this system versus loading the data via SQL into the database are:

1. It is database-agnostic.
2. It respects Django model validation.
3. It is version-controlled.

### Tests

To run the tests for a specific Django app, use this command::

```bash
cd ~/Projects/sportsclub/sportsclub
python manage.py test core
```

We could also run the test verbosely, and for a specific test class only:

```bash
cd ~/Projects/sportsclub/sportsclub
python manage.py test core.tests.test_api_addresses.AddressAPITestCase -v 2
```

But we usually want to run all the tests at once. We can do that with a single command:

```bash
cd ~/Projects/sportsclub/sportsclub
python manage.py test
```

## Github Actions

GitHub Actions is a continuous integration and continuous delivery (CI/CD) platform that allows us to automate our build, test, and deployment workflows directly within GitHub. It enables creating automated processes that trigger when specific events occur in a repository, such as when someone opens a pull request, creates an issue, or pushes a commit.

Key components are:

* **Workflows**: Automated processes defined in YAML files stored in the `.github/workflows` directory of the repository that run one or more job.
* **Events**: Activities that trigger workflows, like pull requests, issues, commits, or scheduled times.
* **Jobs**: Sets of steps that execute on the same runner, which can run in parallel or sequentially.
* **Actions**: Reusable code packages that perform specific tasks like pulling the repository, setting up build environments, or deploying to cloud providers.
* **Runners**: Servers that execute workflows.

This project includes a `.github/workflows/ci.yml` file that has four jobs:

| Job         | Purpose                                 | Runs when              |
|-------------|-----------------------------------------|------------------------|
| lint        | Check code style with Ruff              | Always                 |
| test        | Run Django tests against PostgreSQL     | Always                 |
| build       | Verify Docker image builds successfully | After lint & test pass |
| integration | Start full stack and test API endpoints | After lint & test pass |

Key features of this workflow:

* PostgreSQL service container: GitHub Actions spins up a real PostgreSQL instance for tests
* Dependency caching: Speeds up subsequent runs by caching pip packages
* Docker layer caching: Uses GitHub Actions cache for faster Docker builds
* Parallel execution: `build` and `integration` run in parallel after `lint` and `test`
* Failure handling: Logs are shown if integration tests fail
* Environment variables now match `.env.example` (except DEBUG=False for CI safety)

This basic CI pipeline is meant to be extended and improved by students as they learn more about the world of DevSecOps. Moreover, a `cd.yml` file is also meant to be added, when the time comes.

## Ruff formatting

Our first push to the Github repository will trigger the `ci.yml` workflow. We will be able to follow its execution via the `Actions` tab in our repository at Github. To make sure we do not get linting errors not caused by us, e.g., use of single quotes in strings instead of double quotes in files created by the `manage.py startapp` command, run these commands before pushing:

```bash
cd ~/Projects/sportsclub
pip install ruff
ruff check --fix .
ruff format .
```

Review the changes made by `ruff check --fix` and `ruff format`, delete unnecessary files, such as the `views.py` file in each app, stage the changed files and commit them. Then push the commits.
