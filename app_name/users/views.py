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

user = Blueprint('user', __name__,
                 static_folder='../../upload/foto_user', static_url_path="/media")

# region ================================= FUNGSI-FUNGSI AREA ==========================================================================

role_group_all = ["mahasiswa", "mentor", "pengajar"]
role_group_admin = ["SUPER ADMIN"]
role_mahasiswa = ["mahasiswa"]
role_pengajar = ["pengajar"]
role_mentor = ["mentor"]


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

# get profile admin
@user.route('/get_admin_profile', methods=['GET', 'OPTIONS'])
@jwt_required()
@cross_origin()
def get_admin_profile():
    try:
        ROUTE_NAME = str(request.path)

        id_user = str(get_jwt()["id_admin"])
        role = str(get_jwt()["role_desc"])
        nama = str(get_jwt()["nama"])

        if role not in role_group_admin:
            return permission_failed()

        dt = Data()

        query = """ SELECT a.* FROM admin a WHERE id_admin = %s """
        values = (id_user, )

        rowCount = dt.row_count(query, values)
        hasil = dt.get_data(query, values)
        hasil = {'data': hasil, 'status_code': 200, 'row_count': rowCount}
        ########## INSERT LOG ##############
        imd = ImmutableMultiDict(request.args)
        imd = imd.to_dict()
        param_logs = "[" + str(imd) + "]"
        try:
            logs = secure_filename(strftime("%Y-%m-%d %H:%M:%S"))+" - "+ROUTE_NAME + \
                " - id_user = "+str(id_user)+" - roles = "+str(role)+"\n"
        except Exception as e:
            logs = secure_filename(strftime(
                "%Y-%m-%d %H:%M:%S"))+" - "+ROUTE_NAME+" - id_user = NULL - roles = NULL\n"
        tambahLogs(logs)
        ####################################
        return make_response(jsonify(hasil), 200)
    except Exception as e:
        return bad_request(str(e))


# get profile pengajar
@user.route('/get_pengajar_profile', methods=['GET', 'OPTIONS'])
@jwt_required()
@cross_origin()
def get_pengajar_profile():
    try:
        ROUTE_NAME = str(request.path)

        id_user = str(get_jwt()["id_user"])
        role = str(get_jwt()["role_desc"])
        email = str(get_jwt()["email"])

        if role not in role_group_all:
            return permission_failed()

        dt = Data()

        query = """ SELECT a.* FROM pengajar a WHERE id_pengajar = %s """
        values = (id_user, )

        rowCount = dt.row_count(query, values)
        hasil = dt.get_data(query, values)
        hasil = {'data': hasil, 'status_code': 200, 'row_count': rowCount}
        ########## INSERT LOG ##############
        imd = ImmutableMultiDict(request.args)
        imd = imd.to_dict()
        param_logs = "[" + str(imd) + "]"
        try:
            logs = secure_filename(strftime("%Y-%m-%d %H:%M:%S"))+" - "+ROUTE_NAME + \
                " - id_user = "+str(id_user)+" - roles = "+str(role)+"\n"
        except Exception as e:
            logs = secure_filename(strftime(
                "%Y-%m-%d %H:%M:%S"))+" - "+ROUTE_NAME+" - id_user = NULL - roles = NULL\n"
        tambahLogs(logs)
        ####################################
        return make_response(jsonify(hasil), 200)
    except Exception as e:
        return bad_request(str(e))

# get profile mentor


@user.route('/get_mentor_profile', methods=['GET', 'OPTIONS'])
@jwt_required()
@cross_origin()
def get_mentor_profile():
    try:
        ROUTE_NAME = str(request.path)

        id_user = str(get_jwt()["id_user"])
        role = str(get_jwt()["role_desc"])
        email = str(get_jwt()["email"])

        if role not in role_group_all:
            return permission_failed()

        dt = Data()

        query = """ SELECT a.* FROM mentor a WHERE id_mentor = %s """
        values = (id_user, )

        rowCount = dt.row_count(query, values)
        hasil = dt.get_data(query, values)
        hasil = {'data': hasil, 'status_code': 200, 'row_count': rowCount}
        ########## INSERT LOG ##############
        imd = ImmutableMultiDict(request.args)
        imd = imd.to_dict()
        param_logs = "[" + str(imd) + "]"
        try:
            logs = secure_filename(strftime("%Y-%m-%d %H:%M:%S"))+" - "+ROUTE_NAME + \
                " - id_user = "+str(id_user)+" - roles = "+str(role)+"\n"
        except Exception as e:
            logs = secure_filename(strftime(
                "%Y-%m-%d %H:%M:%S"))+" - "+ROUTE_NAME+" - id_user = NULL - roles = NULL\n"
        tambahLogs(logs)
        ####################################
        return make_response(jsonify(hasil), 200)
    except Exception as e:
        return bad_request(str(e))


