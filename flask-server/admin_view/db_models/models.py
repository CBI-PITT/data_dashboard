from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, current_user
from flask import url_for
from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView, expose, BaseView
from flask_admin.menu import MenuLink


db = SQLAlchemy()


class IndexInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    field = db.Column(db.String(100))
    description = db.Column(db.String(100))
    type = db.Column(db.String(100))
    es_index = db.Column(db.String(100))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    account = db.Column(db.String(100))
    password = db.Column(db.String(100))
    # is_verified = db.Column(db.Boolean, default=False)


class Parameters(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    index_name = db.Column(db.String(100), unique=True)
    resolution_micrometer = db.Column(db.Integer)
    density_atlas_col_name = db.Column(db.String(100))
    density_agg = db.Column(db.String(100))
    n_value_col_name = db.Column(db.String(100))

# class MyAdminIndexView(AdminIndexView):
#     @expose("/")
#     def home(self):
#         return self.render("admin/home_page.html")

#     def is_accessible(self):
#         # Ensure user is authenticated and is verified to access the model view
#         return current_user.is_authenticated

#     def inaccessible_callback(self, name, **kwargs):
#         # Redirect to login page if the user doesn't have access
#         return self.render("admin/login.html")


# class MyModelView(ModelView):
#     def is_accessible(self):
#         return current_user.is_authenticated

#     def inaccessible_callback(self, name, **kwargs):
#         return self.render("admin/login.html")

# class LogoutMenuLink(MenuLink):
#     def is_accessible(self):
#         return True  # Make the logout link always accessible

#     def get_url(self):
#         return url_for('logout')
# class FileUploadView(BaseView):
#     @expose("/", methods=("GET", "POST"))
#     def home(self):
#         return self.render("admin/upload_file.html")
