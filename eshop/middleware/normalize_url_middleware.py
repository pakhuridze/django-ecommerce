from django.http import HttpResponsePermanentRedirect
import re
  
class NormalizeUrlMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Normalize slashes by removing extra trailing slashes
        normalized_path = re.sub(r'/+', '/', request.path)

        # Check if the path has changed
        if normalized_path != request.path:
            # Redirect to the cleaned version of the URL
            return HttpResponsePermanentRedirect(normalized_path)

        # Call the next middleware or view
        return self.get_response(request)
