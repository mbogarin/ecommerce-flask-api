# E-Commerce Flask API

# ** IMPORTS:
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from datetime import datetime, timezone
from sqlalchemy.orm import DeclarativeBase, relationship, Mapped, mapped_column
from sqlalchemy import DateTime, ForeignKey, Table, Column, String, Integer, select, Float
from marshmallow import ValidationError
from typing import List, Optional


# ** SETUP & CONFIGURATION:
# 1. Initialize Flask app:
app = Flask(__name__)

# 2. MySQL database configuration:
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:Murphy324!!@localhost/ecommerce_api'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 3. Create Base Model:
class Base(DeclarativeBase):
    pass

# 4. Initialize Extension Classes: SQLAlchemy + Marshmallow
db = SQLAlchemy(model_class=Base)
db.init_app(app)
ma = Marshmallow(app)


# [DATABASE MODELS]:
# 1. Order_Product Association Table:
order_product = Table(
    "order_product",
    Base.metadata,
    Column("order_id", ForeignKey("orders.id"), primary_key=True),
    Column("product_id", ForeignKey("products.id"), primary_key=True)
)

# 2. User Table:
class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    address: Mapped[str] = mapped_column(String(200))
    email: Mapped[str] = mapped_column(String(200), unique=True, nullable=False)
 
 
    # < One-to-Many relationship: A user can place multiple orders.
    orders: Mapped[List["Order"]] = relationship(back_populates="user", cascade="all, delete-orphan")


# 3. Order Table:
class Order(Base):
    __tablename__ = "orders"
    id: Mapped[int] = mapped_column(primary_key=True)
    order_date: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    
    
    # < a) Many-to-Many relationship: An order can contain multiple products.
    products: Mapped[List["Product"]] = relationship(secondary=order_product, back_populates="orders")
    
    # < b) One-to-Many relationship: An order can only have one user. 
    user: Mapped["User"] = relationship(back_populates="orders")


# 4. Product Table:
class Product(Base):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(primary_key=True)
    product_name: Mapped[str] = mapped_column(String(150))
    price: Mapped[float] = mapped_column(Float)
    
    
    # < Many-to-Many relationship: A product can belong to multiple orders.
    orders: Mapped[List["Order"]] = relationship(secondary=order_product, back_populates="products")



# [MARSHMALLOW SCHEMAS]:
# 1. UserSchema:
class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        
# 2. OrderSchema:
class OrderSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Order
        include_fk = True

# 3. ProductSchema:
class ProductSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Product
        
# 4. Initialize Schemas:
user_schema = UserSchema()
users_schema = UserSchema(many=True) 

order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)

product_schema = ProductSchema()
products_schema = ProductSchema(many=True)



# [CRUD ENDPOINTS]:

# 1. USER endpoints:
# ===========================================================================
# > U-1) Retrieve all users: GET
@app.route("/users", methods=["GET"])

def get_users():
    query = select(User)
    users = db.session.execute(query).scalars().all()
    return users_schema.jsonify(users), 200
    
# > U-2) Retrieve a user by ID: GET
@app.route("/users/<int:id>", methods=["GET"])

def get_user(id):
    user = db.session.get(User, id)
    
    if not user: 
        return jsonify({"Message": "User not found"}), 404
              
    return user_schema.jsonify(user), 200

# > U-3) Create a new user: POST
@app.route("/users", methods=["POST"])

def create_user():
    try:
        user_data = user_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    new_user = User(name = user_data["name"], address = user_data["address"], email = user_data["email"])
    db.session.add(new_user)
    db.session.commit()
    return user_schema.jsonify(new_user), 201

# > U-4) Update a user by ID: PUT
@app.route("/users/<int:id>", methods=["PUT"])

def update_user(id):
    user = db.session.get(User, id)
    
    if not user:
        return jsonify({"Message": "User not found"}), 404
    
    try:
        user_data = user_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    user.name = user_data["name"]
    user.address = user_data["address"]
    user.email = user_data["email"]
    
    db.session.commit()
    return user_schema.jsonify(user), 200

# > U-5) Delete a user by ID: DELETE
@app.route("/users/<int:id>", methods=["DELETE"])

def delete_user(id):
    user = db.session.get(User, id)
    
    if not user:
        return jsonify({"Message": "User not found"}), 404
    
    db.session.delete(user)
    db.session.commit()
    return jsonify({"Message": f"The user {user.name} ({id}) was successfully deleted!"}), 200


# 2. PRODUCT endpoints:
# ===========================================================================
# > P-1) Retrieve all products: GET
@app.route("/products", methods=["GET"])

