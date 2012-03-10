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
from kotti.resources import File
from pyramid.i18n import TranslationStringFactory
_ = TranslationStringFactory('kotti_events')

class EventFolder(Content):
    type_info = Content.type_info.copy(
        name=u'EventFolder',
        title=_(u"Event folder"),
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
       polymorphic_identity='event_folder')

class Event(Content):
    type_info = Content.type_info.copy(
        name=u'Event',
        title=_(u'Event'),
        add_view=u'add_event',
        addable_to=[u'EventFolder'],
        )

    def get_pictures(self):
        # TODO: Check on add, not view.
        supported_mimetypes = ['image/jpeg', 'image/png', 'image/gif']
        for child in self.keys():
            if (self[child].type_info.name == EventPicture.type_info.name
                and self[child].mimetype in supported_mimetypes):
                yield self[child]

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

mapper(Event, events, inherits=Content, polymorphic_identity='event')

class EventPicture(File):
    type_info = File.type_info.copy(
        name=u'EventPicture',
        title=_(u'Event picture'),
        add_view=u'add_eventpicture',
        addable_to=[u'Event'],
        )

    def __init__(self, **kwargs):
        super(EventPicture, self).__init__(in_navigation=False, **kwargs)

event_pictures = Table('event_pictures', metadata,
    Column('id', Integer, ForeignKey('files.id'), primary_key=True),
)

mapper(EventPicture, event_pictures, inherits=File,
       polymorphic_identity='event_picture')
