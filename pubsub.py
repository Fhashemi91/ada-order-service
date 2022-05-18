from google.cloud import pubsub_v1
from google.api_core.exceptions import AlreadyExists

publisher = pubsub_v1.PublisherClient()

topic_name = 'projects/ada-return/topics/order'


try:
    publisher.create_topic(name=topic_name)
except AlreadyExists:
    pass

def submit_message(message, topic=topic_name, **kwargs):
    future = publisher.publish(topic, message.encode(), **kwargs)
    return future.result()
