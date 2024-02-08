from flask import Blueprint
from db_models.models import user_credentials, job_info, index_info
from flask import jsonify, request, session
from flask_login import current_user

group_user_bp = Blueprint('group_user_bp', __name__)


@group_user_bp.route("/group_user/info/")
def getGroupUserInfo():
    user_id = current_user.get_id()
    users = user_credentials.query.filter_by(id=user_id)
    if user_id and len(users):
        user = users[0]
        user_info = [{
            'name': user.account,
            'group': user.group
        }]
    else:
        user_info = [{
            'name': "",
            'group': ""
        }]
    # Return the data as JSON
    return jsonify(user_info)


@group_user_bp.route("/group_user/data/")
def getGroupUserData():
    try:
        indices = index_info.query.all()
        if indices:
            data_info = [
                {
                    'index_name': x.name,
                    'pipline': x.pipeline.name,
                    'created': x.created,
                    'modified': x.modified
                }
                for x in indices
            ]
        else:
            data_info = [{
                'index_name' : '',
                'pipline' :'',
                'created' : '',
                'modified' : ''
            }]
        # Return the data as JSON
        return jsonify(data_info)
    except Exception as e:
        print("Error", e)
        return jsonify({"error": str(e)}), 500


@group_user_bp.route("/group_user/job/<id>")
def getGroupUserJob(id):
    try:
        
        job_info = [{
            'job_name' : 'job1',
            'pipline' :'pip1',
            'dataset' :'',
            'timestamp' : '2024-1-9',
            'status' : 'finished'
        }]
        # Return the data as JSON
        return jsonify(job_info)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@group_user_bp.route("/group_user/jobs/")
def getGroupUserJobs():
    try:
        jobs = job_info.query.all()
        if jobs:
            jobs_json = [
                {
                    'job_name': x.name,
                    'pipeline': x.index.pipeline.name,
                    'dataset': x.dataset,
                    'index': x.index.name,
                    'timestamp': x.created,
                    'status': x.status
                }
                for x in jobs
            ]
        else:
            jobs_json = [{
                'job_name': '',
                'pipeline': '',
                'dataset': '',
                'index': '',
                'timestamp': '',
                'status': ''
            }]
        # Return the data as JSON
        return jsonify(jobs_json)
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500
