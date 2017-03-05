import uuid
import json

from django.db import models

VOTE_TYPE = (
    (0, 'up',),
    (1,'down',),
)

DB_STATUS = (
    (-1, 'deleted',),
)


class NimingModel(models.Model):
    @staticmethod
    def get_by_id(pk):
        data = list(NimingModel.objects.all().filter(pk=pk))
        if data:
            return data[0]


# Create your models here.
class User(NimingModel):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    create_time = models.DateTimeField(auto_now_add=True)
    edit_time = models.DateTimeField(auto_now=True)
    open_id = models.CharField(max_length=100)
    nick_name = models.CharField(max_length=100)

    @staticmethod
    def create_or_get(open_id='', uuid=''):
        user = None

        if open_id:
            user = User.objects.all().filter(open_id=open_id)
        if uuid:
            user = User.objects.all().filter(uuid=uuid)

        if user:
            return user[0]
        elif open_id:
            user = User(open_id=open_id)
            user.save()
            return user

class Topic(NimingModel):
    create_time = models.DateTimeField(auto_now_add=True)
    edit_time = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(User)
    content = models.TextField(default='')
    db_status = models.IntegerField(choices=DB_STATUS, default=0)
    order = models.IntegerField(default=0)


class VoteOnTopic(NimingModel):
    create_time = models.DateTimeField(auto_now_add=True)
    edit_time = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(User)
    vote_type = models.IntegerField(default=-1, choices=VOTE_TYPE)
    topic = models.ForeignKey(Topic)

    @staticmethod
    def vote_of_topic(topic):
        votes = VoteOnTopic.objects.all().filter(topic=topic)
        sum = 0
        for vote in votes:
            sum += vote.vote_type

        return sum

    @staticmethod
    def vote_status(user, topic):
        votes = VoteOnTopic.objects.all().filter(creator=user, topic=topic)
        if votes:
            vote = votes[0]
            return vote.type
        else:
            return 0


class Comment(NimingModel):
    create_time = models.DateTimeField(auto_now_add=True)
    edit_time = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(User)
    topic = models.ForeignKey(Topic)
    content = models.TextField(default='')
    db_status = models.IntegerField(choices=DB_STATUS, default=0)
    replies = models.TextField(default='')
    order = models.IntegerField(default=0)


    @staticmethod
    def all_comments(topic, user):
        raw_comments = Comment.objects.all().filter(topic=topic)
        comments = []
        for comment in raw_comments:
            comments.append({
                'content': comment.content,
                'time': comment.create_time,
                'vote': {
                    'number': VoteOnComment.vote_of_comment(comment),
                    'status': VoteOnComment.vote_type(user, comment)
                }
            })


    def reply(self, creator, content, reply_id):
        replies = self.get_replies()

        new_reply = {
            'create_time': '',
            'content': content,
            'creator': creator.pk,
            'reply_id': reply_id,
        }

    def get_replies(self):
        return json.loads(self.replies)


class VoteOnComment(NimingModel):
    create_time = models.DateTimeField(auto_now_add=True)
    edit_time = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(User)
    vote_type = models.IntegerField(default=-1, choices=VOTE_TYPE)
    comment = models.ForeignKey(Topic)

    @staticmethod
    def vote_of_comment(comment):
        votes = VoteOnComment.objects.all().filter(comment=comment)
        sum = 0
        for vote in votes:
            sum += vote.vote_type

        return sum

    @staticmethod
    def vote_status(user, comment):
        votes = VoteOnComment.objects.all().filter(creator=user, comment=comment)
        if votes:
            vote = votes[0]
            return vote.type
        else:
            return 0
