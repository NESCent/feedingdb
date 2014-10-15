from feeddb.feed.util import FeedUploadStatus
from django.http import HttpResponseRedirect

class FeedUploadStatusMiddleware():
    def process_request(self, request):
        request.feed_upload_status = FeedUploadStatus(session=request.session)
        changed_params = request.feed_upload_status.update_with_querystring(request.GET)
        if changed_params:
            qs = changed_params.urlencode()
            if len(qs):
                return HttpResponseRedirect(request.path + '?' + qs)
            else:
                return HttpResponseRedirect(request.path)
