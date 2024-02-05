from flask import Blueprint
from db_models.models import user_credentials, job_info
from flask import  jsonify
group_user_bp = Blueprint('group_user_bp', __name__)
@group_user_bp.route("/group_user/info/<id>")
def getGroupUserInfo(id):
    try:
        # Retrieve all data from the IndexInfo table
        # user_info = user_credentials.query.all()
        
        # Serialize the data into a list of dictionaries
        # info_list = []
        # for info in user_info:
        #     info_list.append(
        #         {
        #             # 'id': info.id,
        #             "field": info.field,
        #             "field_description": info.description,
        #             "type": info.type,
        #             "es_index": info.es_index,
        #         }
        #     )
        user_info = [{
            'name' : 'kelin',
            'group' :'cbi'
        }]
        # Return the data as JSON
        return jsonify(user_info)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@group_user_bp.route("/group_user/data/")
def getGroupUserData():
    try:
        
        data_info = [{
            'index_name' : 'klimstra',
            'pipline' :'pip1',
            'created' : '2024-1-9',
            'modified' : '2024-1-10'
        }]
        # Return the data as JSON
        return jsonify(data_info)
    except Exception as e:
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
                    'job_name': x.job_name,
                    'pipline': x.pipline_name,
                    'dataset': '',
                    'timestamp': x.time,
                    'status': x.status
                }
                for x in jobs
            ]
        else:
            jobs_json = [{
                'job_name': '',
                'pipline': '',
                'dataset': '',
                'timestamp': '',
                'status': ''
            }]
        # Return the data as JSON
        return jsonify(jobs_json)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
