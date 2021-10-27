from flask import Flask,render_template,request,redirect,Response
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from datetime import date, datetime
from urllib.parse import urlparse

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50), nullable = False)

    pic = db.Column(db.Text, unique = True, nullable = False)
    mimetype = db.Column(db.Text, nullable = False)

    position = db.Column(db.String(50), nullable = False)
    date_of_birth = db.Column(db.Date, nullable = False)
    blood_group = db.Column(db.String(50), nullable = False)
    phone = db.Column(db.String(50), nullable = False)
    email = db.Column(db.String(80), nullable = False)

    def __str__(self):
        return f'<User {self.id}>'

@app.route("/")
def index():
    users = User.query.order_by(User.id).all()
    return render_template('index.html',users = users)


@app.route('/users',methods = ['GET','POST'])
def users():

    if request.method == 'POST':
        pic = request.files['pic']
        
        if not pic:
            return "No pic Uploaded", 400

        username = request.form['username']

        filename = secure_filename(pic.filename)
        mimetype = pic.mimetype    
        
        position = request.form['position']

        dob = request.form['DOB'].split("-")
        date_of_birth = date(int(dob[0]), int(dob[1]), int(dob[2]))

        blood_group = request.form['blood_group']
        phone = request.form['phone']
        email = request.form['email']
       
        new_user = User(
            name=username, 
            pic = pic.read(),
            date_of_birth = date_of_birth,
            mimetype = mimetype, 
            position = position,
            blood_group = blood_group,
            phone = phone,
            email=email
            )

        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect('/users')
        except :
            return f"There was a problem adding a user..."
    else:
        users = User.query.order_by(User.id).all()
        return render_template('users.html',users = users)


@app.route("/delete/<int:id>")
def delete(id):
    user = User.query.get_or_404(id)
    
    try:
        db.session.delete(user)
        db.session.commit()
        return redirect('/users')
    except:
        return "There was a problem deleting a user..."
    
@app.route("/update/<int:id>",methods=['GET','POST'])
def update(id):
    user = User.query.get_or_404(id)

    if request.method == "POST":
        
        user.name = request.form['username']
        pic = request.files['pic']

        if pic:
            user.filename = secure_filename(pic.filename)
            user.mimetype = pic.mimetype    
            user.pic = pic.read()
                
        user.position = request.form['position']

        dob = request.form['DOB'].split("-")
        user.date_of_birth = date(int(dob[0]), int(dob[1]), int(dob[2]))

        user.blood_group = request.form['blood_group']
        user.phone = request.form['phone']
        user.email = request.form['email']
              
        try:
            db.session.commit()
            return redirect("/users")
        except:
            return "There was a problem updating a user..."
    else:
        return render_template("update.html",user = user)

    

@app.route("/preview/<int:id>")
def preview(id):
    user = User.query.filter_by(id=id).first()
    o = urlparse(request.base_url)
    host = o.hostname
    return render_template('preview.html',user = user,host=host)


@app.route("/images/<int:id>")
def get_image(id):
    user = User.query.filter_by(id=id).first()

    if not user:
        return f"No user with id {id}",404

    return Response(user.pic, mimetype=user.mimetype)




if __name__ == "__main__":
    app.run(debug=True)
