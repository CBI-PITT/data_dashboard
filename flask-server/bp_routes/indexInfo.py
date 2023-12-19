
from flask import Blueprint
from admin_view.db_models.models import IndexInfo
from flask import  jsonify
indexInfo_bp = Blueprint('indexInfo', __name__)
@indexInfo_bp.route("/indexInfo")
def getIndexInfo():
    try:
        # Retrieve all data from the IndexInfo table
        all_info = IndexInfo.query.all()

        # Serialize the data into a list of dictionaries
        info_list = []
        for info in all_info:
            # info_list.append({
            #     'id': info.id,
            #     'field': info.field,
            #     'description': info.description,
            #     'type': info.type,
            #     'index': info.index
            #     # Add other columns as needed
            # })

            info_list.append(
                {
                    # 'id': info.id,
                    "field": info.field,
                    "field_description": info.description,
                    "type": info.type,
                    "es_index": info.es_index,
                }
            )

        # Return the data as JSON
        return jsonify(info_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500