# get Profile mahasiswa
@user.route('/get_mahasiswa_profile', methods=['GET', 'OPTIONS'])
@jwt_required()
@cross_origin()
def get_mahasiswa_profile():
    try:
        ROUTE_NAME = str(request.path)

        id_user = str(get_jwt()["id_user"])
        role = str(get_jwt()["role_desc"])
        email = str(get_jwt()["email"])

        if role not in role_mahasiswa:
            return permission_failed()

        dt = Data()

        query = """ SELECT a.* FROM mahasiswa a WHERE id_mahasiswa = %s """
        values = (id_user, )

        rowCount = dt.row_count(query, values)
        hasil = dt.get_data(query, values)
        hasil = {'data': hasil, 'status_code': 200, 'row_count': rowCount}
        ########## INSERT LOG ##############
        imd = ImmutableMultiDict(request.args)
        imd = imd.to_dict()
        param_logs = "[" + str(imd) + "]"
        try:
            logs = secure_filename(strftime("%Y-%m-%d %H:%M:%S"))+" - "+ROUTE_NAME + \
                " - id_user = "+str(id_user)+" - roles = "+str(role)+"\n"
        except Exception as e:
            logs = secure_filename(strftime(
                "%Y-%m-%d %H:%M:%S"))+" - "+ROUTE_NAME+" - id_user = NULL - roles = NULL\n"
        tambahLogs(logs)
        ####################################
        return make_response(jsonify(hasil), 200)
    except Exception as e:
        return bad_request(str(e))

# update data profile mahasiswa pribadi


@user.route('/update_mahasiswa_profile', methods=['PUT', 'OPTIONS'])
@jwt_required()
@cross_origin()
def update_my_profile():

    try:
        id_user = str(get_jwt()["id_user"])
        role = str(get_jwt()["role_desc"])
        email = str(get_jwt()["email"])

        if role not in role_mahasiswa:
            return permission_failed()

        dt = Data()
        data = request.json

        query_temp = " SELECT id_mahasiswa FROM mahasiswa WHERE id_mahasiswa = %s "
        values_temp = (id_user, )
        data_mahasiswa = dt.get_data(query_temp, values_temp)
        if len(data_mahasiswa) == 0:
            return defined_error("Gagal, data tidak ditemukan")

        query = """UPDATE mahasiswa SET id_mahasiswa = %s """
        values = (id_user, )

        if "email_ubah" in data:
            query += """, email = %s """
            values += (data["email_ubah"], )
        else:
            return parameter_error("email_ubah tidak di temukan")
        if "nama_ubah" in data:
            query += """, nama_mahasiswa = %s """
            values += (data["nama_ubah"], )
        else:
            return parameter_error("nama_ubah tidak di temukan")
        if "tanggal_ubah" in data:
            query += """, tanggal_lahir = %s """
            values += (data["tanggal_ubah"], )
        else:
            return parameter_error("tanggal_ubah tidak di temukan")
        if "asal_kampus_ubah" in data:
            query += """, asal_kampus = %s """
            values += (data["asal_kampus_ubah"], )
        else:
            return parameter_error("asal_kampus_ubah tidak di temukan")
        if "posisi_ubah" in data:
            query += """, posisi = %s """
            values += (data["posisi_ubah"], )
        else:
            return parameter_error("posisi_ubah tidak di temukan")
        if "foto_user" in data:
            filename_photo = secure_filename(strftime(
                "%Y-%m-%d %H:%M:%S")+"_"+str(random_string_number_only(5))+"_foto_user.png")
            save(data["foto_user"], os.path.join(
                app.config['UPLOAD_FOLDER_FOTO_TEMPAT_UJI_KOMPETENSI'], filename_photo))

            query += """ ,foto_user = %s """
            values += (filename_photo, )
        else:
            return parameter_error("foto_user tidak di temukan")

        query += """ WHERE id_mahasiswa = %s """
        values += (id_user, )
        dt.insert_data_last_row(query, values)
        hasil = {"status": "berhasil update data mahasiswa"}
        return make_response(jsonify({'status_code': 200, 'description': hasil}), 200)
    except Exception as e:
        return bad_request(str(e))


