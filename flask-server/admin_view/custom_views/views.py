from flask_login import current_user
from flask import url_for,flash
from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView, expose, BaseView
from flask_admin.menu import MenuLink
from config.es_config import es_server
from elasticsearch import Elasticsearch

es = Elasticsearch(es_server, request_timeout=180)



class MyAdminIndexView(AdminIndexView):
    @expose("/")
    def home(self):
        return self.render("admin/home_page.html", current_user=current_user.name)

    def is_accessible(self):
        # Ensure user is authenticated to access the model view
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        # Redirect to login page if the user doesn't have access
        return self.render("admin/security/login.html")


class MyModelView(ModelView):
    # column_exclude_list = ['version']

    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return self.render("admin/security/login.html")
    # def on_model_change(self, form, model, is_created):
    #     existing_model = self.session.query(model.__class__).get(model.id)
    #     print("model here", model.version)
    #     if existing_model and existing_model.version != model.version:
    #         print('not allign!')
    #         # raise sqlalchemy_exc.ConcurrentModificationError("Record has been updated by another user. Please refresh and try again.")
    #         return False  # Prevent the update
        
    #     # Increment the version on each change
    #     model.version += 1
    #     self.session.commit()
    #     # return super(MyModelView, self).on_model_change(form, model, is_created)
    
   
    # def get_query(self):
    #     if current_user.is_authenticated and current_user.is_admin:
    #         # Admin user - retrieve all records
    #         return self.session.query(self.model)
    #     elif current_user.is_authenticated:
    #         # Regular user - retrieve records based on ownership
    #         if hasattr(self.model, 'owner_id'):  # Check if 'owner_id' attribute exists in the model
    #             return self.session.query(self.model).filter_by(owner_id=current_user.id)
    #         else:
    #             # Adjust this part based on your model's ownership attribute
    #             return self.session.query(self.model)
    #     else:
    #         # Unauthenticated user - return empty query
    #         return self.session.query(self.model).filter_by(id=-1)

    # def is_accessible(self):
    #     return current_user.is_authenticated

    # def inaccessible_callback(self, name, **kwargs):
    #     return self.render("admin/security/login.html")


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
