from flask import Flask, render_template
from flask_cors import CORS
from routes.projects import projects_bp
from routes.materials import materials_bp
from routes.transactions import transactions_bp
from routes.invoices import invoices_bp
from routes.budget import budget_bp
from routes.invoice_pdf import invoice_pdf_bp

app = Flask(__name__)
CORS(app)

# ── API routes ─────────────────────────────────────────────
app.register_blueprint(projects_bp,     url_prefix='/api/projects')
app.register_blueprint(materials_bp,    url_prefix='/api/materials')
app.register_blueprint(transactions_bp, url_prefix='/api/transactions')
app.register_blueprint(invoices_bp,     url_prefix='/api/invoices')
app.register_blueprint(invoice_pdf_bp,  url_prefix='/api/invoices')
app.register_blueprint(budget_bp,       url_prefix='/api/budget')

# ── Frontend routes ────────────────────────────────────────
@app.route('/')
def index():
    return render_template('dashboard.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/inventory')
def inventory():
    return render_template('inventory.html')

@app.route('/finance')
def finance():
    return render_template('finance.html')

@app.route('/invoices')
def invoices():
    return render_template('invoices.html')

@app.route('/projects')
def projects():
    return render_template('projects.html')

@app.route('/mobile')
def mobile():
    return render_template('mobile.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
