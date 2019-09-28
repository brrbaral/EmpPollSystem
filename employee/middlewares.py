from django.contrib.auth.models import Group
class RoleMiddleware:
    def __init__(self,get_response):
        self.get_response=get_response
        #ONE TIME CONFIGURATION AND INITIALIZATION

    def __call__(self, request):
        # CODE TO BE EXACUTED FOR EACH REQUEST BEFORE THE VIEW(and later middleware) ARE CALLED
        response=self.get_response(request)
        return response


    def process_view(self, request,view_func, *view_args, **view_kargs):
        #THIS METHOD IS FOR EXECUTING SOME CODES
        if request.user.is_authenticated:
            request.role=None
            groups=request.user.groups.all()
            if groups:
                request.role=groups[0].name

    # def process_exception(self,request, exception):
    #     #CALLED FOR THE RESPONSE IF EXCEPTION IS RAISED BY VIEW; RETURN EITHER NONE OR HTTPRESPONSE
    #     pass
    #
    # def process_template_response(self, request, response):
    #     #REQUEST-HTTPREQUEST OBJECT
    #     #RESPONSE- TEMPLATERESPONSE OBJECT
    #     #RETURN TEPLATERESPONSE;USE THIS FOR CHANGING TEMPLATE OR CONTEXT IF IT IS NEEDED
    #     pass