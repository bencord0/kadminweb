# kadminweb

A kerberos administration web app

## Setup

Ask an admin to create you a principal and keytab.


    # kadmin addprinc -randkey +requires_preauth http/devapp
    # kadmin ktadd    -k /tmp/devapp.keytab      http/devapp


    $ export KRB5_KTNAME=/tmp/devapp.keytab
    $ export AUTH_SERVICE_NAME=http/devapp@EXAMPLE.COM
    $ export AUTH_SERVICE_REALM=EXAMPLE.COM

Test that the keytab works by verifying passwords against the KDC.

    $ python ./scripts/check_password.py
    Username: alice
    Password:
    Authenticated alice: True

## Create a super user

    $ ./manage.py migrate
    $ ./manage.py createsuperuser
    Username: bob
    Email address: bob@example.com
    Superuser created successfully

This user will have access to the admin pages, and can add other users.

## Running the webserver

    $ ALLOWED_HOSTS=localhost
    $ SECRET_KEY=$(uuidgen)
    $ gunicorn core.wsgi:application

