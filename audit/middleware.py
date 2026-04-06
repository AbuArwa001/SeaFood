import threading

_thread_locals = threading.local()

def get_current_user():
    return getattr(_thread_locals, 'user', None)

class ThreadLocalUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = getattr(request, 'user', None)

        # DRF JWT Authentication check inside standard middleware
        if not user or not user.is_authenticated:
            auth_header = request.headers.get('Authorization')
            if auth_header and auth_header.startswith('Bearer '):
                try:
                    from rest_framework_simplejwt.authentication import JWTAuthentication
                    jwt_authenticator = JWTAuthentication()
                    tup = jwt_authenticator.authenticate(request)
                    if tup is not None:
                        user, _ = tup
                except Exception:
                    pass

        if user and user.is_authenticated:
            _thread_locals.user = user
        else:
            _thread_locals.user = None

        response = self.get_response(request)

        if hasattr(_thread_locals, 'user'):
            del _thread_locals.user

        return response
