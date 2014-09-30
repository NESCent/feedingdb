from django.contrib.admin.views.main import ChangeList

class FeedChangeList(ChangeList):
    def __init__(self, *args, **kwargs):
        request = kwargs.get('request', None)
        if request is not None:
            self.request = request
        super(FeedChangeList, self).__init__(*args, **kwargs)
