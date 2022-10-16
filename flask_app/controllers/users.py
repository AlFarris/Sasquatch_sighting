from flask import get_flashed_messages, render_template, session, redirect, request,flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.sighting import Sighting
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route("/")
def index():
    return render_template("index.html", messages = get_flashed_messages())

@app.route("/sighting/new")
def new_sighting():
    if 'user_id' not in session:
        return redirect("/")
    data= {
            'id':session.get('user_id')
        }
    this_user = User.get_by_id(data)
    return render_template("new_sighting.html", user=this_user)

@app.route("/dashboard")
def dashboard():
    if 'user_id' not in session:
        return redirect("/")
    data= {
            'id':session.get('user_id')
        }
    this_user = User.get_by_id(data)
    return render_template("dashboard.html", user = this_user, all_sightings= Sighting.get_all(), all_users=User.get_all())

@app.route("/create",  methods=['POST'])
def create():
    if not Sighting.validate_sighting(request.form):
        return redirect("/sighting/new")
    data = {
            'location': request.form['location'],
            'description': request.form['description'],
            'date': request.form['date'],
            'number': request.form['number'],
            'user_id': session.get('user_id')
        }
    Sighting.create(data)
    return redirect("/dashboard")

@app.route("/sighting/delete/<int:id>")
def delete_sighting(id):
    Sighting.delete_sighting({"id": id})
    return redirect("/dashboard")

@app.route("/sighting/show/<int:id>")
def show_sighting(id):
    if 'user_id' not in session:
        return redirect("/")
    data={
        "id": session.get('user_id')
    }
    sighting= Sighting.get_all_by_id({"id": id})
    return render_template("show_sighting.html", user= User.get_by_id(data), sighting=sighting)

@app.route("/sighting/edit/<int:id>")
def edit_sighting(id):
    if 'user_id' not in session:
        return redirect("/")
    data={
        "id": id
    }
    ur_id = session.get('user_id')
    ur_data={
        "id": ur_id
    }
    user = User.get_by_id(ur_data)
    sighting= Sighting.get_all_by_id(data)
    return render_template("edit_sighting.html",sighting=sighting, user=user)


@app.route("/sighting/update", methods=['POST'])
def update_sighting():
    if not Sighting.validate_sighting(request.form):
        return redirect("/sighting/edit/%s" %request.form['id'])
    data = {
        'id': request.form['id'],
        'location': request.form['location'],
        'description': request.form['description'],
        'date': request.form['date'],
        'number': request.form['number'],
        'user_id': session.get('user_id')
    }
    Sighting.update_sighting(data)
    return redirect("/dashboard")

@app.route("/register", methods=['POST'])
def register():
    if not User.validate_user(request.form):
        return redirect('/')
    if request.form['password'] == request.form['confirm_pass']:
        data = {
            'first_name': request.form['first_name'],
            'last_name': request.form['last_name'],
            'email': request.form['email'],
            'password': bcrypt.generate_password_hash(request.form['password']) 
        }
        user_id = User.create(data)
        session['user_id'] = user_id
        return redirect("/dashboard")
    flash("Passwords do not match.")
    return redirect("/")

@app.route("/login", methods=['POST'])
def login():
    data={
        'email': request.form['email']
    }
    this_user = User.get_by_email(data)
    if this_user and bcrypt.check_password_hash(this_user.password, request.form['password']):
        session['user_id'] = this_user.id
        return redirect("/dashboard")
    flash("Invalid login attempt")
    return redirect("/")
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")