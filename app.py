from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

with app.app_context():
    db.create_all()

@app.route('/edit-profile', methods=['GET', 'POST'])
def edit_profile():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        if user:
            user.username = username
            user.password = password
        else:
            user = User(username=username, email=email, password=password)
            db.session.add(user)

        db.session.commit()
        return redirect(url_for('success'))

    return render_template('base.html')

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Обработка данных
        print(f"Updated Profile - Name: {username}, Email: {email}, Password: {password}")

        return redirect(url_for('success'))

    return render_template('base.html')

# Роут для подтверждения
@app.route('/success')
def success():
    return "Profile updated successfully!"

if __name__ == '__main__':
    app.run(debug=True, port=5000)
