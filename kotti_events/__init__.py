def kotti_configure(settings):
    settings['kotti.includes'] += ' kotti_events.views'
    settings['kotti.available_types'] += ' kotti_events.resources.EventFolder'
    settings['kotti.available_types'] += ' kotti_events.resources.Event'
    settings['kotti.available_types'] += ' kotti_events.resources.EventPicture'
