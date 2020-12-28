from flask import render_template, session, redirect, url_for
from .forms import EventForm
from . import main


@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@main.route('/event/<item>', methods=['GET', 'POST'])
def event(item):
    if item == 'user':
        page = 'event_user.html'
        form = EventForm()
    elif item == 'topic':
        page = 'event_topic.html'
        form = EventForm()
    elif item == 'neighbor':
        page = 'event_neighbor.html'
        form = EventForm()
    elif item == 'info':
        page = 'event_info.html'
        form = ''
    return render_template(page, form=form)


@main.route('/user', methods=['GET', 'POST'])
def user():
    return render_template('user.html')


@main.route('/topic', methods=['GET', 'POST'])
def topic():
    return render_template('topic.html')


@main.route('/favicon.ico', methods=['GET', 'POST'])
def image():
    return (
        'data:image/vnd.microsoft.icon;base64,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FP/wfRT/8H0U//B9FP/wfRT/8H0U//B9FP/wfRT/8H0U//B9FP/wfRT/8H0U9e98FFcAAAAA73wUAPB9FJLwfRT/8H0U//B9FP/wfRT/8H0U//B9FP/wfRT/8H0U//B9FP/wfRT/8H0U//B9FP/wfRT/8H0U//B9FP/wfRT/8H0U//B9FP/wfRT/8H0U//B9FP/wfRT/8H0U//B9FP/wfRT/8H0U//B9FP/wfRT+8H0Uke98FADvfBQC8H0UqPB9FP/wfRT/8H0U//B9FP/wfRT/8H0U//B9FP/wfRT/8H0U//B9FP/wfRT/8H0U//B9FP/wfRT/8H0U//B9FP/wfRT/8H0U//B9FP/wfRT/8H0U//B9FP/wfRT/8H0U//B9FP/wfRT/8H0U//B9FP/wfRSo73wUAu98FBXwfRS68H0U//B9FP/wfRT/8H0U//B9FP/wfRT/8H0U//B9FP/wfRT/8H0U//B9FP/wfRT/8H0U//B9FP/wfRT/8H0U//B9FP/wfRT/8H0U//B9FP/wfRT/8H0U//B9FP/wfRT/8H0U//B9FP/wfRT/8H0U//B9FLrvfBQV73wUFvB9FLzwfRT/8H0U//B9FP/wfRT/8H0U//B9FP/wfRT/8H0U//B9FP/wfRT/8H0U//B9FP/wfRT/8H0U//B9FP/wfRT/8H0U//B9FP/wfRT/8H0U//B9FP/wfRT/8H0U//B9FP/wfRT/8H0U//B9FP/wfRT/8H0Uu+98FBXvfxAI8H0UrvB9FP/wfRT/8H0U//B9FP/wfRT/8H0U//B9FP/wfRT/8H0U//B9FP/wfRT/8H0U//B9FP/wfRT/8H0U//B9FP/wfRT/8H0U//B9FP/wfRT/8H0U//B9FP/wfRT/8H0U//B9FP/wfRT/8H0U//B9FP/wfRSr738RBO99EwDwfRSk8H0U//B9FP/wfRT/8H0U2vF9FJfwfRTh8H0U//B9FP/wfRT/8H0U//B9FP/wfRT/8H0U//B9FP/wfRT/8H0U//B9FP/wfRT/8H0U//B9FP/wfRT/8H0U//B9FP/wfRT/8H0U//B9FP/wfRT/8H0U//B9E53vfRMAAAAAAPB8FHzwfRT78H0U//B9FP/wfRSU8XwTCvB9E4LwfRT78H0U//B9FP/wfRT/8H0U//B9FP/wfRT/8H0U//B9FP/wfRT/8H0U//B9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')
