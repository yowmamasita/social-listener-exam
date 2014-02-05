from ferrisnose import AppEngineTest
from ferris.core import mail


class MailTest(AppEngineTest):

    def test(self):
        res, body = mail.send_template(
            sender='user@example.com',
            recipient='test@example.com',
            subject='Hello!',
            template_name='ferris_test',
            context={
                'name': 'Doctor'
            })

        assert 'Doctor' in body
