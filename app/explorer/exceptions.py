class ThomasLaPoule(Exception):
    def __init__(self, arg):
        self.msg = arg
class QueryFormatNotValide(Exception):
    def __init__(self, arg):
        self.msg = arg
