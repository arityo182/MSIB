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

#get profile admin
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


#get profile pengajar
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

#get profile mentor
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

        if role not in role_group_all:
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
    ROUTE_NAME = str(request.path)

    now = datetime.datetime.now()

    id_user = str(get_jwt()["id_user"])
    role = str(get_jwt()["role_desc"])
    email = str(get_jwt()["email"])

    if role not in role_group_all:
        return permission_failed()

    try:
        dt = Data()
        data = request.json

        query_temp = " SELECT id_mahasiswa FROM mahasiswa WHERE id_mahasiswa = %s "
        values_temp = (id_user, )
        data_temp = dt.get_data(query_temp, values_temp)
        if len(data_temp) == 0:
            return defined_error("Gagal, data tidak ditemukan")

        query = """UPDATE mahasiswa SET id_mahasiswa = id_user"""
        values = ()

        if "email_ubah" in data:
            query += ", email = %s "
            values += (data["email_ubah"], )
        if "nama_ubah" in data:
            query += ", nama_mahasiswa = %s "
            values += (data["nama_ubah"], )
        if "tanggal_ubah" in data:
            query += ", tanggal_lahir = %s "
            values += (data["tanggal_ubah"], )
        if "asal_kampus_ubah" in data:
            query += ", asal_kampus = %s "
            values += (data["asal_kampus_ubah"], )
        if "posisi_ubah" in data:
            query += ", posisi = %s "
            values += (data["posisi_ubah"], )
        if "foto_user" in data:
            filename_photo = secure_filename(strftime(
                "%Y-%m-%d %H:%M:%S")+"_"+str(random_string_number_only(5))+"_foto_user.png")
            save(data["foto_user"], os.path.join(
                app.config['UPLOAD_FOLDER_FOTO_USER'], filename_photo))

            query += """ ,foto_user = %s """
            values += (filename_photo, )

        query += " WHERE id_mahasiswa = %s "
        values += (email, )
        dt.insert_data_last_row(query, values)
        hasil = {"status": "berhasil update data mahasiswa"}

    except Exception as e:
        print("Error: " + str(e))

    return jsonify(hasil)


# insert Data mahasiswa
@user.route("/insert_mahasiswa", methods=["POST", "OPTIONS"])
@cross_origin()
def insert_mahasiswa():
    try:
        hasil = {"status": "berhasil tambah data mahasiswa"}

        dt = Data()
        data = request.json

        # Cek data
        if "email" not in data:
            return parameter_error("Email tidak ada")
        if "nama_mahasiswa" not in data:
            return parameter_error("Nama Mahasiswa tidak di temukan")
        if "password" not in data:
            return parameter_error("Password tidak ada")
        if "asal_kampus" not in data:
            return parameter_error("Asal Kampus tidak di temukan")
        if "posisi" not in data:
            return parameter_error("Posisi tidak ada")

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
        query = "INSERT into mahasiswa (email, nama_mahasiswa, password, asal_kampus, posisi, status_id) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (email, nama_mahasiswa, pass_ency,
                  asal_kampus, posisi, status_id)
        dt.insert_data_last_row(query, values)
        return make_response(hasil)

    except Exception as e:
        return bad_request(str(e))

# menampilkan data mahasiswa


@user.route("/get_data_mahasiswa", methods=["GET"])
@cross_origin()
def get_data_mahasiswa():
    try:
        dt = Data()
        query = "SELECT * FROM mahasiswa"
        values = ()

        rowCount = dt.row_count(query, values)
        hasil = dt.get_data(query, values)
        hasil = {'data': hasil, 'status_code': 200, 'row_count': rowCount}
        return make_response(jsonify(hasil), 200)
    except Exception as e:
        return bad_request(str(e))


# update data mahasiswa
@user.route("/update_data_mahasiswa", methods=["PUT"])
@cross_origin()
def update_data_mahasiswa():
    hasil = {"status": "Gagal update data mahasiswa"}

    try:
        dt = Data()
        data = request.json

        # check email apakah sidah di lock
        if "email_awal" not in data:
            return parameter_error("Email belum di pilih")

        email = data["email_awal"]

        query = "UPDATE mahasiswa SET email = %s "
        values = (email, )

        if "email_ubah" in data:
            query += ", email = %s "
            values += (data["email_ubah"], )
        if "nama_ubah" in data:
            query += ", nama_mahasiswa = %s "
            values += (data["nama_ubah"], )
        if "password_ubah" in data:
            query += ", password = %s "
            password = data["password_ubah"]
            pass_ency = hashlib.md5(password.encode('utf-8')).hexdigest()
            values += (pass_ency, )
        if "asal_kampus_ubah" in data:
            query += ", asal_kampus = %s "
            values += (data["asal_kampus_ubah"], )
        if "posisi_ubah" in data:
            query += ", posisi = %s "
            values += (data["posisi_ubah"], )

        query += " WHERE email = %s "
        values += (email, )
        dt.insert_data_last_row(query, values)
        hasil = {"status": "berhasil update data mahasiswa"}

    except Exception as e:
        print("Error: " + str(e))

    return jsonify(hasil)

# delete data mahasiswa


