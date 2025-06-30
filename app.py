from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Konfigurasi koneksi database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost:3306/komodo'# Ganti sesuai dengan username/password kamu
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Model Item
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Float, nullable=False)

# Buat tabel kalau belum ada
with app.app_context():
    db.create_all()


# GET semua item
@app.route('/api/items', methods=['GET'])
def get_items():
    items = Item.query.all()
    return jsonify([{
        'id': item.id,
        'name': item.name,
        'description': item.description,
        'price': item.price
    } for item in items]), 200

# GET satu item berdasarkan ID
@app.route('/api/items/<int:id>', methods=['GET'])
def get_item(id):
    item = Item.query.get(id)
    if item:
        return jsonify({
            'id': item.id,
            'name': item.name,
            'description': item.description,
            'price': item.price
        }), 200
    return jsonify({"error": "Item not found"}), 404

# POST tambah item
@app.route('/api/items', methods=['POST'])
def add_item():
    data = request.get_json()
    item = Item(
        name=data['name'],
        description=data['description'],
        price=float(data['price'])
    )
    db.session.add(item)
    db.session.commit()
    return jsonify({"message": "Item added successfully"}), 201

# PUT update item berdasarkan ID
@app.route('/api/items/<int:id>', methods=['PUT'])
def update_item(id):
    item = Item.query.get(id)
    if item:
        data = request.get_json()
        item.name = data['name']
        item.description = data['description']
        item.price = float(data['price'])
        db.session.commit()
        return jsonify({"message": "Item updated successfully"}), 200
    return jsonify({"error": "Item not found"}), 404

# DELETE item berdasarkan ID
@app.route('/api/items/<int:id>', methods=['DELETE'])
def delete_item(id):
    item = Item.query.get(id)
    if item:
        db.session.delete(item)
        db.session.commit()
        return jsonify({"message": "Item deleted successfully"}), 200
    return jsonify({"error": "Item not found"}), 404


@app.route('/')
def index():
    return render_template('index.html')  # pastikan kamu punya file templates/index.html


if __name__ == '_main_':
    app.run(debug=True)