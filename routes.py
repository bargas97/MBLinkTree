# route.py

from flask import Blueprint, jsonify, request
from model import Manager, get_data
from model import Influencer
from flask import request
from model import Manager, GroupInfo, Visitor  # Importe os modelos adicionais aqui
from database import db

api_blueprint = Blueprint('api', __name__)

@api_blueprint.route('/{name}', methods=['GET'])
def get_influencers():
    influencers_list = Influencer.query.all()
    return jsonify([{"influencer_id": influencer.influencer_id, "name": influencer.name} for influencer in influencers_list])

@api_blueprint.route('/managers', methods=['POST'])
def create_manager():
    data = request.get_json()
    new_manager = Manager(user_name=data['user_name'], password=data['password'])
    db.session.add(new_manager)
    db.session.commit()
    return jsonify({"message": "Manager created successfully"}), 201

@api_blueprint.route('/visitors', methods=['GET'])
def get_visitors():
    visitors_list = Visitor.query.all()
    return jsonify([{
        "visitor_id": visitor.visitor_id,
        "influencer_id": visitor.influencer_id,
        "referer": visitor.referer,
        "location": visitor.location,
        "link_id": visitor.link_id,
        "created_at": visitor.created_at.isoformat(),
        "headers": visitor.headers
    } for visitor in visitors_list])
# @api_blueprint.route('/api', methods=['GET'])
# def api():
#     data = get_data()
#     return jsonify(data)