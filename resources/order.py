from datetime import datetime

from flask import jsonify

from constant import STATUS_CREATED
from daos.order_dao import OrderDAO
from daos.status_dao import StatusDAO
from db import Session
from pubsub import submit_message


TIME_FORMAT = '%Y-%m-%d %H:%M:%S.%f'


class Order:
    @staticmethod
    def create(body):
        session = Session()

        if not body:
            return jsonify({"msg": "missing body!"}), 405

        customer_id = body.get('customer_id')
        product_id = body.get('product_id')
        delivery_time = body.get('delivery_time', datetime.now().strftime(TIME_FORMAT))

        if not (customer_id and product_id):
            return jsonify({"msg": "customer_id or product_id is missing"}), 406

        order = OrderDAO(customer_id, product_id, datetime.now(),
                               datetime.strptime(delivery_time, TIME_FORMAT),
                               StatusDAO(STATUS_CREATED, datetime.now()))
        session.add(order)
        session.commit()
        session.refresh(order)
        session.close()
        submit_message("order_created", id=str(order.id))
        return jsonify({'order_id': order.id}), 200

    @staticmethod
    def get(o_id):
        session = Session()
        # https://docs.sqlalchemy.org/en/14/orm/query.html
        # https://www.tutorialspoint.com/sqlalchemy/sqlalchemy_orm_using_query.htm
        order = session.query(OrderDAO).filter(OrderDAO.id == o_id).first()
        
        submit_message("order info requested", id=str(o_id))
        if order:
            status_obj = order.status
            text_out = {
                "customer_id:": order.customer_id,
                "product_id": order.product_id,
                "order_time": order.order_time.isoformat(),
                "delivery_time": order.delivery_time.isoformat(),
                "status": {
                    "status": status_obj.status,
                    "last_update": status_obj.last_update.isoformat(),
                }
            }
            session.close()
            return jsonify(text_out), 200
        else:
            session.close()
            return jsonify({'message': f'There is no order with id {o_id}'}), 404

    @staticmethod
    def delete(o_id):
        submit_message("order delete requested", id=str(o_id))

        session = Session()
        effected_rows = session.query(OrderDAO).filter(OrderDAO.id == o_id).delete()
        session.commit()
        session.close()
        if effected_rows == 0:
            return jsonify({'message': f'There is no order with id {o_id}'}), 404
        else:
            return jsonify({'message': 'The order was removed'}), 200
