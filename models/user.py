from app import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    company = db.Column(db.String())
    document = db.Column(db.String())
    username = db.Column(db.String())
    password = db.Column(db.String())

    def __init__(self, name, company, document, username, password):
        self.name = name
        self.company = company
        self.document = document
        self.username = username
        self.password = password

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'company': self.company,
            'document':self.document,
            'username':self.username,
            'password':self.password
        }
    def serializeWithoutPassword(self):
            return {
            'id': self.id,
            'name': self.name,
            'company': self.company,
            'document':self.document,
        }
