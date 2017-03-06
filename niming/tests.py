from django.test import Client, TestCase
import json

c = Client()
# Create your tests here.

resp = c.get('/wx_login', {'code': 'the code is a mock one'})
uuid = json.loads(resp.content)['uuid']


class TopicCase(TestCase):
    def test_fetch_topics(self):
        res = c.get('/topic/fetch', HTTP_UUID=uuid)
        self.assertEqual(res.status_code, 200)

    def post_topic(self):
        res = c.post('/topic/post', '{"content": "test"}', content_type="application/json", HTTP_UUID=uuid)
        self.assertEqual(res.status_code, 200)

    def test_vote_topic(self):
        res = c.get('/topic/vote', {'topic_id': 2, 'vote_type': 1}, HTTP_UUID=uuid)
        self.assertEqual(res.status_code, 200)

    def test_comment_on_topic(self):
        res = c.post('/topic/post_comment?topic_id=2', '{"content": "test comment"}', content_type="application/json", HTTP_UUID=uuid)
        self.assertEqual(res.status_code, 200)

class CommentCase(TestCase):
    def test_vote_comment(self):
        res = c.get('/comment/vote', {'comment_id': 6, 'vote_type': 1}, HTTP_UUID=uuid)
