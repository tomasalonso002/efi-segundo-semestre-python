from models import db
from flask import Flask

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']=(
    'mysql+pymysql://root:@localhost/efi-segundo-semestre'
)
app.config['SQLALCHEMY_TRACK_NOTIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()
    print("Base de datos creada correctamente")
    