from datetime import datetime
from sqlalchemy import desc
from kotti import DBSession
from kotti_events.resources import Event

def get_upcoming_events(folder):
    """
    Get upcoming events in given folder.
    """
    session = DBSession()
    now = datetime.now()
    events = session.query(Event)\
        .filter(Event.parent_id==folder.id)\
        .filter(Event.start_date >= now)\
        .order_by(Event.start_date, Event.start_time)\
        .all()
    return events

def get_past_events(folder, limit=None):
    """
    Get past events in given folder.
    """
    session = DBSession()
    now = datetime.now()
    query = session.query(Event)\
        .filter(Event.parent_id==folder.id)\
        .filter(Event.start_date < now)\
        .order_by(desc(Event.start_date), desc(Event.start_time))
    events = (limit and query.limit(limit) or query).all()
    return events
