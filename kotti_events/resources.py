from sqlalchemy import Table
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy import Time
from sqlalchemy import Date
from sqlalchemy import Integer
from sqlalchemy.orm import mapper
from kotti import metadata
from kotti.resources import Content
#from kotti.util import _
_ = lambda x: x

class EventFolder(Content):
    type_info = Content.type_info.copy(
        name=u'EventFolder',
        add_view=u'add_eventfolder',
        addable_to=[u'Document'],
        )

    def __init__(self, **kwargs):
        super(EventFolder, self).__init__(**kwargs)

eventfolders = Table(
    'event_folders', metadata,
    Column('id', Integer, ForeignKey('contents.id'), primary_key=True),
)

mapper(EventFolder, eventfolders, inherits=Content,
       polymorphic_identity='event_folders')

class Event(Content):
    type_info = Content.type_info.copy(
        name=u'Event',
        add_view=u'add_event',
        addable_to=[u'EventFolder'],
        )

    def __init__(self, place=u"", body=u"", start_date=None,
                 end_date=None, start_time=None, end_time=None, **kwargs):
        super(Event, self).__init__(in_navigation=False, **kwargs)
        self.place = place
        self.body = body
        self.start_date = start_date
        self.start_time = start_time
        self.end_date = end_date
        self.end_time = end_time

events = Table('events', metadata,
    Column('id', Integer, ForeignKey('contents.id'), primary_key=True),
    Column('place', String(100)),
    Column('body', Text()),
    Column('start_date', Date()),
    Column('start_time', Time(), nullable=True),
    Column('end_date', Date(), nullable=True),
    Column('end_time', Time(), nullable=True),
)

mapper(Event, events, inherits=Content, polymorphic_identity='events')
