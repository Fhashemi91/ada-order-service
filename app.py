from flask import Flask, request

from db import Base, engine
from resources.order import Order
from resources.status import Status

app = Flask(__name__)
app.config["DEBUG"] = True
Base.metadata.create_all(engine)


@app.route('/orders', methods=['POST'])
def create_order():
    req_data = request.get_json()
    return Order.create(req_data)


@app.route('/orders/<o_id>', methods=['GET'])
def get_order(o_id):
    return Order.get(o_id)


@app.route('/orders/<o_id>/status', methods=['PUT'])
def update_order_status(o_id):
    status = request.args.get('status')
    return Status.update(o_id, status)


@app.route('/orders/<o_id>', methods=['DELETE'])
def delete_order(o_id):
    return Order.delete(o_id)


app.run(host='0.0.0.0', port=8080)
