# coding: utf8
import boto3
from boto3.session import Session
from Queue import Queue


class kinesis(object):

    def __init__(self, app=None, **kwargs):
        self.app = app
        if app is not None:
            self.init_app(app)
            app.after_request(self.send_events)

            self.queue = Queue()
            credentials = Session().get_credentials()
            try:
                self.kinesis = boto3.client(
                    'firehose',
                    aws_access_key_id=kwargs.get(
                        "aws_access_key_id",
                        credentials.access_key,
                        aws_secret_access_key=kwargs.get('aws_secret_access_key',
                                                         credentials.secret_key),
                        region=kwargs.get("region_name", Session().region_name)
                    ),
                    self.StreamName = kwargs['StreamName']
                )
            except:
                raise TypeError("aws_access_key_id, aws_secret_access_key, region_name, StreamName")

    def init_app(self, app):
        if hasattr(app, "teardown_appcontext"):
            app.teardown_appcontext(self.send_events)
        else:
            app.teardown_request(self.send_events)

    def event(self, evt):
        self.queue(evt)

    def send_events(self, exception):
        while True:
            try:
                evt = self.queue.get_nowait()
            except Empty:
                break
        return Exception
