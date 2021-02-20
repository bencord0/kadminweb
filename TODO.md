- Modify pykerberos to expose add_principal
    - Wire it up to the /admin/django_kerberos/kerberosuser/add/ form
- Expose the kadmin change passwd (unconditional password reset)

- Allow admins to change user passwords /admin/django_kerberos/kerberosuser/<username>/password/
- Allow users to change their own passwords /accounts/password_change/
- Allow users to reset their own passwords /accounts/password_reset/

- Allow anonymous users to sign-up
