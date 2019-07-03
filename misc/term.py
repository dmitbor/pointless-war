class Term:
    term_name = ""
    term_plural = ""
    associations = []

    def __init__(self):
        self.term_name = ""
        self.term_plural = ""
        self.associations = []

    def set_name(self, given_name):
        self.term_name = given_name

    def set_plural(self, given_plural):
        self.term_plural = given_plural

    def set_assocs(self, given_assocs):
        self.associations = given_assocs

    def get_name(self):
        return self.term_name
