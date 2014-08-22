from feeddb.feed.util import FeedUploadStatus

class FeedUploadStatusMiddleware():
    def process_request(self, request):
        request.feed_upload_status = FeedUploadStatus(session=request.session)
