from app import db

class Company(db.Model):
    __tablename__ = 'companies'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    financial_code = db.Column(db.String())

    def __init__(self, name, financial_code):
        self.name = name
        self.financial_code = financial_code

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'financial_code': self.financial_code,
        }
