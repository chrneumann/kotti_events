import datetime
from pyramid.url import resource_url

from StringIO import StringIO
import Image
import colander
from kotti.views.edit import ContentSchema
from kotti.views.edit import generic_edit
from kotti.views.edit import generic_add
from kotti.views.view import view_node
from kotti.views.util import ensure_view_selector
from kotti.views.util import template_api
from kotti.views.file import AddFileFormView
from kotti.views.file import EditFileFormView
from kotti.views.file import attachment_view
from kotti.views.file import inline_view
from deform.widget import RichTextWidget
from pyramid.i18n import TranslationStringFactory
_ = TranslationStringFactory('kotti_events')
from pyramid.response import Response

from kotti_events.resources import EventFolder
from kotti_events.resources import EventPicture
from kotti_events.resources import Event
from kotti_events.util import get_upcoming_events
from kotti_events.util import get_past_events


class EventFolderSchema(ContentSchema):
    pass

class EventSchema(ContentSchema):
    place = colander.SchemaNode(colander.String(),
                                title=_("Place"))
    body = colander.SchemaNode(
        colander.String(),
        widget=RichTextWidget(theme='advanced', width=790, height=500),
        missing=u"",
        title=_("Body")
        )
    start_date = colander.SchemaNode(
        colander.Date(), title=_("Start date"))
    start_time = colander.SchemaNode(
        colander.Time(), title=_("Start time"))
    end_date = colander.SchemaNode(
        colander.Date(), title=_("End date"))
    end_time = colander.SchemaNode(
        colander.Time(), title=_("End time"))

@ensure_view_selector
def edit_events(context, request):
    return generic_edit(context, request, EventFolderSchema())

def add_events(context, request):
    return generic_add(context, request, EventFolderSchema(), EventFolder, u'calendar')

@ensure_view_selector
def edit_event(context, request):
    return generic_edit(context, request, EventSchema())

def add_event(context, request):
    return generic_add(context, request, EventSchema(), Event, Event.type_info.title)

def view_eventfolder(context, request):
    return {
        'api': template_api(context, request),
        'upcoming_events': get_upcoming_events(context),
        'past_events': get_past_events(context),
        }

class AddEventPictureFormView(AddFileFormView):
    def add(self, **appstruct):
        buf = appstruct['file']['fp'].read()
        return EventPicture(
            title=appstruct['title'],
            description=appstruct['description'],
            data=buf,
            filename=appstruct['file']['filename'],
            mimetype=appstruct['file']['mimetype'],
            size=len(buf),
            )


class EditEventPictureFormView(EditFileFormView):
    pass

def thumbnail_view(context, request, size=(180,112)):
    img = Image.open(StringIO(context.data))
    img.thumbnail(size)
    thumbnail = StringIO()
    img.save(thumbnail, img.format)
    res = Response(
        headerlist=[
            ('Content-Length', str(len(thumbnail.getvalue()))),
            ('Content-Type', str(context.mimetype)),
            ],
        app_iter=thumbnail.getvalue(),
        )
    return res

def icon_view(context, request):
    return thumbnail_view(context, request, (90,56))

def includeme_edit(config):
    config.add_view(
        edit_events,
        context=EventFolder,
        name='edit',
        permission='edit',
        renderer='kotti:templates/edit/node.pt',
        )

    config.add_view(
        add_events,
        name=EventFolder.type_info.add_view,
        permission='add',
        renderer='kotti:templates/edit/node.pt',
        )

    config.add_view(
        edit_event,
        context=Event,
        name='edit',
        permission='edit',
        renderer='kotti:templates/edit/node.pt',
        )

    config.add_view(
        add_event,
        name=Event.type_info.add_view,
        permission='add',
        renderer='kotti:templates/edit/node.pt',
        )

    config.add_view(
        AddEventPictureFormView,
        name=EventPicture.type_info.add_view,
        permission='add',
        renderer='kotti:templates/edit/node.pt',
        )

    config.add_view(
        EditEventPictureFormView,
        context=EventPicture,
        name='edit',
        permission='edit',
        renderer='kotti:templates/edit/node.pt',
        )

def includeme_view(config):
    config.add_view(
        thumbnail_view,
        context=EventPicture,
        name='thumbnail-view',
        permission='view',
        )

    config.add_view(
        icon_view,
        context=EventPicture,
        name='icon-view',
        permission='view',
        )

    config.add_view(
        inline_view,
        context=EventPicture,
        name='inline-view',
        permission='view',
        )

    config.add_view(
        attachment_view,
        context=EventPicture,
        name='attachment-view',
        permission='view',
        )

    config.add_view(
        context=EventPicture,
        name='view',
        permission='view',
        renderer='templates/eventpicture-view.pt',
        )

    config.add_view(
        view_eventfolder,
        context=EventFolder,
        name='view',
        permission='view',
        renderer='templates/eventfolder-view.pt',
        )

    config.add_view(
        view_node,
        context=Event,
        name='view',
        permission='view',
        renderer='templates/event-view.pt',
        )

    config.add_static_view('static-kotti_events', 'kotti_events:static')

def includeme(config):
    config.add_translation_dirs('kotti_events:locale/')
    includeme_edit(config)
    includeme_view(config)
