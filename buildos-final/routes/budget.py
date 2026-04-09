from flask import Blueprint, jsonify
from config import supabase

budget_bp = Blueprint('budget', __name__)


@budget_bp.route('/<project_id>', methods=['GET'])
def get_budget_summary(project_id):
    # get project budget
    project = supabase.table('projects').select('budget') \
        .eq('id', project_id).single().execute()
    budget = float(project.data['budget'])

    # get all invoices for this project
    invoices = supabase.table('invoices').select('id') \
        .eq('project_id', project_id).execute()
    invoice_ids = [inv['id'] for inv in invoices.data]

    spent = 0.0
    if invoice_ids:
        items = supabase.table('invoice_items') \
            .select('total').in_('invoice_id', invoice_ids).execute()
        spent = sum(float(item['total']) for item in items.data if item['total'])

    remaining = budget - spent
    percent = round((spent / budget) * 100, 1) if budget > 0 else 0

    return jsonify({
        'budget': budget,
        'spent': spent,
        'remaining': remaining,
        'percent_used': percent,
        'is_overrun': spent > budget
    })
