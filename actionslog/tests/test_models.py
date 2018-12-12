
"""Model tests."""

from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.test import TestCase
# from django.utils.encoding import force_text

from actionslog.models import LogAction


class ModelTestCase(TestCase):
    """This class defines the test suite for the bucketlist model."""

    def setUp(self):
        """Define the test client and other test variables."""
        self.user = User.objects.create(username="nerd") # ADD THIS LINE
        self.status_msg = 'Reset password success'


    def test_model_manager(self):
        la_kwargs = {
            'instance': self.user,
            'user': self.user,
            'action_info': {'info': self.status_msg},
        }
        LogAction.objects.create_log_action(**la_kwargs)

