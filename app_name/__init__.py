# -*- coding: utf-8 -*-
import re
import sys
from flask import Flask, jsonify, request, make_response, render_template, redirect, Blueprint
from flask_jwt_extended import create_access_token, get_jwt, jwt_required, JWTManager
from flask_cors import CORS, cross_origin
from werkzeug.utils import secure_filename
from time import gmtime, strftime
import json
import datetime
import os
import base64
import random
import hashlib
import warnings

from .users.views import user

from . data import Data
from . import config as CFG


# IMPORT BLUEPRINT

# region >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> CONFIGURATION <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
app = Flask(__name__, static_url_path=None)  # panggil modul flask

# CORS Configuration
cors = CORS(app, resources={r"*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'

# Flask JWT Extended Configuration
app.config['SECRET_KEY'] = CFG.JWT_SECRET_KEY
app.config['JWT_HEADER_TYPE'] = CFG.JWT_HEADER_TYPE
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(
    days=1)  # 1 hari token JWT expired
jwt = JWTManager(app)

# Application Configuration
app.config['PRODUCT_ENVIRONMENT'] = CFG.PRODUCT_ENVIRONMENT
app.config['BACKEND_BASE_URL'] = CFG.BACKEND_BASE_URL


# LOGS FOLDER PATH
app.config['LOGS'] = CFG.LOGS_FOLDER_PATH

# UPLOAD FOLDER PATH
UPLOAD_FOLDER_PATH = CFG.UPLOAD_FOLDER_PATH

# Cek apakah Upload Folder Path sudah diakhiri dengan slash atau belum
if UPLOAD_FOLDER_PATH[-1] != "/":
    UPLOAD_FOLDER_PATH = UPLOAD_FOLDER_PATH + "/"

app.config['UPLOAD_FOLDER_FOTO_USER'] = UPLOAD_FOLDER_PATH+"foto_user/"
app.config['UPLOAD_FOLDER_FOTO_TEMPAT_UJI_KOMPETENSI'] = UPLOAD_FOLDER_PATH + \
    "lokasi/foto_tempat_uji_kompetensi/"

# Create folder if doesn't exist
list_folder_to_create = [
    app.config['LOGS'],
    app.config['UPLOAD_FOLDER_FOTO_USER'],
    app.config['UPLOAD_FOLDER_FOTO_TEMPAT_UJI_KOMPETENSI']
]
for x in list_folder_to_create:
    if os.path.exists(x) == False:
        os.makedirs(x)

# endregion >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> CONFIGURATION <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<


# region >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> FUNCTION AREA <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

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


def tambahLogs(logs):
    f = open(app.config['LOGS'] + "/" +
             secure_filename(strftime("%Y-%m-%d")) + ".txt", "a")
    f.write(logs)
    f.close()

# endregion >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> FUNCTION AREA <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<


# region >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> AUTH AREA (JWT) <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

# Tambah data Admin
@app.route("/register_admin", methods=['POST'])
@cross_origin()
def register_admin():
    ROUTE_NAME = request.path
    try:
        dt = Data()
        data = request.json

        # Check Data
        if "username" not in data:
            return parameter_error("Username belum diisi")
        if "password" not in data:
            return parameter_error("Password belum diisi")
        if "nama" not in data:
            return parameter_error("Nama belum diisi")

        # mendapatkan data dari request body
        username = request.json.get('username')
        password = request.json.get('password')
        nama = request.json.get('nama')
        status_id = "admin"

        # check data username di database
        query_temp = "SELECT username FROM admin WHERE username = %s"
        values_temp = (username, )
        if len(dt.get_data(query_temp, values_temp)) != 0:
            return defined_error("Username telah digunakan")

        # mengubah password ke md5
        pass_ency = hashlib.md5(password.encode("utf-8")).hexdigest()

        # insert data ke table admin
        query = "INSERT into admin (username, password, nama, status_id) VALUES (%s, %s, %s, %s)"
        values = (username, pass_ency, nama, status_id)
        dt.insert_data_last_row(query, values)
        return make_response(jsonify({'status_code': 200, 'description': "berhasil nambah admin"}))
    except Exception as e:
        return bad_request(str(e))

# Melihat data admin


@app.route("/get_data_admin", methods=["GET"])
@cross_origin()
def get_data_admin():

    try:
        dt = Data()
        query = "SELECT * FROM admin"
        values = ()

        rowCount = dt.row_count(query, values)
        hasil = dt.get_data(query, values)
        hasil = {'data': hasil, 'status_code': 200, 'row_count': rowCount}
        return make_response(jsonify(hasil), 200)
    except Exception as e:
        return bad_request(str(e))

# Delete admin


@app.route("/delete_data_admin/<username>", methods=["DELETE"])
def delete_data_mentor(username):
    hasil = {"status": "gagal hapus data Admin"}

    try:
        dt = Data()
        data = request.json

        query = "DELETE FROM admin WHERE username = %s"
        values = (username, )
        dt.insert_data_last_row(query, values)
        hasil = {"status": "berhasil hapus data Admin"}
    except Exception as e:
        print("Error: " + str(e))

    return jsonify(hasil)


# Login admin
@app.route("/login_admin", methods=["POST"])
@cross_origin()
def login_admin():
    ROUTE_NAME = request.path

    data = request.json

    if "username" not in data:
        return parameter_error("Username tidak ada")
    if "password" not in data:
        return parameter_error("Password tidak ada")

    username = data["username"]
    password = data["password"]

    username = username.lower()
    password_enc = hashlib.md5(password.encode(
        'utf-8')).hexdigest()  # Convert password to md5

    # mengecek data pada database
    dt = Data()
    query = """SELECT id_admin, password, status_id FROM admin WHERE username = %s """
    values = (username, )
    data_admin = dt.get_data(query, values)
    if len(data_admin) == 0:
        return defined_error("Username tidak di temukan")
    data_admin = data_admin[0]
    db_id_admin = data_admin["id_admin"]
    db_password = data_admin["password"]

    if password_enc != db_password:
        return defined_error("Wrong Password", "Invalid Credential", 401)

    role_desc = "SUPER ADMIN"

    jwt_payload = {
        "id_user": db_id_admin,
        "role_desc": role_desc,
        "username": username
    }

    access_token = create_access_token(username, additional_claims=jwt_payload)

    # try:
    #     logs = secure_filename(strftime("%Y-%m-%d %H:%M:%S"))+" - "+ROUTE_NAME+" - id_user = "+str(db_id_user)+" - roles = "+str(role)+"\n"
    # except Exception as e:
    #     logs = secure_filename(strftime("%Y-%m-%d %H:%M:%S"))+" - "+ROUTE_NAME+" - id_user = NULL - roles = NULL\n"
    # tambahLogs(logs)

    return jsonify(access_token=access_token)

# Login user Mahasiswa


@app.route("/login_user/mahasiswa", methods=["POST"])
@cross_origin()
def login_mahasiswa():
    ROUTE_NAME = request.path

    data = request.json

    if "email" not in data:
        return parameter_error("Email tidak ada")
    if "password" not in data:
        return parameter_error("Password tidak ada")

    email = data["email"]
    password = data["password"]

    password_enc = hashlib.md5(password.encode(
        'utf-8')).hexdigest()  # Convert password to md5

    # mengecek data pada database
    dt = Data()
    query = "SELECT id_mahasiswa, password, status_id FROM mahasiswa WHERE email = %s "
    values = (email, )
    data_admin = dt.get_data(query, values)
    if len(data_admin) == 0:
        return defined_error("Email tidak di temukan")
    data_admin = data_admin[0]
    db_id_mahasiswa = data_admin["id_mahasiswa"]
    db_password = data_admin["password"]

    if password_enc != db_password:
        return defined_error("Wrong Password", "Invalid Credential", 401)

    role_desc = "Mahasiswa"

    jwt_payload = {
        "id_user": db_id_mahasiswa,
        "role_desc": role_desc,
        "email": email
    }

    access_token = create_access_token(email, additional_claims=jwt_payload)

    # try:
    #     logs = secure_filename(strftime("%Y-%m-%d %H:%M:%S"))+" - "+ROUTE_NAME+" - id_user = "+str(db_id_user)+" - roles = "+str(role)+"\n"
    # except Exception as e:
    #     logs = secure_filename(strftime("%Y-%m-%d %H:%M:%S"))+" - "+ROUTE_NAME+" - id_user = NULL - roles = NULL\n"
    # tambahLogs(logs)

    return jsonify(access_token=access_token)

# Login user Pengajar


@app.route("/login_user/pengajar", methods=["POST"])
@cross_origin()
def login_pengajar():
    ROUTE_NAME = request.path

    data = request.json

    if "email" not in data:
        return parameter_error("Email tidak ada")
    if "password" not in data:
        return parameter_error("Password tidak ada")

    email = data["email"]
    password = data["password"]

    password_enc = hashlib.md5(password.encode(
        'utf-8')).hexdigest()  # Convert password to md5

    # mengecek data pada database
    dt = Data()
    query = "SELECT id_pengajar, password, status_id FROM pengajar WHERE email = %s "
    values = (email, )
    data_admin = dt.get_data(query, values)
    if len(data_admin) == 0:
        return defined_error("Email tidak di temukan")
    data_admin = data_admin[0]
    db_id_pengajar = data_admin["id_pengajar"]
    db_password = data_admin["password"]

    if password_enc != db_password:
        return defined_error("Wrong Password", "Invalid Credential", 401)

    role_desc = "pengajar"

    jwt_payload = {
        "id_user": db_id_pengajar,
        "role_desc": role_desc,
        "email": email
    }

    access_token = create_access_token(email, additional_claims=jwt_payload)

    # try:
    #     logs = secure_filename(strftime("%Y-%m-%d %H:%M:%S"))+" - "+ROUTE_NAME+" - id_user = "+str(db_id_user)+" - roles = "+str(role)+"\n"
    # except Exception as e:
    #     logs = secure_filename(strftime("%Y-%m-%d %H:%M:%S"))+" - "+ROUTE_NAME+" - id_user = NULL - roles = NULL\n"
    # tambahLogs(logs)

    return jsonify(access_token=access_token)


# Login user Mentor
@app.route("/login_user/mentor", methods=["POST"])
@cross_origin()
def login_mentor():
    ROUTE_NAME = request.path

    data = request.json

    if "email" not in data:
        return parameter_error("Email tidak ada")
    if "password" not in data:
        return parameter_error("Password tidak ada")

    email = data["email"]
    password = data["password"]

    password_enc = hashlib.md5(password.encode(
        'utf-8')).hexdigest()  # Convert password to md5

    # mengecek data pada database
    dt = Data()
    query = "SELECT id_mentor, password, status_id FROM mentor WHERE email = %s "
    values = (email, )
    data_admin = dt.get_data(query, values)
    if len(data_admin) == 0:
        return defined_error("Email tidak di temukan")
    data_admin = data_admin[0]
    db_id_mentor = data_admin["id_mentor"]
    db_password = data_admin["password"]

    if password_enc != db_password:
        return defined_error("Wrong Password", "Invalid Credential", 401)

    role_desc = "mentor"

    jwt_payload = {
        "id_user": db_id_mentor,
        "role_desc": role_desc,
        "email": email
    }

    access_token = create_access_token(email, additional_claims=jwt_payload)

    # try:
    #     logs = secure_filename(strftime("%Y-%m-%d %H:%M:%S"))+" - "+ROUTE_NAME+" - id_user = "+str(db_id_user)+" - roles = "+str(role)+"\n"
    # except Exception as e:
    #     logs = secure_filename(strftime("%Y-%m-%d %H:%M:%S"))+" - "+ROUTE_NAME+" - id_user = NULL - roles = NULL\n"
    # tambahLogs(logs)

    return jsonify(access_token=access_token)

# fungsi error handle Halaman Tidak Ditemukan


@app.errorhandler(404)
@cross_origin()
def not_found(error):
    return make_response(jsonify({'error': 'Tidak Ditemukan', 'status_code': 404}), 404)

# fungsi error handle Halaman internal server error


@app.errorhandler(500)
@cross_origin()
def not_found(error):
    return make_response(jsonify({'error': 'Error Server', 'status_code': 500}), 500)

# endregion >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> ERROR HANDLER AREA <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<


# --------------------- REGISTER BLUEPRINT ------------------------

app.register_blueprint(user, url_prefix='/users')

# --------------------- END REGISTER BLUEPRINT ------------------------
