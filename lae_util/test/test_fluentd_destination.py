# Copyright Least Authority Enterprises.
# See LICENSE for details.

"""
Tests for ``lae_util.fluentd_destination``.
"""

from __future__ import unicode_literals

from testtools.matchers import (
    MatchesStructure,
    Equals,
    IsInstance,
)

from twisted.python.url import URL
from twisted.web.resource import Resource
from twisted.web.server import Site
from twisted.web.client import Agent
from twisted.internet.task import deferLater
from twisted.trial.unittest import TestCase as AsyncTestCase

from lae_util.testtools import TestCase

from ..fluentd_destination import (
    FluentdDestination,
    _parse_destination_description,
)


class Collector(Resource):
    def __init__(self):
        Resource.__init__(self)
        self.collected = []


    def render_POST(self, request):
        self.collected.append(request.content.read())
        return b""



class FluentdDestinationTests(AsyncTestCase):
    def test_posted(self):
        root = Resource()
        collector = Collector()
        root.putChild(b"foo", collector)

        from twisted.internet import reactor
        while True:
            try:
                port = reactor.listenTCP(0, Site(root))
            except:
                pass
            else:
                self.addCleanup(port.stopListening)
                port_number = port.getHost().port
                break

        fluentd_url = URL(
            scheme="http",
            host="127.0.0.1",
            port=port_number,
            path=["foo"],
        )

        agent = Agent(reactor)
        destination = FluentdDestination(agent, fluentd_url)
        destination({"hello": "world"})

        def check():
            self.assertEquals(collector.collected, [b'json={"hello": "world"}'])

        return deferLater(reactor, 0.1, check)



class  ParseDestinationDescriptionTests(TestCase):
    def test_fluentd_destination(self):
        reactor = object()
        self.assertThat(
            _parse_destination_description("fluentd:http://foo/bar")(reactor),
            MatchesStructure(
                agent=IsInstance(Agent),
                fluentd_url=Equals(
                    URL(scheme=u"http", host=u"foo", path=[u"bar"]),
                ),
            )
        )
