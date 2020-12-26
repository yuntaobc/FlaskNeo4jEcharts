from flask_wtf import FlaskForm
from wtforms import StringField, DateTimeField, SubmitField


class EventUserForm(FlaskForm):
    name = StringField("Event name to search",
                       render_kw={'oninput': 'event_list()',
                                  'placeholder': 'Event name to search',
                                  'id': 'name-input',
                                  'class': 'typeahead',
                                  'autocomplate': 'off',
                                  'data-provide': 'typeahead'})
    s_time = DateTimeField(format='%Y-%m-%dT%H:%M:%S')
    e_time = DateTimeField(format='%Y-%m-%dT%H:%M:%S')
    submit = SubmitField("Search")
