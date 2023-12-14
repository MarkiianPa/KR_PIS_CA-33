from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Website(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    address = db.Column(db.String(100))
    version = db.Column(db.String(20))
    contacts = db.Column(db.String(100))

class Client(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(150))
    phone_number = db.Column(db.String(20))

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    products = db.relationship('Product', secondary='order_product', backref=db.backref('orders', lazy='dynamic'))
    status = db.Column(db.String(20))
    payment_type = db.Column(db.String(20))
    delivery_type = db.Column(db.String(20))
    date = db.Column(db.DateTime(timezone=True), default=func.now())

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    height = db.Column(db.Float)
    width = db.Column(db.Float)
    length = db.Column(db.Float)
    material = db.Column(db.String(50))
    description = db.Column(db.Text)
    price = db.Column(db.Float)
    color = db.Column(db.String(20))
    quantity = db.Column(db.Integer)
    path_to_img = db.Column(db.String(100))
    category = db.Column(db.String(50))  # Add the 'category' attribute
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id'))

    def to_dict(self):
            return {
                'id' : self.id,
                'height' : self.height,
                'width' : self.width,
                'length' : self.length,
                'material' : self.material,
                'description' : self.description,
                'price' : self.price,
                'color' : self.color,
                'quantity' : self.quantity,
                'path_to_img' : self.path_to_img,
                'category' : self.category,
                'supplier_id' : self.supplier_id
            }


class OrderProduct(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)

class PaymentAndDelivery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    payment_successful = db.Column(db.Boolean)
    delivery_address = db.Column(db.String(100))

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    salary = db.Column(db.Float)
    position = db.Column(db.String(50))
    status = db.Column(db.String(20))

class Manager(db.Model):
    id = db.Column(db.Integer, db.ForeignKey('employee.id'), primary_key=True)
    login = db.Column(db.String(20))
    password = db.Column(db.String(60))

class FurnitureList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    manager_id = db.Column(db.Integer, db.ForeignKey('manager.id'), nullable=False)
    products = db.relationship('Product', secondary='furniture_list_product', backref=db.backref('furniture_lists', lazy='dynamic'))
    date = db.Column(db.DateTime(timezone=True), default=func.now())

class FurnitureListProduct(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    furniture_list_id = db.Column(db.Integer, db.ForeignKey('furniture_list.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)

class Supplier(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    address = db.Column(db.String(100))
    contacts = db.Column(db.String(100))
