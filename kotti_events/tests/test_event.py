from datetime import datetime

from kotti.testing import UnitTestBase

class TestEventPictureMethods(UnitTestBase):
    """
    Test methods which operate on the event's pictures.
    """
    def setUp(self):
        from kotti_events.resources import Event
        self.event = Event(u"Frankfurt", u"<b>Awesome!</b>",
                           datetime.now, None, None, None)

        from kotti_events.resources import EventPicture
        for name in ['foo', 'bar', 'cruz']:
            self.event[name] = EventPicture(name=name, mimetype=u'image/jpeg')

        self.emty_event = Event(u"Frankfurt", u"<b>Awesome!</b>",
                                datetime.now, None, None, None)
                          
    def test_get_icon(self):
        icon = self.event.get_icon()
        assert icon.name == 'foo'

        icon = self.emty_event.get_icon()
        assert icon == None

    def test_get_pictures(self):
        pictures = list(self.event.get_pictures())
        assert len(pictures) == 3
        assert pictures[2].name == 'cruz'

        pictures = list(self.emty_event.get_pictures())
        assert len(pictures) == 0
