from flask_login import current_user
from flask import url_for
from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView, expose, BaseView
from flask_admin.menu import MenuLink
from config.es_config import es_server
from elasticsearch import Elasticsearch

es = Elasticsearch(es_server, request_timeout=180)



class MyAdminIndexView(AdminIndexView):
    @expose("/")
    def home(self):
        return self.render("admin/home_page.html")

    def is_accessible(self):
        # Ensure user is authenticated to access the model view
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        # Redirect to login page if the user doesn't have access
        return self.render("admin/security/login.html")


class MyModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return self.render("admin/security/login.html")


class LogoutMenuLink(MenuLink):
    def is_accessible(self):
        return True  # Make the logout link always accessible

    def get_url(self):
        return url_for('administrator.admin_logout')


class FileUploadView(BaseView):
    @expose("/", methods=("GET", "POST"))
    def home(self):
        indices = es.cat.indices(format="json")
        indexNamesArray = [entry["index"] for entry in indices]
        return self.render("admin/indexing/upload_file.html", indexNamesArray=indexNamesArray)
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return self.render("admin/security/login.html")
