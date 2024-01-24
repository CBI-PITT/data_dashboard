from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin


db = SQLAlchemy()


# version = db.Column(db.Integer, default=0)
group_pipline_association = db.Table(
    "group_pipline_association",
    db.Column("group_id", db.Integer, db.ForeignKey("group_list.id")),
    db.Column("pipline_id", db.Integer, db.ForeignKey("pipline_info.id")),
)

pipline_step_association = db.Table(
    "pipline_step_association",
    db.Column("pipline_id", db.Integer, db.ForeignKey("pipline_info.id")),
    db.Column("step_id", db.Integer, db.ForeignKey("step.id")),
)


class field_info(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    field = db.Column(db.String(100))
    description = db.Column(db.String(100))
    type = db.Column(db.String(100))
    es_index = db.Column(db.String(100))


class admin_credentials(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    account = db.Column(db.String(100))
    password = db.Column(db.String(100))
    # is_admin = db.Column(db.Boolean, default=False)


class parameters(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    es_index = db.Column(db.String(100), unique=True)
    resolution_micrometer = db.Column(db.Integer)
    density_atlas_col_name = db.Column(db.String(100))
    density_agg = db.Column(db.String(100))
    n_value_col_name = db.Column(db.String(100))
    # version = db.Column(db.Integer, default=0)


class user_credentials(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))
    group = db.Column(db.String(100))
    is_group_admin = db.Column(db.Boolean)


class group_list(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group = db.Column(db.String(100), unique=True)
    piplines = db.relationship(
        "pipline_info",
        secondary=group_pipline_association,
        backref="group_id",
        lazy=True,
    )
    index_name = db.relationship("index_info", backref="group_id")
    job_name = db.relationship("job_info", backref="group_id")


class pipline_info(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pipline_name = db.Column(db.String(100))
    steps = db.relationship(
        "step", secondary=pipline_step_association, backref="pipeline_id", lazy=True
    )

    # any configuration


class step(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    step_name = db.Column(db.String(100), unique=True)
    container = db.Column(db.String(100))
    input = db.Column(db.String(100))
    output = db.Column(db.String(100))
    parameters = db.Column(db.String(100))
    type = db.Column(db.String(100))


class step_type(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    step_type_name = db.Column(db.String(100))


class index_info(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    index_name = db.Column(db.String(100), unique=True)
    group = db.Column(db.Integer, db.ForeignKey(group_list.id))
    created = db.Column(db.Date)
    modified = db.Column(db.Date)
    breif = db.Column(db.String(100))


class job_info(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_name = db.Column(db.String(100))
    pipline_name = db.Column(db.String(100))
    time = db.Column(db.Date)
    status = db.Column(db.String(100))
    group = db.Column(db.Integer, db.ForeignKey(group_list.id))


# class Index(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     es_index = db.Column(db.String(100), unique=True)
#     brief = db.Column(db.String(100))
#     owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # Foreign key reference to User's id

# class FieldInfo(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     field = db.Column(db.String(100))
#     description = db.Column(db.String(100))
#     type = db.Column(db.String(100))
#     es_index_id = db.Column(db.Integer, db.ForeignKey('index.id'))  # Foreign key reference to Index's es_index

# class User(db.Model,UserMixin):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100))
#     account = db.Column(db.String(100), unique=True)
#     password = db.Column(db.String(100))
#     is_admin = db.Column(db.Boolean, default=False)
#     # Define a relationship to connect Index and User models
#     indices = db.relationship('Index', backref='user', lazy=True)

# class Parameters(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     es_name_id = db.Column(db.Integer, db.ForeignKey('index.id'))  # Foreign key reference to Index's es_index
#     resolution_micrometer = db.Column(db.Integer)
#     density_atlas_col_name = db.Column(db.String(100))
#     density_agg = db.Column(db.String(100))
#     n_value_col_name = db.Column(db.String(100))

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
