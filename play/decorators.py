from functools import wraps
from django.http import JsonResponse
from django.conf import settings
from .models import User


def require_login(func=None, redirect=None):
    """
    第二种写法：带参数的装饰器
    第二种方法可以解决 got an unexpected keyword argument 错误。
    """

    def decorator(func):
        @wraps(func)
        def returned_wrapper(request, *args, **kwargs):

            try:
                openid = request.headers['X-TT-OPENID']
            except AttributeError:
                return JsonResponse(dict(code=101, msg='No authenticate header'))
            except Exception as e:
                return JsonResponse(dict(code=102, msg='Can not get openid'))

            try:
                user, created = User.objects.get_or_create(username=openid)
            except User.DoesNotExist:
                return JsonResponse(dict(code=103, msg='User does not exist'))

            if not user.is_active:
                return JsonResponse(dict(code=104, msg='User inactive or deleted'))

            request.user = user
            return func(request, *args, **kwargs)
            # if request.user.is_authenticated:
            #     return func(request, *args, **kwargs)
            # else:
            #     return JsonResponse(dict(code=1, msg='User not login'))

        return returned_wrapper

    if not func:
        def foo(func):
            return decorator(func)

        return foo

    else:
        return decorator(func)

