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

class CompanyValue(db.Model):
    __tablename__ = 'company_values'

    id = db.Column(db.Integer, primary_key=True)
    id_company = db.Column(db.Integer())
    market_points = db.Column(db.Float(12,6))

    def __init__(self, id_company, market_points):
        self.name = name
        self.id_company = id_company
        self.market_points = market_points

    def __repr__(self):
        return '<id {}>'.format(self.id)
    
    def serialize(self):
        return {
            'id': self.id, 
            'id_company': self.id_company,
            'market_points': self.market_points,
        }



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