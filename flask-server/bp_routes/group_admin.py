from flask import Blueprint
from db_models.models import user_credentials
from flask import  jsonify
group_admin_bp = Blueprint('group_admin_bp', __name__)
@group_admin_bp.route("/group_admin/info/<id>")
def getGroupAdminInfo(id):
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
    
@group_admin_bp.route("/group_admin/data")
def getGroupAdminData():
    try:
        
        data_info = [{
            'index_name' : 'cebra3.0',
            'pipline' :'pip1',
            'created' : '2024-1-9',
            'modified' : '2024-1-10'
        },
        {
            'index_name' : 'cebra1.0',
            'pipline' :'pip2',
            'created' : '2023-1-9',
            'modified' : '2023-1-10'
        },
        {
        'index_name' : 'cebra2.0',
            'pipline' :'pip3',
            'created' : '2023-1-8',
            'modified' : '2023-1-9'
        }]
        # Return the data as JSON
        return jsonify(data_info)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@group_admin_bp.route("/group_admin/job")
def getGroupAdminJob():
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
    
@group_admin_bp.route("/group_admin/pipline")
def getGroupAdminPipline():
    try:
        job_info = [{
            'pipline' :'pip1',
        }]
        # Return the data as JSON
        return jsonify(job_info)
    except Exception as e:
        return jsonify({"error": str(e)}), 500