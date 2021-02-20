#!/usr/bin/env python
import os
import sys
import getpass
import logging

# pypi.org/project/pykerberos/
import kerberos

from dataclasses import dataclass


@dataclass
class Settings:
    service: str
    realm: str
    keytab_file: str


def check_password(username, password):
    try:
        # verify is an extra field implemented in https://github.com/02strich/pykerberos
        # it is needed to prevent KDC spoofing attacks, but require service authentication
        # with a keytab file specified in `KRB5_KTNAME`.
        return kerberos.checkPassword(username, password, settings.service, settings.realm, True)
    except kerberos.BasicAuthError:
        logging.exception("username/password mismatch")
        return False


def main():
    print('Username: ', end='', flush=True)
    username = sys.stdin.readline().strip()
    password = getpass.getpass()

    authenticated = check_password(username, password)
    print(f'Authenticated {username}: {authenticated}')


if __name__ == '__main__':
    settings = Settings(
        service=os.getenv('AUTH_SERVICE_NAME', 'http/devapp@EXAMPLE.COM'),
        realm=os.getenv('AUTH_SERVICE_REALM', 'EXAMPLE.COM'),
        keytab_file=os.getenv('KRB5_KTNAME', '/etc/krb5.keytab'),
    )
    main()
