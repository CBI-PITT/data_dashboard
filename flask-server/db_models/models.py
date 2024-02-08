from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin


db = SQLAlchemy()


class field_info(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    field = db.Column(db.String(100))
    description = db.Column(db.String(100))
    type = db.Column(db.String(100))
    es_index = db.Column(db.String(100))


# class admin_credentials(db.Model, UserMixin):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100))
#     account = db.Column(db.String(100), unique=True)
#     password = db.Column(db.String(100))
#     # is_admin = db.Column(db.Boolean, default=False)


class group_list(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)

    def __str__(self):
        return self.name


class step_type(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

    def __str__(self):
        return self.name


class parameters(db.Model):
    """
    Parameters for calculating density and N value
    """
    id = db.Column(db.Integer, primary_key=True)
    es_index = db.Column(db.String(100), unique=True)  # should be related to actual index model
    resolution_micrometer = db.Column(db.Integer)  # atlas resolution
    density_atlas_col_name = db.Column(db.String(100))  # change to dropdown - what existing column in the index is used to calculate density
    density_agg = db.Column(db.String(100))
    n_value_col_name = db.Column(db.String(100))  # change to dropdown - what existing column in the index is used to calculate N value
    # version = db.Column(db.Integer, default=0)


class user_credentials(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))
    # group_id = db.Column(db.Integer, db.ForeignKey('group_list.id'))  # TODO: M2M
    groups = db.relationship('group_list', secondary='user_group_association', backref="users")
    is_active = db.Column(db.Boolean, default=True)
    is_authenticated = db.Column(db.Boolean, default=False)
    is_superuser = db.Column(db.Boolean, default=False)
    is_group_admin = db.Column(db.Boolean, default=False)

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def __str__(self):
        return self.account


class step(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    container = db.Column(db.String(100))
    input = db.Column(db.String(100))
    output = db.Column(db.String(100))
    parameters = db.Column(db.String(100))
    type_id = db.Column(db.Integer, db.ForeignKey('step_type.id'))
    type = db.relationship("step_type", backref=db.backref("steps", lazy='dynamic'))

    def __str__(self):
        return self.name


user_group_association = db.Table(
    "user_group_association",
    db.Column("user_id", db.Integer, db.ForeignKey("user_credentials.id")),
    db.Column("group_id", db.Integer, db.ForeignKey("group_list.id")),
)

# version = db.Column(db.Integer, default=0)
pipeline_group_association = db.Table(
    "pipeline_group_association",
    db.Column("pipeline_id", db.Integer, db.ForeignKey("pipeline_info.id")),
    db.Column("group_id", db.Integer, db.ForeignKey("group_list.id")),
)

pipeline_step_association = db.Table(
    "pipeline_step_association",
    db.Column("pipeline_id", db.Integer, db.ForeignKey("pipeline_info.id")),
    db.Column("step_id", db.Integer, db.ForeignKey("step.id")),
)


class pipeline_info(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    steps = db.relationship(
        "step", secondary='pipeline_step_association', backref="pipelines"
    )
    groups = db.relationship(
        "group_list", secondary='pipeline_group_association', backref="groups"
    )

    def __str__(self):
        return self.name


class index_info(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    group_id = db.Column(db.Integer, db.ForeignKey('group_list.id'))
    group = db.relationship('group_list', backref=db.backref("indices", lazy='dynamic'))
    created = db.Column(db.Date)
    modified = db.Column(db.Date)
    description = db.Column(db.String(100))
    pipeline_id = db.Column(db.Integer, db.ForeignKey('pipeline_info.id'))
    pipeline = db.relationship("pipeline_info", backref=db.backref("pipeline_jobs", lazy='dynamic'))

    def __str__(self):
        return self.name


class job_info(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    dataset = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('user_credentials.id'))
    user = db.relationship('user_credentials', backref=db.backref("user_jobs", lazy='dynamic'))
    created = db.Column(db.Date)
    status = db.Column(db.String(100))
    group_id = db.Column(db.Integer, db.ForeignKey('group_list.id'))
    group = db.relationship('group_list', backref=db.backref("group_jobs", lazy='dynamic'))
    index_id = db.Column(db.Integer, db.ForeignKey('index_info.id'))
    index = db.relationship('index_info', backref=db.backref("index_jobs", lazy='dynamic'))

    def __str__(self):
        return self.name


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
