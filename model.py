from database import db
from datetime import datetime
from sqlalchemy.dialects.postgresql import JSONB  #

class Influencer(db.Model):
    __tablename__ = 'influencers'
    influencer_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    url = db.Column(db.String(255))
    created_at = db.Column(db.DateTime)

    links = db.relationship('Link', backref='influencer', lazy=True)
    visitors = db.relationship('Visitor', backref='influencer', lazy=True)
    # Adicione relações conforme necessário

class Link(db.Model):
    __tablename__ = 'links'
    link_id = db.Column(db.Integer, primary_key=True)
    link_name = db.Column(db.String(255), nullable=False)
    url = db.Column(db.String(500),nullable=False)
    url_reduced = db.Column(db.String(100),nullable=False)
    isvisible = db.Column(db.Boolean, default=False)
    influencer_id = db.Column(db.Integer, db.ForeignKey('influencers.influencer_id'))
    created_at = db.Column(db.DateTime , default=datetime.utcnow)

    visitors = db.relationship('Visitor', backref='link', lazy=True)
    # Adicione mais modelos conforme necessário

# Defina outros modelos seguindo a mesma estrutura
    
class Manager(db.Model):
    __tablename__ = 'managers'
    manager_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(100))
    password = db.Column(db.String(255))

class GroupInfo(db.Model):
    __tablename__ = 'group_infos'
    group_info_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

class Visitor(db.Model):
    __tablename__ = 'visitors'
    visitor_id = db.Column(db.Integer, primary_key=True)
    influencer_id = db.Column(db.Integer, db.ForeignKey('influencers.influencer_id'), nullable=False)
    referer = db.Column(db.Text)
    location = db.Column(db.String(100))
    link_id = db.Column(db.Integer, db.ForeignKey('links.link_id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    headers = db.Column(JSONB, default={})

def get_data():
    return {"mensagem": "Olá, Mundo!"}