# insert Data mahasiswa
@user.route("/insert_mahasiswa", methods=["POST", "OPTIONS"])
@jwt_required()
@cross_origin()
def insert_mahasiswa():
    try:
        id_user = str(get_jwt()["id_user"])
        role = str(get_jwt()["role_desc"])
        username = str(get_jwt()["username"])

        if role not in role_group_admin:
            return permission_failed()

        dt = Data()
        data = request.json

        # Cek data
        if "email" not in data:
            return parameter_error("email tidak temukan")
        if "nama_mahasiswa" not in data:
            return parameter_error("nama_mahasiswa tidak di temukan")
        if "password" not in data:
            return parameter_error("password tidak di temukan")
        if "asal_kampus" not in data:
            return parameter_error("asal_kampus tidak di temukan")
        if "posisi" not in data:
            return parameter_error("posisi tidak di temukan")

        email = data["email"]
        nama_mahasiswa = data["nama_mahasiswa"]
        password = data["password"]
        asal_kampus = data["asal_kampus"]
        posisi = data["posisi"]
        status_id = "mahasiswa"

        # check email dan nama mahasiwa di database
        query_temp = "SELECT * FROM mahasiswa WHERE email = %s"
        values_temp = (email, )
        if len(dt.get_data(query_temp, values_temp)) != 0:
            return defined_error("Mahasiswa sudah ada di database")

        # Covert password md5
        pass_ency = hashlib.md5(password.encode('utf-8')).hexdigest()

        # Masukan data ke database
        query = "INSERT into mahasiswa (email, nama_mahasiswa, password, asal_kampus, posisi, status_id, id_admin) VALUES (%s, %s, %s, %s, %s, %s,%s)"
        values = (email, nama_mahasiswa, pass_ency,
                  asal_kampus, posisi, status_id, id_user)
        dt.insert_data(query, values)
        hasil = {"status": "berhasil tambah data mahasiswa"}
        return make_response(jsonify({'status_code': 200, 'description': hasil}), 200)
    except Exception as e:
        return bad_request(str(e))

# menampilkan data mahasiswa


@user.route("/get_data_mahasiswa", methods=["GET"])
@jwt_required()
@cross_origin()
def get_data_mahasiswa():
    try:

        id_user = str(get_jwt()["id_user"])
        role = str(get_jwt()["role_desc"])
        username = str(get_jwt()["username"])

        if role not in role_group_admin:
            return permission_failed()

        dt = Data()
        query = "SELECT * FROM mahasiswa"
        values = ()

        rowCount = dt.row_count(query, values)
        hasil = dt.get_data(query, values)
        hasil = {'data': hasil, 'status_code': 200, 'row_count': rowCount}
        return make_response(jsonify({'status_code': 200, 'description': hasil}), 200)
    except Exception as e:
        return bad_request(str(e))


