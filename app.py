# Updated app.py with all features integrated
from flask import Flask, request, jsonify, render_template, Response
from scraper import scrape_amazon_products
import csv, io
from flask_cors import CORS
from fpdf import FPDF
import os

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/scrape', methods=['GET'])
def scrape():
    query = request.args.get('query')
    pages = int(request.args.get('pages', 1))
    if pages > 5:
        return render_template('index.html', error='Max 5 pages allowed')

    try:
        results = scrape_amazon_products(query, pages)
        return render_template('index.html', results=results)
    except Exception as e:
        return render_template('index.html', error=str(e))

@app.route('/download/csv', methods=['POST'])
def download_csv():
    products = request.json.get('products')
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=products[0].keys())
    writer.writeheader()
    writer.writerows(products)
    output.seek(0)
    return Response(output, mimetype='text/csv',
                    headers={'Content-Disposition': 'attachment; filename=products.csv'})

@app.route('/download/pdf', methods=['POST'])
def download_pdf():
    products = request.json.get('products')
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for i, p in enumerate(products, 1):
        pdf.multi_cell(0, 10, f"{i}. {p['title']}\nPrice: {p['price']}\nRating: {p['rating']}\nLink: {p['link']}\n")
    output = io.BytesIO()
    pdf.output(output)
    output.seek(0)
    return Response(output, mimetype='application/pdf',
                    headers={'Content-Disposition': 'attachment; filename=products.pdf'})
    
@app.route('/health')
def health():
    return "OK", 200

@app.errorhandler(500)
def internal_error(error):
    return render_template("index.html", error="Something went wrong. Please try again."), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
