import json
import logging
from dataclasses import asdict

from redis import Redis

from allocation import config
from allocation.domain import events


logger = logging.getLogger(__name__)

r = Redis(**config.get_redis_host_and_port())


def publish(channel, event: events.Event):
    logging.info("publishing: channel=%s, event=%s", channel, event)
    r.publish(channel, json.dumps(asdict(event)))