def get_products():
    query = select(Product)
    products = db.session.execute(query).scalars().all()
    return products_schema.jsonify(products), 200

# > P-2) Retrieve a product by ID: GET
@app.route("/products/<int:id>", methods=["GET"])

def get_product(id):
    product = db.session.get(Product, id)
    
    if not product:
        return jsonify({"Message": "Product not found"}), 404
    
    return product_schema.jsonify(product), 200

# > P-3) Create a new product: POST
@app.route("/products", methods=["POST"])

def create_product():
    try:
        product_data = product_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    new_product = Product(product_name = product_data["product_name"], price = product_data["price"])
    db.session.add(new_product)
    db.session.commit()
    return product_schema.jsonify(new_product), 201

# > P-4) Update a product by ID: PUT
@app.route("/products/<int:id>", methods=["PUT"])

def update_product(id):
    product = db.session.get(Product, id)
    
    if not product:
        return jsonify({"Message": "Product not found"}), 404
    
    try:
        product_data = product_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    product.product_name = product_data["product_name"]
    product.price = product_data["price"]
    
    db.session.commit()
    return product_schema.jsonify(product), 200

# > P-5) Delete a product by ID: DELETE
@app.route("/products/<int:id>", methods=["DELETE"])

def delete_product(id):
    product = db.session.get(Product, id)
    
    if not product:
        return jsonify({"Message": "Product not found"}), 404
    
    db.session.delete(product)
    db.session.commit()
    return jsonify({"Message": f"{product.product_name} product was successfully deleted!"}), 200


# 3. ORDER endpoints:
# ===========================================================================
# > O-1) Create a new order: POST
@app.route("/orders", methods=["POST"])

def create_order():
    try:
        order_data = order_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    user = db.session.get(User, order_data["user_id"])
    if not user:
        return jsonify({"Message": "User not found"}), 404
    
    new_order = Order(user_id=order_data["user_id"])
    
    db.session.add(new_order)
    db.session.commit()
    return order_schema.jsonify(new_order), 201


# > 0-2) Add a product to an order: PUT
@app.route("/orders/<int:order_id>/add_product/<int:product_id>", methods=["PUT"])

def add_product(order_id, product_id):
    order = db.session.get(Order, order_id)
    if not order: 
        return jsonify({"Message": "Order not found"}), 404
    
    product = db.session.get(Product, product_id)
    if not product: 
        return jsonify({"Message": "Product not found"}), 404
    
    if product in order.products:
        return jsonify({"Message": f"Product ({product.id}) already exists in order #{order.id}"}), 400
    
    order.products.append(product)
    db.session.commit()

    return jsonify({"Message": f"The product {product.product_name} was successfully added to order #{order.id}!"}), 200


# > 0-3) Remove a product from an order: DELETE
@app.route("/orders/<int:order_id>/remove_product/<int:product_id>", methods=["DELETE"])

def remove_product(order_id, product_id):
    order = db.session.get(Order, order_id)
    if not order: 
        return jsonify({"Message": "Order not found"}), 404
    
    product = db.session.get(Product, product_id)
    if not product:
        return jsonify({"Message": "Product not found"}), 404
    
    if product not in order.products:
        return jsonify({"Message": "Product not found"}), 404
    
    order.products.remove(product)
    db.session.commit()
    
    return jsonify({"Message": f"{product.product_name} product was removed from order #{order.id}"}), 200
   
# > 0-4) Get all orders for a user: GET
@app.route("/orders/user/<int:user_id>", methods=["GET"])

def my_orders(user_id):
    user = db.session.get(User, user_id)
    
    if not user:
        return jsonify({"Message": "User not found"}), 404
        
    return orders_schema.jsonify(user.orders), 200
    
# > 0-5) Get all products for an order: GET
@app.route("/orders/<int:order_id>/products", methods=["GET"])

def my_products(order_id):
    order = db.session.get(Order, order_id)
    
    if not order:
        return jsonify({"Message": "Order not found"}), 404
    
    return products_schema.jsonify(order.products), 200


# + Bonus: Get order summary
@app.route("/orders/<int:order_id>/summary", methods=["GET"])

def order_summary(order_id):
    order = db.session.get(Order, order_id)
    
    if not order:
        return jsonify({"Message": "Order not found"}), 404
    
    total_items = len(order.products)
    
    total_price = sum(product.price for product in order.products)
    
    return jsonify({
        "order_id": order.id,
        "order_date": order.order_date,
        "user_id": order.user_id,
        "user_name": order.user.name,
        "total_items": total_items,
        "total_price": total_price,
    }), 200

        

# ** CREATE TABLES IN DATABASE:
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    
    app.run(debug=True)




