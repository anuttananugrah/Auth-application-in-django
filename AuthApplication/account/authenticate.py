from django.contrib.auth.backends import BaseBackend
from account.models import User
# from django.contrib.auth.models import User

class EmailBackend(BaseBackend):
    def authenticate(self, request, username = None, password =None, **kwargs):
        try:
            email=username
            user_instance=User.objects.get(email=email)
            if user_instance.check_password(password):
                return user_instance
        except:
            return None

    def get_user(self, user_id):
        try:
            user_instance=User.objects.get(pk=user_id)
            return user_instance
        except:
             return None
                