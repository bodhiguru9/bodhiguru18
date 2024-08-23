from rest_framework.throttling import AnonRateThrottle

class UserBasedAnonRateThrottle(AnonRateThrottle):
    def allow_request(self, request, view):
        if request.user.is_authenticated:
            return True
        return super().allow_request(request, view)
    
    def wait(self):
        return 24 * 60 * 60
