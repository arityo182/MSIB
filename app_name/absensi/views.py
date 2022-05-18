import re
from flask import Blueprint, jsonify, request, make_response, render_template
from flask import current_app as app
from flask_jwt_extended import get_jwt, jwt_required
from flask_cors import cross_origin
from werkzeug.utils import secure_filename
from werkzeug.datastructures import ImmutableMultiDict
from time import gmtime, strftime
import hashlib
import datetime
import requests
import os
import base64
import random
import json
import warnings
import string
import numpy as np
import cv2

from .models import Data


#now = datetime.datetime.now()

absensi = Blueprint('absensi', __name__,
                    static_folder='../../upload/foto_user', static_url_path="/media")

# region ================================= FUNGSI-FUNGSI AREA ==========================================================================

role_group_all = ["mahasiswa", "mentor", "pengajar"]
role_group_admin = ["admin"]


def tambahLogs(logs):
    f = open(app.config['LOGS'] + "/" +
             secure_filename(strftime("%Y-%m-%d")) + ".txt", "a")
    f.write(logs)
    f.close()


def save(encoded_data, filename):
    arr = np.fromstring(base64.b64decode(encoded_data), np.uint8)
    img = cv2.imdecode(arr, cv2.IMREAD_UNCHANGED)
    return cv2.imwrite(filename, img)


def permission_failed():
    return make_response(jsonify({'error': 'Permission Failed', 'status_code': 403}), 403)


def request_failed():
    return make_response(jsonify({'error': 'Request Failed', 'status_code': 403}), 403)


def defined_error(description, error="Defined Error", status_code=499):
    return make_response(jsonify({'description': description, 'error': error, 'status_code': status_code}), status_code)


def parameter_error(description, error="Parameter Error", status_code=400):
    if app.config['PRODUCT_ENVIRONMENT'] == "DEV":
        return make_response(jsonify({'description': description, 'error': error, 'status_code': status_code}), status_code)
    else:
        return make_response(jsonify({'description': "Terjadi Kesalahan Sistem", 'error': error, 'status_code': status_code}), status_code)


def bad_request(description):
    if app.config['PRODUCT_ENVIRONMENT'] == "DEV":
        # Development
        return make_response(jsonify({'description': description, 'error': 'Bad Request', 'status_code': 400}), 400)
    else:
        # Production
        return make_response(jsonify({'description': "Terjadi Kesalahan Sistem", 'error': 'Bad Request', 'status_code': 400}), 400)


def randomString(stringLength):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))


def random_string_number_only(stringLength):
    letters = string.digits
    return ''.join(random.choice(letters) for i in range(stringLength))

# endregion ================================= FUNGSI-FUNGSI AREA ===============================================================


# region ================================= MY PROFILE AREA ==========================================================================

@absensi.route('/helo', methods=['GET'])
def helo():
    return "Hellows"


