from flask import Blueprint, jsonify, request
from config import supabase

transactions_bp = Blueprint('transactions', __name__)


@transactions_bp.route('/<project_id>', methods=['GET'])
def get_transactions(project_id):
    res = supabase.table('transactions') \
        .select('*, materials(name, unit)') \
        .eq('project_id', project_id) \
        .order('created_at', desc=True).limit(50).execute()
    return jsonify(res.data)


@transactions_bp.route('/', methods=['POST'])
def log_transaction():
    body = request.get_json()
    material_id = body['material_id']
    tx_type = body['type']       # 'in' or 'out'
    qty = float(body['quantity'])

    # 1. get current quantity
    mat = supabase.table('materials').select('quantity') \
        .eq('id', material_id).single().execute()
    current_qty = float(mat.data['quantity'])

    # 2. prevent negative stock
    if tx_type == 'out' and current_qty < qty:
        return jsonify({'error': 'Not enough stock available'}), 400

    # 3. update material quantity
    new_qty = current_qty + qty if tx_type == 'in' else current_qty - qty
    supabase.table('materials').update({'quantity': new_qty}) \
        .eq('id', material_id).execute()

    # 4. log the transaction record
    res = supabase.table('transactions').insert({
        'material_id': material_id,
        'project_id': body['project_id'],
        'type': tx_type,
        'quantity': qty,
        'note': body.get('note', ''),
        'logged_by': body.get('logged_by', 'engineer')
    }).execute()

    return jsonify(res.data[0]), 201
