'''
Blueprint for the commands classes
'''


class Command(object):
    def __init__(self, name, summary):

        self.name = name
        self.summary = summary

    @staticmethod
    def add_args(args):
        raise NotImplementedError
        return

    @staticmethod
    def run(**kwargs):
        raise NotImplementedError
        return
