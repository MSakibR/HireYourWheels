from django.contrib.auth import get_user_model

User = get_user_model()

class EmailBackend:
    def authenticate(self, request, email=None, **kwargs):
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