@user.route("/delete_data_mahasiswa/<email>", methods=["DELETE"])
def delete_data_mahasiswa(email):
    hasil = {"status": "gagal hapus data mahasiswa"}

    try:
        dt = Data()
        data = request.json
        query = "DELETE FROM mahasiswa WHERE email = %s"
        values = (email, )
        dt.insert_data_last_row(query, values)
        hasil = {"status": "berhasil hapus data mahasiswa"}
    except Exception as e:
        print("Error: " + str(e))

    return jsonify(hasil)


# Menambha data pengajar
@user.route("/insert_pengajar", methods=["POST", "OPTIONS"])
@cross_origin()
def insert_pengajar():
    RUUTE_NAME = str(request.path)

    now = datetime.datetime.now()
    try:
        dt = Data()
        data = request.json

        hasil = {"status": "berhasil tambah data pengajar"}

        # Cek data
        if "email" not in data:
            return parameter_error("Email tidak ada")
        if "nama_pengajar" not in data:
            return parameter_error("Nama Pengajar tidak di temukan")
        if "password" not in data:
            return parameter_error("Password tidak ada")

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
        query = "INSERT into pengajar (email, nama_pengajar, password, status_id) VALUES (%s, %s, %s, %s)"
        values = (email, nama_pengajar, pass_ency, status_id)
        dt.insert_data_last_row(query, values)
        return make_response(hasil)

    except Exception as e:
        return bad_request(str(e))


# Melampilkan data pengajar
@user.route("/get_data_pengajar", methods=["GET"])
@cross_origin()
def get_data_pengajar():

    try:
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
@user.route("/update_data_pengajar", methods=["PUT"])
@cross_origin()
def update_data_pengajar():
    hasil = {"status": "Gagal update data pengajar"}

    try:
        dt = Data()
        data = request.json

        # check email apakah sidah di lock
        if "email_awal" not in data:
            return parameter_error("Email belum di pilih")

        email = data["email_awal"]

        query = "UPDATE pengajar SET email = %s "
        values = (email, )

        if "email_ubah" in data:
            query += ", email = %s "
            values += (data["email_ubah"], )
        if "nama_ubah" in data:
            query += ", nama_pengajar = %s "
            values += (data["nama_ubah"], )
        if "password_ubah" in data:
            query += ", password = %s "
            password = data["password_ubah"]
            pass_ency = hashlib.md5(password.encode('utf-8')).hexdigest()
            values += (pass_ency, )

        query += " WHERE email = %s "
        values += (email, )
        dt.insert_data_last_row(query, values)
        hasil = {"status": "berhasil update data pengajar"}

    except Exception as e:
        print("Error: " + str(e))

    return jsonify(hasil)

# Delete data pengajar


@user.route("/delete_data_pengajar/<email>", methods=["DELETE"])
def delete_data_pengajar(email):
    hasil = {"status": "gagal hapus data pengajar"}

    try:
        dt = Data()
        data = request.json

        query = "DELETE FROM pengajar WHERE email = %s"
        values = (email, )
        dt.insert_data_last_row(query, values)
        hasil = {"status": "berhasil hapus data pengajar"}
    except Exception as e:
        print("Error: " + str(e))

    return jsonify(hasil)


# Menambah data mentor
@user.route("/insert_mentor", methods=["POST", "OPTIONS"])
@cross_origin()
def insert_mentor():
    RUUTE_NAME = str(request.path)

    now = datetime.datetime.now()
    try:
        dt = Data()
        data = request.json

        hasil = {"status": "berhasil tambah data mentor"}

        # Cek data
        if "email" not in data:
            return parameter_error("Email tidak ada")
        if "nama_mentor" not in data:
            return parameter_error("Nama mentor tidak di temukan")
        if "password" not in data:
            return parameter_error("Password tidak ada")

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
        query = "INSERT into mentor (email, nama_mentor, password, status_id) VALUES (%s, %s, %s, %s)"
        values = (email, nama_mahasiswa, pass_ency, status_id)
        dt.insert_data_last_row(query, values)
        return make_response(hasil)

    except Exception as e:
        return bad_request(str(e))

# Melampilkan data mentor


@user.route("/get_data_mentor", methods=["GET"])
@cross_origin()
def get_data_mentor():

    try:
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
@user.route("/update_data_mentor", methods=["PUT"])
@cross_origin()
def update_data_mentor():
    hasil = {"status": "Gagal update data mentor"}

    try:
        dt = Data()
        data = request.json

        # check email apakah sidah di lock
        if "email_awal" not in data:
            return parameter_error("Email belum di pilih")

        email = data["email_awal"]

        query = "UPDATE mentor SET email = %s "
        values = (email, )

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

        query += " WHERE email = %s "
        values += (email, )
        dt.insert_data_last_row(query, values)
        hasil = {"status": "berhasil update data mentor"}

    except Exception as e:
        print("Error: " + str(e))

    return jsonify(hasil)

# Delete data mentor


@user.route("/delete_data_mentor/<email>", methods=["DELETE"])
def delete_data_mentor(email):
    hasil = {"status": "gagal hapus data mentor"}

    try:
        dt = Data()
        data = request.json

        query = "DELETE FROM mentor WHERE email = %s"
        values = (email, )
        dt.insert_data_last_row(query, values)
        hasil = {"status": "berhasil hapus data mentor"}
    except Exception as e:
        print("Error: " + str(e))

    return jsonify(hasil)

# endregion ================================= MY PROFILE AREA ==========================================================================

