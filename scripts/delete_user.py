#!/usr/bin/env python
import os
import sys
import subprocess

from dataclasses import dataclass


@dataclass
class Settings:
    kadmin_bin: str
    service: str
    realm: str
    keytab_file: str


def delete_user(username):
    subprocess.run(
        [
            settings.kadmin_bin,
            '-r', settings.realm,
            '-p', settings.service,
            '-kt', settings.keytab_file,
            'delete_principal', username,
        ],
        timeout=1,
        check=True,
    )


def main():
    print('Username: ', end='', flush=True)
    username = sys.stdin.readline().strip()

    delete_user(username)
    print(f'Deleted user: {username}')


if __name__ == '__main__':
    settings = Settings(
        kadmin_bin='kadmin',
        service=os.getenv('AUTH_SERVICE_NAME', 'http/devapp@EXAMPLE.COM'),
        realm=os.getenv('AUTH_SERVICE_REALM', 'EXAMPLE.COM'),
        keytab_file=os.getenv('KRB5_KTNAME', '/etc/krb5.keytab'),
    )
    main()
