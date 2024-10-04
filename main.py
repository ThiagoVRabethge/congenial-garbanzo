import os

from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

cors = CORS(app, origins=["*"])

basedir = os.path.abspath(os.path.dirname(__file__))

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://example_vnum_user:9vZyhwOkEDLD2FP1fyVlSnoyVdKEr0Rh@dpg-crvfq8m8ii6s73e7tt00-a.oregon-postgres.render.com/example_vnum"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f"<User {self.name}>"

    def to_dict(self):
        return {"id": self.id, "name": self.name, "email": self.email}


@app.route("/", methods=["GET"])
def root():
    return jsonify({"hello": "world"})


@app.route("/users", methods=["POST"])
def create_user():
    try:
        data = request.json
        new_user = User(name=data["name"], email=data["email"])
        db.session.add(new_user)
        db.session.commit()
        return (
            jsonify(
                {"message": "User created successfully", "user": new_user.to_dict()}
            ),
            201,
        )
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400


@app.route("/users", methods=["GET"])
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])


@app.route("/users/<int:id>", methods=["GET"])
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify(user.to_dict())


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)
