from .models import User

class EmailBackend(object):
    def authenticate(self, request, **kwargs):
        # 要注意登录表单中用户输入的用户名或者邮箱的 field 名均为 username
        email = kwargs.get('email', kwargs.get('username'))
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            pass
        else:
            if user.check_password(kwargs["password"]):
                return user

    def get_user(self, user_id):
        """
        该方法是必须的
        """
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None