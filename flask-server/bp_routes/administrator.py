
import imp
from flask import Blueprint, request, current_app
from flask_login import current_user
from db_models.models import db, admin_credentials, field_info, parameters, index_info
from flask import  jsonify, render_template, request, redirect, url_for
from flask_login import login_user, logout_user
import os
import pandas as pd
from datetime import datetime
from elasticsearch import Elasticsearch
from config.es_config import es_server
from config.host import UPLOAD_FOLDER_PATH
from importing.es_importing import indexing_existed, indexing_new
# from server import app
es = Elasticsearch(es_server, request_timeout=180)
administrator_bp = Blueprint("administrator", __name__)




@administrator_bp.route("/admin_user/login", methods=["POST"])
def admin_login():
    # print(request.form['account'])
    # print(request.form['password'])
    user = admin_credentials.query.filter_by(
        account=request.form["account"], password=request.form["password"]
    ).first()
    print(user)
    if user:
        login_user(user)
        print("logged in")
        return redirect(url_for("admin.home"))

    else:
        return render_template("admin/security/error_login.html")


@administrator_bp.route("/admin_user/logout")
def admin_logout():
    logout_user()
    return render_template("admin/security/logout.html")





@administrator_bp.route("/indexing/mapping_store", methods=["POST"])
def add_index_info():
    try:
        data = request.json
        mapping = data["mapping"]
        index = data["index"]

        for key, value in mapping.items():
            print(key, value["type"])
            new_index_info = field_info(
                field=key, description="", type=value["type"], es_index=index
            )
            db.session.add(new_index_info)

        db.session.commit()

        return jsonify({"message": "Parameters stored successfully"}), 200
    except Exception as e:
        db.session.rollback()  # Rollback changes if an exception occurs
        return jsonify({"error": str(e)}), 500





@administrator_bp.route("/indexing/upload_file", methods=["POST"])
def upload_csv():
    if "file" not in request.files:
        return jsonify({"error": "No file part"})

    file = request.files["file"]
    file_name = file.filename
    delimiter = request.form["delimiter"]
    separator = request.form["separator"]
    index_name = request.form["index_name"]

    # print(file)

    if file_name == "":
        return jsonify({"error": "No selected file"})

    if file:
        if file.mimetype != "text/csv":
            return jsonify({"error": "Invalid file type. Please upload a CSV file"})

        file.save(os.path.join(UPLOAD_FOLDER_PATH, file_name))

        print(file_name + " " + "uploaded")
        separator_mark = {
            "comma": ",",
            "tab": "\t",
            "semicolon": ";",
            "space": " ",
        }.get(separator, ",")

        delimiter_mark = {
            "double_quote": '"',
            "single_quote": "'",
        }.get(delimiter, '"')
        try:
            df = pd.read_csv(
               UPLOAD_FOLDER_PATH + "/" + file_name,
                sep=separator_mark,
                quotechar=delimiter_mark,
            )
        except Exception as e:
            os.remove(UPLOAD_FOLDER_PATH + "/" + file_name)
            error_message = str(e)  # Get the error message
            return render_template(
                "admin/indexing/error_indexing.html", error_message=error_message
            )
        indices = es.cat.indices(format="json")
        # print(indices)
        indexNamesArray = [entry["index"] for entry in indices]
        if index_name in indexNamesArray:
            mappings = es.indices.get_mapping(index=index_name)[index_name]["mappings"][
                "properties"
            ]
            # Check if lengths of DataFrame columns and mappings keys are equal
            if len(df.columns) != len(mappings.keys()):
                return render_template(
                    "admin/indexing/error_indexing.html",
                    error_message="Column count inconsistency between DataFrame and mappings",
                )

            # Check if all DataFrame columns exist in mappings
            missing_columns = [col for col in df.columns if col not in mappings.keys()]

            if missing_columns:
                return render_template(
                    "admin/indexing/error_indexing.html",
                    error_message=f"Columns {', '.join(missing_columns)} do not exist in mappings",
                )
            try:
                indexing_existed(file_name, separator, delimiter, index_name)
                return render_template(
                    "admin/indexing/index_complete.html", file_name=file_name
                )

            except Exception as e:
                error_message = str(e)  # Get the error message
                return render_template(
                    "admin/indexing/error_indexing.html", error_message=error_message
                )
        else:
            for column in df.columns:
                if df[column].isnull().any():
                    # Change the data type of the column to object if it contains null values
                    df[column] = df[column].astype("object")

            column_info = df.dtypes
            # print(column_info,'-------------------------------------')
            columns_data_types = column_info.to_dict()
            # print(columns_data_types)
            indices = es.cat.indices(format="json")
            # print(indices)
            indexNamesArray = [entry["index"] for entry in indices]
            return render_template(
                "admin/indexing/mapping_setting.html",
                columns_data_types=columns_data_types,
                file_name=file_name,
                index_name=index_name,
                separator=separator,
                delimiter=delimiter,
                column_name=columns_data_types.keys(),
            )


@administrator_bp.route("/indexing/start", methods=["POST"])
def index_file():
    data = request.form
    print(data)
    file_name = data["file_name_excluded"]
    index_name = data["index_name_excluded"]
    separator = data["separator_excluded"]
    delimiter = data["delimiter_excluded"]
    shard = data["shard_number_excluded"]
    resolution_micrometer = (
        None
        if data["resolution_micrometer_excluded"] == ""
        else data["resolution_micrometer_excluded"]
    )
    density_atlas_col_name = (
        None
        if data["density_atlas_col_name_excluded"] == "none"
        else data["density_atlas_col_name_excluded"]
    )
    density_agg = (
        None if data["density_agg_excluded"] == "none" else data["density_agg_excluded"]
    )
    n_value_col_name = (
        None
        if data["n_value_col_name_excluded"] == "none"
        else data["n_value_col_name_excluded"]
    )
    # print(file_name, index_name)
    properties = {}
    for key, value in data.items():
        if not key.endswith("excluded"):
            properties[key] = {"type": value}
    mappings = {"properties": properties}
    # print(mappings)
    try:
        indexing_new(file_name, separator, delimiter, index_name, shard, mappings)
        # existing_entry = Parameters.query.filter_by(index_name=index_name).first()
        # if existing_entry:
        #     pass
        # else:
        new_entry_para = parameters(
            es_index=index_name,
            resolution_micrometer=resolution_micrometer,
            density_agg=density_agg,
            density_atlas_col_name=density_atlas_col_name,
            n_value_col_name=n_value_col_name,
        )
        db.session.add(new_entry_para)
        new_entry_index = index_info(
            index_name = index_name,
            created =  datetime.now().strftime("%Y-%m-%d"),
            # modified = '',
            # breif = ''
        )
        db.session.add(new_entry_index)
        db.session.commit()
    except Exception as e:
        error_message = str(e)  # Get the error message
        return render_template(
            "admin/indexing/error_indexing.html", error_message=error_message
        )
    return render_template("admin/indexing/index_complete.html", file_name=file_name)
