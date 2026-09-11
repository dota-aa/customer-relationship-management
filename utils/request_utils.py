from rest_framework.request import Request


def get_client_ip(request: Request):
    """
    get user ip from X_FORWARDED_FOR list -> [client_ip, proxy_1, proxy_2, ...]
    if there was no xff it gets user ip from REMOTE_ADDR
    """
    xff = request.META.get('HTTP_X_FORWARDED_FOR')
    ip = xff.split(',')[0] if xff else request.META.get('REMOTE_ADDR')
    return ip


def get_user_agent(request: Request):
    user_agent = request.META.get('HTTP_USER_AGENT')
    return user_agent
