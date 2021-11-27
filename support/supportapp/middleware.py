from django.http import JsonResponse
import jwt


class CheckAuthentication:

    def __init__(self, get_response):
        self._get_response = get_response

    def __call__(self, request):
        return self._get_response(request)

    def process_exception(self, request, exception):
        token = request.COOKIES.get('jwt')

        if not token:
            return JsonResponse({'detail': 'Unauthenticated!'})
        try:
            jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return JsonResponse({'detail': 'Unauthenticated!'})

        response = self._get_response(request)
        return response
