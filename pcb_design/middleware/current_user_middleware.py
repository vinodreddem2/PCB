import threading

_local = threading.local()  # Thread-local storage

class CurrentUserMiddleware:
    """
    Middleware to capture the current user from the request and store it in a thread-local variable.
    """
    # Middleware Initialization
    def __init__(self, get_response):
        # get_response is used to call the next middleware or the view in the request/response cycle. 
        self.get_response = get_response
    
    #  Capturing the User
    def __call__(self, request):
        # Store the user in thread-local storage
        print(request.user)
        _local.user = getattr(request, 'user', None)

        # Proceed with the request
        response = self.get_response(request)

        # Clean up after the request is complete
        _local.user = None
        return response

