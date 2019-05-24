# project/tests.py
import unittest
from io import BytesIO

import app


class TestAll(unittest.TestCase):
    def setUp(self):
        app.app.testing = True
        self.app = app.app.test_client()

    def test_file_upload(self):

        data = {
            'file': (BytesIO(b'my file contents'), 'oct.txt'),  # we use StringIO to simulate file object
            'field':'1',
            'tweetdate':'201810'
        }
        # note in that in the previous line you can use 'file' or whatever you want.
        # flask client checks for the tuple (<FileObject>, <String>)
        res = self.app.post('/upload', data=data)
        assert res.status_code == 200

    def test_months_start_end(self):

        data = {
            'start': '201812',
            'end': '201810',
            'field':'1'
        }
        #test case passes only if ValueError is raised.
        with self.assertRaises(ValueError):
            res = self.app.post('/testpy', data=data)

    def test_months_end(self):

        data = {

            'end': '201810',
            'topic':'1'
        }

        with self.assertRaises(ValueError):
            res = self.app.post('/testfuturepy', data=data)








if __name__ == "__main__":
    unittest.main()