from flask import Blueprint, jsonify, request
from config import supabase

materials_bp = Blueprint('materials', __name__)


@materials_bp.route('/<project_id>', methods=['GET'])
def get_materials(project_id):
    res = supabase.table('materials').select('*') \
        .eq('project_id', project_id).order('name').execute()
    return jsonify(res.data)


@materials_bp.route('/low-stock/<project_id>', methods=['GET'])
def get_low_stock(project_id):
    res = supabase.table('materials').select('*') \
        .eq('project_id', project_id).execute()
    low = [m for m in res.data if m['quantity'] <= m['reorder_threshold']]
    return jsonify(low)


@materials_bp.route('/', methods=['POST'])
def add_material():
    body = request.get_json()
    res = supabase.table('materials').insert({
        'project_id': body['project_id'],
        'name': body['name'],
        'unit': body.get('unit', 'bags'),
        'quantity': body.get('quantity', 0),
        'unit_price': body.get('unit_price', 0),
        'reorder_threshold': body.get('reorder_threshold', 10)
    }).execute()
    return jsonify(res.data[0]), 201


@materials_bp.route('/<material_id>', methods=['PUT'])
def update_material(material_id):
    body = request.get_json()
    res = supabase.table('materials').update({
        'name': body.get('name'),
        'unit': body.get('unit'),
        'unit_price': body.get('unit_price'),
        'reorder_threshold': body.get('reorder_threshold')
    }).eq('id', material_id).execute()
    return jsonify(res.data[0])


@materials_bp.route('/<material_id>', methods=['DELETE'])
def delete_material(material_id):
    supabase.table('materials').delete().eq('id', material_id).execute()
    return jsonify({'message': 'Material deleted'}), 200
