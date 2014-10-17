from feeddb.feed.util import FeedUploadStatus
from django.http import HttpResponseRedirect

class FeedUploadStatusMiddleware():
    def process_request(self, request):
        request.feed_upload_status = FeedUploadStatus(session=request.session)

    def process_view(self, request, view_func, view_args, view_kwargs):
        changed_params = request.feed_upload_status.update_with_querystring(request.GET)
        try:
            is_add_view = view_func.__name__ == 'add_view'
        except AttributeError:
            is_add_view = False

        if is_add_view and changed_params != False:
            qs = changed_params.urlencode()
            if len(qs):
                return HttpResponseRedirect(request.path + '?' + qs)
            else:
                return HttpResponseRedirect(request.path)
