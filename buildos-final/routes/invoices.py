from flask import Blueprint, jsonify, request
from config import supabase
import time

invoices_bp = Blueprint('invoices', __name__)


@invoices_bp.route('/<project_id>', methods=['GET'])
def get_invoices(project_id):
    res = supabase.table('invoices') \
        .select('*, invoice_items(*, materials(name))') \
        .eq('project_id', project_id) \
        .order('created_at', desc=True).execute()
    return jsonify(res.data)


@invoices_bp.route('/<invoice_id>', methods=['GET'])
def get_invoice(invoice_id):
    res = supabase.table('invoices') \
        .select('*, invoice_items(*, materials(name))') \
        .eq('id', invoice_id).single().execute()
    return jsonify(res.data)


@invoices_bp.route('/', methods=['POST'])
def create_invoice():
    body = request.get_json()
    project_id = body['project_id']
    items = body['items']  # [{material_id, description, quantity, unit_price}]

    total = sum(float(i['quantity']) * float(i['unit_price']) for i in items)
    invoice_number = f"INV-{str(int(time.time()))[-6:]}"

    # create invoice header
    inv = supabase.table('invoices').insert({
        'project_id': project_id,
        'invoice_number': invoice_number,
        'total_amount': total,
        'status': 'draft'
    }).execute()

    invoice_id = inv.data[0]['id']

    # insert line items
    line_items = [{
        'invoice_id': invoice_id,
        'material_id': i['material_id'],
        'description': i['description'],
        'quantity': float(i['quantity']),
        'unit_price': float(i['unit_price'])
    } for i in items]

    supabase.table('invoice_items').insert(line_items).execute()

    return jsonify({**inv.data[0], 'total': total}), 201


@invoices_bp.route('/<invoice_id>/status', methods=['PATCH'])
def update_status(invoice_id):
    body = request.get_json()
    status = body['status']  # 'draft' | 'sent' | 'paid'
    if status not in ('draft', 'sent', 'paid'):
        return jsonify({'error': 'Invalid status'}), 400
    supabase.table('invoices').update({'status': status}) \
        .eq('id', invoice_id).execute()
    return jsonify({'message': f'Status updated to {status}'})


@invoices_bp.route('/<invoice_id>', methods=['DELETE'])
def delete_invoice(invoice_id):
    supabase.table('invoices').delete().eq('id', invoice_id).execute()
    return jsonify({'message': 'Invoice deleted'}), 200
