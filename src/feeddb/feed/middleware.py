from feeddb.feed.util import FeedUploadStatus
from django.http import HttpResponseRedirect

class FeedUploadStatusMiddleware():
    def process_request(self, request):
        request.feed_upload_status = FeedUploadStatus(session=request.session)
        request.feed_upload_status.update_with_querystring(request.GET)
