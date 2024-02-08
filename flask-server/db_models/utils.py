from datetime import datetime
from db_models.models import *


def initial_setup():
    admins = user_credentials.query.filter_by(is_superuser=True).all()
    if len(admins) == 0:
        admin = user_credentials(id=1, name="admin", account="admin", password="password", is_superuser=True)  # TODO security
        db.session.add_all([admin])
    users = user_credentials.query.filter_by(is_superuser=False).all()
    groups = group_list.query.all()
    if not groups:
        group = group_list(id=1, name="general")
        if len(users) == 0:
            user = user_credentials(name="user", account="user", password="password",
                                    is_group_admin=False)  # TODO security
            user.groups.append(group)
            db.session.add_all([group, user])

    # create step types
    step_types = step_type.query.all()
    if not step_types:
        pre_process = step_type(id=1, name="pre-processing")
        register = step_type(id=2, name="registration")
        count_cells = step_type(id=3, name="cell counting")
        segment = step_type(id=4, name="segmentation")
    # create steps
        steps = step.query.all()
        if not steps:
            extract_tiffs = step(
                id=1, name="extract tiff series", container="ims_extract_tiff_v0.1.0", input="str", output="str",
                parameters="-v 1 1 1", type_id=1
            )
            brainreg = step(
                id=2, name="brainreg", container="brainreg_v0.1.0", input="str", output="str",
                parameters="-v 1 1 1", type_id=2
            )
        # create pipeline
        pipelines = pipeline_info.query.all()
        if not pipelines:
            mesospim = pipeline_info(id=1, name="mesospim")
            mesospim.steps.append(extract_tiffs)
            mesospim.steps.append(brainreg)
        # create index
        indices = index_info.query.all()
        if not indices:
            cebra = index_info(id=1, name="CEBRA", group_id=1, created=datetime.now(), modified=datetime.now(),
                               description="c-FOS data", pipeline_id=1
                               )
        # create job
        jobs = job_info.query.all()
        if not jobs:
            job = job_info(
                id=1, name="register_cebra", user_id=1, created=datetime.now(), status="scheduled",
                group_id=1, index_id=1, dataset="/path/to/file.ims"
            )

        db.session.add_all([pre_process, register, count_cells, segment, extract_tiffs, brainreg, mesospim, cebra, job])
    db.session.commit()
