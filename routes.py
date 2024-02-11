# route.py

from flask import Blueprint, jsonify, request
from model import Manager
from flask import request
from model import Manager, GroupInfo, Visitor ,Influencer, Link  # Importe os modelos adicionais aqui
from database import db
from sqlalchemy.exc import SQLAlchemyError  # Import SQLAlchemyError
from werkzeug.exceptions import BadRequest  # Import for catching bad requests
import hashlib

api_blueprint = Blueprint('api', __name__)

################### INFLUENCER ###################################
@api_blueprint.route('/influencers', methods=['GET'])
def get_influencers():
    influencers_list = Influencer.query.all()
    return jsonify([{"influencer_id": influencer.influencer_id, "name": influencer.name} for influencer in influencers_list])

@api_blueprint.route('/influencers', methods=['POST'])
def create_influencer():
    data = request.get_json()
    try:
        if not data or 'name' not in data or 'url' not in data:  # Basic validation to check if name exists
            raise BadRequest('Missing fields in request data')
        new_influencer = Influencer(name=data['name'],url=data['url'])
        db.session.add(new_influencer)
        db.session.commit()
        return jsonify({"message": "Influencer created successfully", "influencer_id": new_influencer.influencer_id}), 201
    except SQLAlchemyError as e:  # Catch any SQLAlchemy errors
        db.session.rollback()  # Rollback the session to a clean state
        return jsonify({"DB error": str(e)}), 500
    except BadRequest as e:
        # Log the bad request error here
        return jsonify({"error": str(e)}), 400
    except Exception as e:  # Catching other errors
        # Log this error
        return jsonify({"error": "An unexpected error occurred."}), 500


#@api_blueprint.route('/influencers', methods=['POST'])
#def create_influencer():
#    data = request.get_json()
#    new_influencer = Influencer(name=data['name'], follower_count=data['follower_count'])  # supondo que o JSON recebido tenha 'name' e 'follower_count'
#    db.session.add(new_influencer)
#    db.session.commit()
#   return jsonify({"message": "Influencer created successfully"}), 201
##################################################################

################### GROUP INFOS ##################################
@api_blueprint.route('/groupinfos', methods=['GET'])
def get_groups_infos():
    group_infos_list = GroupInfo.query.all()
    return jsonify([{"group_info_id": group_infos.group_info_id, "name": group_infos.name} for group_infos in group_infos_list])



##################################################################

################### MANAGER ##################################

@api_blueprint.route('/managers', methods=['POST'])
def create_manager():
    data = request.json
    new_manager = Manager(user_name=data['user_name'], password=data['password'])
    db.session.add(new_manager)
    db.session.commit()
    return jsonify({"message": "Manager created successfully."}), 201

@api_blueprint.route('/managers', methods=['GET'])
def get_managers():
    managers = Manager.query.all()
    managers_data = [{"manager_id": manager.manager_id, "user_name": manager.user_name} for manager in managers]
    return jsonify(managers_data)

@api_blueprint.route('/managers/<int:manager_id>', methods=['GET'])
def get_manager(manager_id):
    manager = Manager.query.get_or_404(manager_id)
    manager_data = {"manager_id": manager.manager_id, "user_name": manager.user_name}
    return jsonify(manager_data)

@api_blueprint.route('/managers/<int:manager_id>', methods=['PUT'])
def update_manager(manager_id):
    manager = Manager.query.get_or_404(manager_id)
    data = request.json
    manager.user_name = data['user_name']
    manager.password = data['password']
    db.session.commit()
    return jsonify({"message": "Manager updated successfully."})

@api_blueprint.route('/managers/<int:manager_id>', methods=['DELETE'])
def delete_manager(manager_id):
    manager = Manager.query.get_or_404(manager_id)
    db.session.delete(manager)
    db.session.commit()
    return jsonify({"message": "Manager deleted successfully."})

##################################################################

################### VISITORS #####################################
@api_blueprint.route('/visitors', methods=['GET'])
def get_visitors():
    Visitor_list = Visitor.query.all()
    return jsonify([{"group_info_id": visitors.visitor_id, "name": visitors.name} for visitors in Visitor_list])

##################################################################

#@api_blueprint.route('/visitors', methods=['GET'])
#def get_visitors():
#    visitors_list = Visitor.query.all()
#    return jsonify([{
#        "visitor_id": visitor.visitor_id,
#        "influencer_id": visitor.influencer_id,
#        "referer": visitor.referer,
#        "location": visitor.location,
#        "link_id": visitor.link_id,
#        "created_at": visitor.created_at.isoformat(),
#        "headers": visitor.headers
#    } for visitor in visitors_list])
# @api_blueprint.route('/api', methods=['GET'])
# def api():
#     data = get_data()
#     return jsonify(data)



##############################################################
## LINKS
# Create a new link
@api_blueprint.route('/links', methods=['POST'])
def create_link():
    data = request.json
    if 'url_reduced' in data and data['url_reduced']:  # If url_reduced is provided
        existing_link = Link.query.filter_by(url_reduced=data['url_reduced']).first()
        if existing_link:
            return jsonify({"error": "Provided url_reduced is already in use."}), 400
        else:
            new_link = Link(link_name=data['link_name'], url=data['url'], url_reduced=data['url_reduced'],
                            isvisible=data.get('isvisible', True), influencer_id=data['influencer_id'])
    else:  # If url_reduced is not provided, generate a reduced link using hash
        hash_value = hashlib.sha256(data['url'].encode() + data['link_name'].encode()+ str(data['influencer_id']).encode()).hexdigest()[:8]  # Using hash for simplicity
        new_link = Link(link_name=data['link_name'], url=data['url'], url_reduced=hash_value,
                        isvisible=data.get('isvisible', True), influencer_id=data['influencer_id'])
    
    db.session.add(new_link)
    db.session.commit()
    return jsonify({"message": "Link created successfully.", "url_reduced": new_link.url_reduced}), 201

# Retrieve all links
@api_blueprint.route('/links', methods=['GET'])
def get_links():
    links = Link.query.all()
    links_data = [{"link_id": link.link_id, "link_name": link.link_name, "url": link.url,
                   "url_reduced": link.url_reduced, "isvisible": link.isvisible,
                   "influencer_id": link.influencer_id, "created_at": link.created_at} for link in links]
    return jsonify(links_data)

# Retrieve a specific link
@api_blueprint.route('/links/<int:link_id>', methods=['GET'])
def get_link(link_id):
    link = Link.query.get_or_404(link_id)
    link_data = {"link_id": link.link_id, "link_name": link.link_name, "url": link.url,
                 "url_reduced": link.url_reduced, "isvisible": link.isvisible,
                 "influencer_id": link.influencer_id, "created_at": link.created_at}
    return jsonify(link_data)

# Update an existing link
@api_blueprint.route('/links/<int:link_id>', methods=['PUT'])
def update_link(link_id):
    link = Link.query.get_or_404(link_id)
    data = request.json
    link.link_name = data['link_name']
    link.url = data['url']
    link.url_reduced = data['url_reduced']
    link.isvisible = data['isvisible']
    link.influencer_id = data['influencer_id']
    db.session.commit()
    return jsonify({"message": "Link updated successfully."})

# Delete a link
@api_blueprint.route('/links/<int:link_id>', methods=['DELETE'])
def delete_link(link_id):
    link = Link.query.get_or_404(link_id)
    db.session.delete(link)
    db.session.commit()
    return jsonify({"message": "Link deleted successfully."})