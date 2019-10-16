from app import db

class CompanyValue(db.Model):
    __tablename__ = 'company_values'

    id = db.Column(db.Integer, primary_key=True)
    id_company = db.Column(db.Integer())
    market_points = db.Column(db.Float(12,6))

    def __init__(self, id_company, market_points):
        self.id_company = id_company
        self.market_points = market_points

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'id_company': self.id_company,
            'market_points': str(self.market_points),
        }
