import json
import urllib2

from django.shortcuts import render
from django.http.response import JsonResponse, HttpResponseForbidden, HttpResponse
from django.http.request import HttpRequest

from models import *


def require_login(func):
    @json_response
    def dec(request, *args, **kwargs):
        uuid = request.META.get('HTTP_UUID', '')
        if not uuid:
            return HttpResponseForbidden()

        user = User.create_or_get(uuid=uuid)
        if not user:
            return HttpResponseForbidden()
        request.current_user = user
        return func(request, *args, **kwargs)

    return dec


def json_response(func):
    def dec(request, *args, **kwargs):
        res = func(request, *args, **kwargs)
        if isinstance(res, HttpResponse):
            return res

        res = JsonResponse(res, safe=False)
        return res
    return dec


@json_response
def wx_login(request):
    code = request.GET.get('code')

    # app_id = ''
    # secret = ''
    # wx_url = 'https://api.weixin.qq.com/sns/jscode2session?appid=%s&secret=%s&js_code=%s&grant_type=authorization_code' % (
    #     app_id,
    #     secret,
    #     code,
    # )
    #
    # rep = urllib2.urlopen(wx_url)
    # data = json.loads(rep.read())
    # openid = data['openid']
    #
    openid = code
    user = User.create_or_get(openid)

    return {
        'uuid': user.uuid.hex,
    }


@require_login
def post_topic(request):
    data = json.loads(request.body)

    topic = Topic()
    topic.creator = request.current_user
    topic.content = data['content']

    if data['content']:
        topic.save()

    return {
        'rc': 0
    }


@require_login
def fetch_topics(request):
    order = request.GET.get('order', 'new')

    raw_topics = Topic.objects.all().order_by('-create_time')
    topics = []
    for topic in raw_topics:
        comments = Comment.all_comments(topic, request.current_user)
        topics.append({
            'id': topic.pk,
            'content': topic.content,
            'time': topic.create_time,
            'vote': {
                'number': VoteOnTopic.vote_of_topic(topic),
                'status': VoteOnTopic.vote_status(request.current_user, topic)
            },
            'comments': comments
        })

    return {
        'data': topics
    }


@require_login
def vote_topic(request):
    topic_id = request.GET.get('topic_id')
    topic = Topic.get_by_id(topic_id)
    vote_type = request.GET.get('type', '1')

    if not topic:
        return False

    vote = VoteOnTopic.create_or_get(request.current_user, topic)
    vote.vote_type = int(vote_type)

    vote.save()

    return True


@require_login
def post_comment_on_topic(request):
    topic_id = request.GET.get('topic_id')
    data = json.loads(request.body)
    topic = Topic.get_by_id(topic_id)

    if not topic:
        return False

    comment = Comment()
    comment.creator = request.current_user
    comment.content = data['content']
    comment.topic = topic

    comment.save()

    return True


def post_comment_on_comment(request):
    comment_id = request.GET.get('comment_id')
    reply_id = request.GET.get('reply_id', '-1')
    comment = Topic.get_by_id(comment_id)
    data = json.loads(request.body)

    if not comment:
        return False

    comment.reply(request.current_user, data['content'], reply_id)

    return True


@require_login
def vote_comment(request):
    comment_id = request.GET.get('comment_id')
    comment = Comment.get_by_id(comment_id)
    vote_type = request.GET.get('type', '1')

    if not comment:
        return False

    vote = VoteOnComment.create_or_get(request.current_user, comment)
    vote.vote_type = int(vote_type)

    vote.save()

    return True