# update data mahasiswa
@user.route("/update_data_mahasiswa/<id>", methods=["PUT"])
@jwt_required()
@cross_origin()
def update_data_mahasiswa(id):

    try:
        id_user = str(get_jwt()["id_user"])
        role = str(get_jwt()["role_desc"])
        username = str(get_jwt()["username"])

        if role not in role_group_admin:
            return permission_failed()

        dt = Data()

        query = "SELECT id_mahasiswa FROM mahasiswa WHERE id_mahasiswa = %s "
        values = (id, )
        data_mahasiswa = dt.get_data(query, values)
        if len(data_mahasiswa) == 0:
            return defined_error("id mahasiswa tidak di temukan", 401)

        data = request.json

        # check email apakah sidah di lock
        # if "email_awal" not in data:
        #     return parameter_error("Email belum di pilih")

        # email = data["email_awal"]

        query = "UPDATE mahasiswa SET id_mahasiswa = %s "
        values = (id, )

        if "email_ubah" in data:
            query += ", email = %s "
            values += (data["email_ubah"], )
        else:
            return parameter_error("email_ubah tidak ditemukan")
        if "nama_ubah" in data:
            query += ", nama_mahasiswa = %s "
            values += (data["nama_ubah"], )
        else:
            return parameter_error("nama_ubah tidak ditemukan")
        if "password_ubah" in data:
            query += ", password = %s "
            password = data["password_ubah"]
            pass_ency = hashlib.md5(password.encode('utf-8')).hexdigest()
            values += (pass_ency, )
        else:
            return parameter_error("password_ubah tidak ditemukan")
        if "asal_kampus_ubah" in data:
            query += ", asal_kampus = %s "
            values += (data["asal_kampus_ubah"], )
        else:
            return parameter_error("asal_kampus_ubah tidak ditemukan")
        if "posisi_ubah" in data:
            query += ", posisi = %s "
            values += (data["posisi_ubah"], )
        else:
            return parameter_error("posisi_ubah tidak ditemukan")

        query += " WHERE id_mahasiswa = %s "
        values += (id, )
        dt.insert_data_last_row(query, values)
        hasil = {"status": "berhasil update data mahasiswa"}
        return make_response(jsonify({'status_code': 200, 'description': hasil}), 200)
    except Exception as e:
        return bad_request(str(e))


# delete data mahasiswa


@user.route("/delete_data_mahasiswa/<id>", methods=["DELETE"])
@jwt_required()
@cross_origin()
def delete_data_mahasiswa(id):
    hasil = {"status": "gagal hapus data mahasiswa"}

    try:
        id_user = str(get_jwt()["id_user"])
        role = str(get_jwt()["role_desc"])
        username = str(get_jwt()["username"])

        if role not in role_group_admin:
            return permission_failed()

        dt = Data()

        query = "SELECT id_mahasiswa FROM mahasiswa WHERE id_mahasiswa = %s "
        values = (id, )
        data_mahasiswa = dt.get_data(query, values)
        if len(data_mahasiswa) == 0:
            return defined_error("id mahasiswa tidak di temukan", 401)

        data = request.json
        query = "DELETE FROM mahasiswa WHERE id_mahasiswa = %s"
        values = (id, )
        dt.insert_data(query, values)
        hasil = {"status": "berhasil hapus data mahasiswa"}
        return make_response(jsonify({'status_code': 200, 'description': hasil}), 200)
    except Exception as e:
        return bad_request(str(e))


# Menambha data pengajar
@user.route("/insert_pengajar", methods=["POST", "OPTIONS"])
@jwt_required()
@cross_origin()
def insert_pengajar():
    RUUTE_NAME = str(request.path)

    now = datetime.datetime.now()
    try:
        id_user = str(get_jwt()["id_user"])
        role = str(get_jwt()["role_desc"])
        username = str(get_jwt()["username"])

        if role not in role_group_admin:
            return permission_failed()

        dt = Data()
        data = request.json

        hasil = {"status": "berhasil tambah data pengajar"}

        # Cek data
        if "email" not in data:
            return parameter_error("email tidak ditemukan")
        if "nama_pengajar" not in data:
            return parameter_error("nama_pengajar tidak di temukan")
        if "password" not in data:
            return parameter_error("password tidak ada")

        email = data["email"]
        nama_pengajar = data["nama_pengajar"]
        password = data["password"]
        status_id = "pengajar"

        # check email dan nama mahasiwa di database
        query_temp = "SELECT * FROM pengajar WHERE email = %s"
        values_temp = (email, )
        if len(dt.get_data(query_temp, values_temp)) != 0:
            return defined_error("Pengajar sudah ada di database")

        # Covert password md5
        pass_ency = hashlib.md5(password.encode('utf-8')).hexdigest()

        # Masukan data ke database
        query = "INSERT into pengajar (email, nama_pengajar, password, status_id, id_admin) VALUES (%s, %s, %s, %s, %s)"
        values = (email, nama_pengajar, pass_ency, status_id, id_user)
        dt.insert_data(query, values)
        return make_response(jsonify({'status_code': 200, 'description': hasil}), 200)

    except Exception as e:
        return bad_request(str(e))


