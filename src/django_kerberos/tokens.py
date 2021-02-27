from django.contrib.auth.tokens import PasswordResetTokenGenerator


class PasswordlessResetTokenGenerator(PasswordResetTokenGenerator):
    """
    PasswordResetTokenGenerator that doesn't take the password into account
    """

    def _make_hash_value(self, user, timestamp):
        login_timestamp = '' if user.last_login is None else user.last_login.replace(microsecond=0, tzinfo=None)
        return str(user.pk) + str(login_timestamp) + str(timestamp)


token_generator = PasswordlessResetTokenGenerator()
