from flask_wtf import FlaskForm
from wtforms import StringField, DateTimeField, SubmitField


class EventForm(FlaskForm):
    name = StringField("Event name to search",
                       render_kw={
                           'placeholder': 'Name to search',
                           'id': 'name-input',
                           'class': 'typeahead',
                           'autocomplate': 'off',
                           'data-provide': 'typeahead'})
    s_time = DateTimeField(format='%Y-%m-%dT%H:%M:%S',
                           render_kw={
                               'id': 's-time'
                           })
    e_time = DateTimeField(format='%Y-%m-%dT%H:%M:%S',
                           render_kw={
                               'id': 'e-time'
                           })
    submit = SubmitField("Search")
