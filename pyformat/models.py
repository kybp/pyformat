from pyformat import db

class Paste(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text)

    def __init__(self, text):
        self.text = text

    def __repr__(self):
        return '<Paste: {}>'.format(self.id)
