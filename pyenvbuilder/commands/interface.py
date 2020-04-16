'''
Blueprint for the commands classes
'''


class Command(object):
    def __init__(self, name, summary):

        self.name = name
        self.summary = summary

    def add_args(self, args):
        raise NotImplementedError
        return

    def run(self, **kwargs):
        raise NotImplementedError
        return
