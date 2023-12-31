from flask import Flask, request, jsonify, render_template

from models import db, connect_db, Cupcake

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "oh-so-secret"
app.app_context().push()
connect_db(app)

@app.route('/')
def show_homepage():
    """Show homepage"""
    all_cupcakes = Cupcake.query.all()
    return render_template("home.html", cupcakes = all_cupcakes)
    
    
@app.route('/api/cupcakes')
def list_cupcakes():
    """Return all cupcakes"""
    all_cupcakes = [cupcake.serialize() for cupcake in Cupcake.query.all()]
    return jsonify(cupcakes = all_cupcakes)

@app.route('/api/cupcakes/<int:id>')
def get_cupcake(id):
    """Return single cupcake based on id"""
    cupcake = Cupcake.query.get_or_404(id)

    return jsonify(cupcake = cupcake.serialize())

@app.route('/api/cupcakes', methods = ["POST"])
def create_cupcake():
    """Add new cupcake and return json instance of cupcake"""
    flavor = request.json.get("flavor")
    size = request.json.get("size")
    rating = request.json.get("rating")
    image = request.json.get("image")
    
    new_cupcake = Cupcake(flavor=flavor, size = size, rating = rating, image = image)
    
    db.session.add(new_cupcake)
    db.session.commit()
    response_json=jsonify(cupcake=new_cupcake.serialize())
    return (response_json, 201)

@app.route('/api/cupcakes/<int:id>', methods=["PATCH"])
def update_cupcake(id):
    """Update existing cupcake instance and returns updated json"""
    cupcake = Cupcake.query.get_or_404(id)
    cupcake.flavor = request.json.get("flavor", cupcake.flavor)
    cupcake.size = request.json.get("size", cupcake.size)
    cupcake.rating = request.json.get("rating", cupcake.rating)
    cupcake.image = request.json.get("image", cupcake.image)
    db.session.commit()
    return jsonify(cupcake = cupcake.serialize())

@app.route('/api/cupcakes/<int:id>', methods=["DELETE"])
def delete_cupcake(id):
    """Delete prior existing cupcake and return a message confirming deletion"""
    cupcake = Cupcake.query.get_or_404(id)
    db.session.delete(cupcake)
    db.session.commit()
    return jsonify(message="deleted")