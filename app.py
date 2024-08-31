from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///budget.db"
db = SQLAlchemy(app)

class Budget(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)

@app.route("/")
def index():
    budgets = Budget.query.all()
    return render_template("index.html", budgets=budgets)

@app.route("/add", methods=["POST"])
def add_budget():
    name = request.form["name"]
    amount = float(request.form["amount"])
    budget = Budget(name=name, amount=amount)
    db.session.add(budget)
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/delete/<int:id>")
def delete_budget(id):
    budget = Budget.query.get(id)
    db.session.delete(budget)
    db.session.commit()
    return redirect(url_for("index"))



with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)