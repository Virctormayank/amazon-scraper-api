from flask import Flask, request, jsonify, render_template, Response
from scraper import scrape_amazon_products
import csv
import io

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/scrape', methods=['GET'])
def scrape():
    query = request.args.get('query', default='laptop', type=str)
    pages = request.args.get('pages', default=1, type=int)
    format_ = request.args.get('format', default='', type=str).lower()

    data = scrape_amazon_products(query, pages)

    if format_ == 'csv':
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=["Name", "Price (₹)", "Rating"])
        writer.writeheader()
        writer.writerows(data)
        return Response(output.getvalue(), mimetype='text/csv',
                        headers={"Content-Disposition": f"attachment;filename={query}_products.csv"})

    # If accessed via browser form, show table
    return render_template("index.html", results=data)

if __name__ == "__main__":
    app.run(debug=True, port=8000)