@absensi.route("/get_mahasiswa", methods=['GET'])
# @jwt_required()
# @cross_origin()
def get_mahasiswa():
    # id_user 		= int(get_jwt()["id_user"])
    # role            = strftime(get_jwt()["role_desc"])
    try:
        ROUTE_NAME = str(request.path)
        dt = Data()
        data = request.json
        # if role != "pengajar" :
        #     return permission_failed()
        if "id_course" not in data:
            return parameter_error("Missing id_course in Request Body")
        if "page" not in data:
            page = 1
        else:
            page = data['page']
        if "limit" not in data:
            limit = 10
        else:
            limit = data['limit']
        id_course = data["id_course"]
        # search =  data["search"]
        # limit =  data["limit"]
        # page =  data["page"]
        # order_by =  data["order_by"]
        query_temp = "SELECT id_mahasiswa FROM rppt WHERE id_course = %s"
        query = "SELECT rppt.id_mahasiswa ,mahasiswa.nama_mahasiswa FROM rppt LEFT JOIN mahasiswa ON rppt.id_mahasiswa=mahasiswa.id_mahasiswa WHERE id_course = %s "
        values = (id_course, )
        data_temp = dt.get_data(query, values)
        # return (jsonify(data_temp))
        # if len(data_temp == 0):
        #     return defined_error("ID Course tidak ditemukan")

        # Validasi parameter limit
        try:
            limit = int(limit)
        except Exception as e:
            return parameter_error("Invalid limit Parameter")
            # Parameter limit tidak boleh lebih kecil dari 1, kecuali -1 itu unlimited
        if limit != -1 and limit < 1:
            return parameter_error("Invalid limit Parameter")

            # jika variabel search tidak null(check kondisi)

            # if data['order_by']:
            #     order_by = data['order_by']
            #     if order_by == "judul_asc":
            #         query += " ORDER BY judul ASC "
            #     elif order_by == "judul_desc":
            #         query += " ORDER BY judul DESC "
            #     elif order_by == "waktu_asc":
            #         query += " ORDER BY waktu_mulai ASC "
            #     elif order_by == "waktu_desc":
            #         query += " ORDER BY waktu_mulai DESC "
            #     else:
            #         query += " ORDER BY pengajuan_event DESC "
            # else:
            #     query += " ORDER BY pengajuan_event ASC "

            # return make_response(str(limit), 200)
        rowCount = dt.row_count(query, values)
        if str(limit) != "-1":
            hasil = dt.get_data_lim_param(query, values, page, limit)
            # return (jsonify(hasil))
        else:
            hasil = dt.get_data(query, values)
        hasil = {'data': hasil, 'status_code': 200, 'page': page,
                 'offset': str(limit), 'row_count': rowCount}
        # return response(hasil)
        ########## INSERT LOG ##############
        # imd = ImmutableMultiDict(request.args)
        # imd = imd.to_dict()
        # param_logs = "[" + str(imd) + "]"
        # try:
        #     logs = secure_filename(strftime("%Y-%m-%d %H:%M:%S"))+" - "+ROUTE_NAME+" - id_user = "+str(id_user)+" - roles = "+str(role)+" - param_logs = "+param_logs+"\n"
        # except Exception as e:
        #         logs = secure_filename(strftime("%Y-%m-%d %H:%M:%S"))+" - "+ROUTE_NAME+" - id_user = NULL - roles = NULL - param_logs = "+param_logs+"\n"
        # tambahLogs(logs)
        # return("Hehe")
        return make_response(jsonify(hasil), 200)
    except Exception as e:
        # return ("hehe")
        return bad_request(str(e))


@absensi.route("/set_absensi_mahasiswa", methods=['POST', 'PUT'])
def set_absensi_mahasiswa():
    try:
        dt = Data()
        data = request.json

        if "id_course" not in data:
            return parameter_error("Missing id_course in Request Body")
        elif "id_mahasiswa" not in data:
            return parameter_error("Missing id_mahasiswa in Request Body")
        elif "absen_status" not in data:
            parameter_error("Missing absens_status in Request Body")
        elif "meetings" not in data:
            parameter_error("Missing meeting in Request Body")
        id_course = data["id_course"]
        id_mahasiswa = data["id_mahasiswa"]
        absen_status = data["absen_status"]
        pertemuan = data["pertemuan"]
        query = "UPDATE absensi SET absen_status =%s WHERE id_course =%s AND id_mahasiswa=%s AND pertemuan_ke=%s"
        values = (absen_status, id_course, id_mahasiswa, pertemuan)
        dt.insert_data(query, values)
        hasil = "Update status absensi mahasiswa berhasil"
        return response(hasil)
        # return("hehe")
    except Exception as e:
        return("Error: "+str(e))


@absensi.route("/get_recap_absensi", methods=['GET'])
def get_recap_absensi():
    try:
        dt = Data()
        data = request.json
        if "id_course" not in data:
            return parameter_error("Missing id_course in Request Body")
        elif "id_mahasiswa" not in data:
            return parameter_error("Missing id_mahasiswa in Request Body")
        elif "absen_status" not in data:
            return parameter_error("Missing absen_status in Request Body")
        id_course = data["id_course"]
        id_mahasiswa = data["id_mahasiswa"]
        absen_status = data["absen_status"]
        query = "SELECT * FROM absensi WHERE id_course=%s AND id_mahasiswa=%s AND keterangan=%s"
        values = (id_course, id_mahasiswa, absen_status)
        rowCount = dt.row_count(query, values)
        hasil = {'row_count': rowCount}
        return make_response(jsonify(hasil))
        hasil = "data berhasil didapatkan"
        return response(hasil)
    except Exception as e:
        return ("Error: "+str(e))
