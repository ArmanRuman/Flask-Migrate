from flask import Flask 
from flask_sqlalchemy import SQLAlchemy 
from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin, login_required, current_user, roles_accepted
from flask_mail import Mail
from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView

app = Flask(__name__)
app.config['SECRET_KEY'] = 'asecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///security.db'
app.config['SECURITY_REGISTERABLE'] = True
app.config['SECURITY_PASSWORD_SALT'] = 'mysalt'
app.config['SECURITY_SEND_REGISTER_EMAIL'] = True
app.config['SECURITY_RECOVERABLE'] = True
app.config['SECURITY_CONFIRMABLE'] = True
app.config['SECURITY_CHANGEABLE'] = True
app.config['SECURITY_EMAIL_SENDER'] = 'armanruman.eee.cu@gmail.com'
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'armanruman.eee.cu@gmail.com'
app.config['MAIL_PASSWORD'] = 'gszkstjyxdgmisjp'
app.config['MAIL_USE_TLS'] = False 
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_DEFAULT_SENDER']=('Arman','armanruman.eee.cu@gmail.com')

db = SQLAlchemy(app)
mail = Mail(app)


# Define models
roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))
class UserView(ModelView):

    def is_accessible(self):
        return current_user.has_role('Admin')
    def inaccessible_callback(self,name,**kwargs):
        return '<h1>You are not logged in! </h1>'

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)
admin = Admin(app, template_mode='bootstrap3')
admin.add_view(UserView(User, db.session))

def create_user():
    user=User.query.filter(User.email == 'alma.yitzhak@intrees.org').first()
    user.roles.append(Role(name='Admin'))
    db.session.add(user)
    db.session.commit()

@app.route('/')
def index():
    #admin_role = user_datastore.find_or_create_role('admin')
    #user_datastore.add_role_to_user(current_user, admin_role)
    #db.session.commit()
    return '<h1>home page</h1>'

@app.route('/protected')
@login_required
def protected():
    return '<h1>This is protected! Your email is: {}</h1>'.format(current_user.email)

@app.route('/roleprotected')
@roles_accepted('admin')
def roleprotected():
    return '<h1>This is for admins only.</h1>'
@app.route('/login')
def login():
    return 'You are login now!'

if __name__ == '__main__':
    app.run(debug=True)