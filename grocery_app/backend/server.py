from flask import Flask, json, request, jsonify, render_template
import products_dao
import orders_dao
import uom_dao
from sql_connection import get_sql_connection
from flask_cors import CORS

app = Flask(__name__, static_url_path='/static', template_folder='templates')
CORS(app)

connection = get_sql_connection()


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/manage-product.html')
def manage_product():
    return render_template('manage-product.html')

@app.route('/order.html')
def order():
    return render_template('order.html')

@app.route('/getAllOrders', methods=['GET'])
def get_all_orders():
    response = orders_dao.get_all_orders(connection)
    response = jsonify(response)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/insertOrder', methods=['POST'])
def insert_order():
    request_payload = request.get_json()

    if not request_payload:
        return jsonify({'error': 'No JSON data received'}), 400

    customer_name = request_payload.get('customer_name')
    grand_total = request_payload.get('grand_total')
    order_details = request_payload.get('order_details')

    # Validate and process request_payload data as needed
    # Example validation:
    if not customer_name or not grand_total or not order_details:
        return jsonify({'error': 'Missing required data fields'}), 400

    # Insert into database using your DAO function
    order_id = orders_dao.insert_order(connection, request_payload)

    return jsonify({'order_id': order_id}), 200

@app.route('/getProducts', methods=['GET'])
def get_products():
    
    products = products_dao.get_all_products(connection)
    response = jsonify(products)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/insertProduct', methods=['POST'])
def insert_product():
    request_payload = json.loads(request.form['data'])
    product_id = products_dao.insert_new_product(connection, request_payload)
    response = jsonify({
        'product_id': product_id
    })
    response.headers.add('Access-Control-Allow-Origin', "*")
    return response

@app.route('/getUOM', methods=['GET'])
def get_uom():
    response = uom_dao.get_uoms(connection)
    response = jsonify(response)
    response.headers.add('Access-Control-Allow-Origin', "*")
    return response

@app.route('/deleteProduct', methods=['POST'])
def delete_product():
    return_id = products_dao.delete_product(connection, request.form['product_id'])
    response = jsonify({
        'product_id': return_id
    })
    response.headers.add('Access-Control-Allow-Origin', "*")
    return response

if __name__ == '__main__':
    print("Starting Python Flask Server For Grocery Store Management System")
    app.run(port=5000)