# Melampilkan data pengajar
@user.route("/get_data_pengajar", methods=["GET"])
@jwt_required()
@cross_origin()
def get_data_pengajar():

    try:
        id_user = str(get_jwt()["id_user"])
        role = str(get_jwt()["role_desc"])
        username = str(get_jwt()["username"])

        if role not in role_group_admin:
            return permission_failed()

        dt = Data()
        query = "SELECT * FROM pengajar"
        values = ()

        rowCount = dt.row_count(query, values)
        hasil = dt.get_data(query, values)
        hasil = {'data': hasil, 'status_code': 200, 'row_count': rowCount}
        return make_response(jsonify(hasil), 200)
    except Exception as e:
        return bad_request(str(e))


# update data pengajar
@user.route("/update_data_pengajar/<id>", methods=["PUT"])
@jwt_required()
@cross_origin()
def update_data_pengajar(id):
    try:
        id_user = str(get_jwt()["id_user"])
        role = str(get_jwt()["role_desc"])
        username = str(get_jwt()["username"])

        if role not in role_group_admin:
            return permission_failed()

        dt = Data()

        query = "SELECT id_pengajar FROM pengajar WHERE id_pengajar = %s "
        values = (id, )
        data_pengajar = dt.get_data(query, values)
        if len(data_pengajar) == 0:
            return defined_error("id pengajar tidak di temukan", 401)

        data = request.json

        # check email apakah sidah di lock
        # if "email_awal" not in data:
        #     return parameter_error("Email belum di pilih")

        # email = data["email_awal"]

        query = "UPDATE pengajar SET id_pengajar = %s "
        values = (id, )

        if "email_ubah" in data:
            query += ", email = %s "
            values += (data["email_ubah"], )
        else:
            return parameter_error("email_ubah tidak di temukan")
        if "nama_ubah" in data:
            query += ", nama_pengajar = %s "
            values += (data["nama_ubah"], )
        else:
            return parameter_error("nama_ubah tidak di temukan")
        if "password_ubah" in data:
            query += ", password = %s "
            password = data["password_ubah"]
            pass_ency = hashlib.md5(password.encode('utf-8')).hexdigest()
            values += (pass_ency, )
        else:
            return parameter_error("password_ubah tidak di temukan")

        query += " WHERE id_pengajar = %s "
        values += (id, )
        dt.insert_data_last_row(query, values)
        hasil = {"status": "berhasil update data pengajar"}
        return make_response(jsonify({'status_code': 200, 'description': hasil}), 200)
    except Exception as e:
        return bad_request(str(e))

# Delete data pengajar


@user.route("/delete_data_pengajar/<id>", methods=["DELETE"])
@jwt_required()
@cross_origin()
def delete_data_pengajar(id):
    try:
        id_user = str(get_jwt()["id_user"])
        role = str(get_jwt()["role_desc"])
        username = str(get_jwt()["username"])

        if role not in role_group_admin:
            return permission_failed()

        dt = Data()

        query = "SELECT id_pengajar FROM pengajar WHERE id_pengajar = %s "
        values = (id, )
        data_pengajar = dt.get_data(query, values)
        if len(data_pengajar) == 0:
            return defined_error("id pengajar tidak di temukan", 401)

        data = request.json

        query = "DELETE FROM pengajar WHERE id_pengajar = %s"
        values = (id, )
        dt.insert_data(query, values)
        hasil = {"status": "berhasil hapus data pengajar"}
        return make_response(jsonify({'status_code': 200, 'description': hasil}), 200)
    except Exception as e:
        return bad_request(str(e))


