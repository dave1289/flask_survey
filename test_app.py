from unittest import TestCase
from app import app
from flask import session

app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']


class ColorFormTestCase(TestCase):
    def test_home(self):
        with app.test_client() as client:
            res = client.get('/')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<a href="/questions">', html)

    def test_redirect(self):
        with app.test_client() as client:
            res = client.get('/old-home')

            self.assertEqual(res.status_code, 302)
            self.assertEqual(res.location, '/')

    def test_redirect_follow(self):
        with app.test_client() as client:
            res = client.get('/old-home', follow_redirects=True)
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<a href="/questions">', html)

    def test_about(self):
        with app.test_client() as client:
            res = client.get('/about-us')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<h1 class="text-center display-1">Survey Engine</h1>', html)

   #  def test_session_count(self):
   #      with app.test_client() as client:
   #          res = client.get('/')

   #      self.assertEqual(res.status_code, 200)
   #      self.assertEqual(session['count'], 1)

   #  def test_session_count_multiple(self):
   #      with app.test_client() as client:
   #          with client.session_transaction() as change_session:
   #              change_session['count'] = 999
   #              res = client.get('/')
        
   #              self.assertEqual(res.status_code, 200)
   #              self.assertEqual(session['count', 1000])