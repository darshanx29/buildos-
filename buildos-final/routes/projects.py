from flask import Blueprint, jsonify, request
from config import supabase

projects_bp = Blueprint('projects', __name__)


@projects_bp.route('/', methods=['GET'])
def get_projects():
    res = supabase.table('projects').select('*').order('created_at', desc=True).execute()
    return jsonify(res.data)


@projects_bp.route('/<project_id>', methods=['GET'])
def get_project(project_id):
    res = supabase.table('projects').select('*').eq('id', project_id).single().execute()
    return jsonify(res.data)


@projects_bp.route('/', methods=['POST'])
def create_project():
    body = request.get_json()
    res = supabase.table('projects').insert({
        'name': body['name'],
        'site_location': body.get('site_location', ''),
        'budget': body['budget']
    }).execute()
    return jsonify(res.data[0]), 201


@projects_bp.route('/<project_id>', methods=['PUT'])
def update_project(project_id):
    body = request.get_json()
    res = supabase.table('projects').update({
        'name': body.get('name'),
        'site_location': body.get('site_location'),
        'budget': body.get('budget')
    }).eq('id', project_id).execute()
    return jsonify(res.data[0])


@projects_bp.route('/<project_id>', methods=['DELETE'])
def delete_project(project_id):
    supabase.table('projects').delete().eq('id', project_id).execute()
    return jsonify({'message': 'Project deleted'}), 200
