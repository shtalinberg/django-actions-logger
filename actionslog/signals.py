from django.dispatch import Signal


action_logged = Signal(providing_args=["action"])
