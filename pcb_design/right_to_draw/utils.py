from django.contrib.auth.tokens import PasswordResetTokenGenerator
class CustomTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return f"{user.pk}{timestamp}{user.password}"

token_generator = CustomTokenGenerator()