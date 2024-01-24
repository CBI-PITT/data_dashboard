
import importlib
import config.db_config as db_config
from config.host import UPLOAD_FOLDER_PATH
from flask import Flask
from flask_cors import CORS
from elasticsearch import Elasticsearch
from flask_admin import Admin
import sys
from db_models.models import db, admin_credentials, field_info, parameters, index_info

# from models.admin.admin_models import db, admin_credentials, filed_info,parameters,index
# from models.models import db,admin_credentials, field_info,parameters,index
from flask_login import LoginManager, login_user, logout_user
from admin_view.custom_views.views import (
    MyAdminIndexView,
    MyModelView,
    FileUploadView,
    LogoutMenuLink,
)
from config.es_config import es_server

from bp_routes.indexInfo import indexInfo_bp
from bp_routes.dashboard import dahsboard_bp
from bp_routes.administrator import administrator_bp
from bp_routes.group_user import group_user_bp
from bp_routes.group_admin import group_admin_bp
CONFIG_SQL_CONNECTION = db_config.DATABASE
CONFIG_SCREATE_KEY = db_config.SCREATE_KEY
es = Elasticsearch(es_server, request_timeout=180)
app = Flask(__name__)
CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://" + CONFIG_SQL_CONNECTION
app.config["SECRET_KEY"] = CONFIG_SCREATE_KEY
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER_PATH
db.init_app(app)


login_manager = LoginManager(app)


@login_manager.user_loader
def load_user(user_id):
    # load the user from the database
    return admin_credentials.query.get(int(user_id))


admin = Admin(
    app, name="Dashboard", template_mode="bootstrap4", index_view=MyAdminIndexView()
)


admin.add_link(LogoutMenuLink(name="Logout"))
admin.add_view(FileUploadView(name="UploadFile"))
admin.add_view(MyModelView(index_info, db.session, name="Index"))
admin.add_view(MyModelView(field_info, db.session, name="FieldInfo"))
admin.add_view(MyModelView(parameters, db.session, name="Parameters"))

app.register_blueprint(indexInfo_bp)
app.register_blueprint(dahsboard_bp)
app.register_blueprint(administrator_bp)
app.register_blueprint(group_user_bp)
app.register_blueprint(group_admin_bp)

@app.route("/")
def index_info():
    return app.send_static_file("index.html")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
