class DebugCSRFMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        # Print out any cookies set in the response
        print("Response cookies:", response.cookies)
        return response