# Menambah data mentor
@user.route("/insert_mentor", methods=["POST", "OPTIONS"])
@jwt_required()
@cross_origin()
def insert_mentor():
    RUUTE_NAME = str(request.path)

    now = datetime.datetime.now()
    try:
        id_user = str(get_jwt()["id_user"])
        role = str(get_jwt()["role_desc"])
        username = str(get_jwt()["username"])

        if role not in role_group_admin:
            return permission_failed()

        dt = Data()
        data = request.json

        hasil = {"status": "berhasil tambah data mentor"}

        # Cek data
        if "email" not in data:
            return parameter_error("email tidak di temukan")
        if "nama_mentor" not in data:
            return parameter_error("nama_mentor tidak di temukan")
        if "password" not in data:
            return parameter_error("password tidak ada")

        email = data["email"]
        nama_mahasiswa = data["nama_mentor"]
        password = data["password"]
        status_id = "mentor"

        # check email dan nama mahasiwa di database
        query_temp = "SELECT * FROM mentor WHERE email = %s "
        values_temp = (email, )
        if len(dt.get_data(query_temp, values_temp)) != 0:
            return defined_error("Mentor sudah ada di database")

        # Covert password md5
        pass_ency = hashlib.md5(password.encode('utf-8')).hexdigest()

        # Masukan data ke database
        query = "INSERT into mentor (email, nama_mentor, password, status_id, id_admin) VALUES (%s, %s, %s, %s, %s)"
        values = (email, nama_mahasiswa, pass_ency, status_id, id_user)
        dt.insert_data(query, values)
        return make_response(jsonify({'status_code': 200, 'description': hasil}), 200)

    except Exception as e:
        return bad_request(str(e))

# Melampilkan data mentor


@user.route("/get_data_mentor", methods=["GET"])
@jwt_required()
@cross_origin()
def get_data_mentor():

    try:
        id_user = str(get_jwt()["id_user"])
        role = str(get_jwt()["role_desc"])
        username = str(get_jwt()["username"])

        if role not in role_group_admin:
            return permission_failed()

        dt = Data()
        query = "SELECT * FROM mentor"
        values = ()

        rowCount = dt.row_count(query, values)
        hasil = dt.get_data(query, values)
        hasil = {'data': hasil, 'status_code': 200, 'row_count': rowCount}
        return make_response(jsonify(hasil), 200)
    except Exception as e:
        return bad_request(str(e))


# update data mentor
@user.route("/update_data_mentor/<id>", methods=["PUT", "OPTIONS"])
@jwt_required()
@cross_origin()
def update_data_mentor(id):
    try:
        id_user = str(get_jwt()["id_user"])
        role = str(get_jwt()["role_desc"])
        username = str(get_jwt()["username"])

        if role not in role_group_admin:
            return permission_failed()

        dt = Data()

        query = "SELECT id_mentor FROM mentor WHERE id_mentor = %s "
        values = (id, )
        data_pengajar = dt.get_data(query, values)
        if len(data_pengajar) == 0:
            return defined_error("id mentor tidak di temukan", 401)

        data = request.json

        query = "UPDATE mentor SET id_mentor = %s "
        values = (id, )

        if "email_ubah" in data:
            query += ", email = %s "
            values += (data["email_ubah"], )
        if "nama_ubah" in data:
            query += ", nama_mentor = %s "
            values += (data["nama_ubah"], )
        if "password_ubah" in data:
            query += ", password = %s "
            password = data["password_ubah"]
            pass_ency = hashlib.md5(password.encode('utf-8')).hexdigest()
            values += (pass_ency, )

        query += " WHERE id_mentor = %s "
        values += (id, )
        dt.insert_data_last_row(query, values)
        hasil = {"status": "berhasil update data mentor"}
        return make_response(jsonify({'status_code': 200, 'description': hasil}), 200)
    except Exception as e:
        return bad_request(str(e))

# Delete data mentor


@user.route("/delete_data_mentor/<id>", methods=["DELETE"])
@jwt_required()
@cross_origin()
def delete_data_mentor(id):
    hasil = {"status": "gagal hapus data mentor"}

    try:

        id_user = str(get_jwt()["id_user"])
        role = str(get_jwt()["role_desc"])
        username = str(get_jwt()["username"])

        if role not in role_group_admin:
            return permission_failed()

        dt = Data()
        query = "SELECT id_mentor FROM mentor WHERE id_mentor = %s "
        values = (id, )
        data_mentor = dt.get_data(query, values)
        if len(data_mentor) == 0:
            return defined_error("id mentor tidak di temukan", 401)

        query = "DELETE FROM mentor WHERE id_mentor = %s"
        values = (id, )
        dt.insert_data(query, values)
        hasil = {"status": "berhasil hapus data mentor"}
        return make_response(jsonify({'status_code': 200, 'description': hasil}), 200)
    except Exception as e:
        return bad_request(str(e))

# endregion ================================= MY PROFILE AREA ==========================================================================
