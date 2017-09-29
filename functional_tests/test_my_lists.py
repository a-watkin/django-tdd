from django.conf import settings
from .base import FunctionalTest
from .server_tools import create_session_on_server
from .management.commands.create_session import create_pre_authenticated_session

""" 
Note that, as it is, this will only work because we’re using
LiveServerTestCase, so the User and Session objects we create will end up in
the same database as the test server. Later we’ll need to modify it so that it
works against the database on the staging server too. 
"""


class MyListsTest(FunctionalTest):

    def create_pre_authenticated_session(self, email):

        if self.staging_server:
            session_key = create_session_on_server(self.staging_server, email)
        else:
            session_key = create_pre_authenticated_session(email)
        ## to set a cookie we need to first visit the domain.
        ## 404 pages load the quickest!
        self.browser.get(self.live_server_url + "/404_no_such_url/")
        self.browser.add_cookie(dict(
            name=settings.SESSION_COOKIE_NAME,
            value=session_key,
            path='/',
        ))


        # user = User.objects.create(email=email)
        # session = SessionStore()
        # session[SESSION_KEY] = user.pk
        # session[BACKEND_SESSION_KEY] = settings.AUTHENTICATION_BACKENDS[0]
        # session.save()
        # ## to set a cookie we need to first visit the domain.
        # ## 404 pages load the quickest!
        # self.browser.get(self.live_server_url + "/404_no_such_url/")
        # self.browser.add_cookie(dict(
        #     name=settings.SESSION_COOKIE_NAME,
        #     value=session.session_key,
        #     path='/',
        # ))


    def test_logged_in_users_lists_are_saved_as_my_lists(self):
        email = 'edith@example.com'
        self.browser.get(self.live_server_url)
        self.wait_to_be_logged_out(email)

        # Edith is a logged-in user
        self.create_pre_authenticated_session(email)
        self.browser.get(self.live_server_url)
        self.wait_to_be_logged_in(email)

