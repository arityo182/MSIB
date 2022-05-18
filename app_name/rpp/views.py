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

rpp = Blueprint('rpp', __name__,
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

# check endpoint
# API COURSE

# Menambah data course
@rpp.route("/insert_course", methods=["POST", "OPTIONS"])
@cross_origin()
def insert_course():
    try:
        dt = Data()
        data = request.json

        hasil = {"status": "berhasil tambah data course"}

        # Cek data
        if "nama_course" not in data:
            return parameter_error("Nama Course tidak ada")
        if "hari" not in data:
            return parameter_error("Hari tidak ada")
        if "jam_mulai" not in data:
            return parameter_error("Jam mulai tidak ada")
        if "jam_selesai" not in data:
            return parameter_error("Jam selesai tidak ada")
        if "kelas" not in data:
            return parameter_error("Kelas tidak ada")
        if "sks" not in data:
            return parameter_error("SKS tidak ada")
        if "kuota" not in data:
            return parameter_error("Limit tidak ada")

        id_course = None
        nama_course = data["nama_course"]
        hari = data["hari"]
        jam_mulai = data["jam_mulai"]
        jam_selesai = data["jam_selesai"]
        kelas = data["kelas"]
        sks = data["sks"]
        kuota = data["kuota"]

        # Masukan data ke database
        query = "INSERT into course (id_course, nama_course, hari, jam_mulai, jam_selesai, kelas, sks, kuota) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        values = (id_course, nama_course, hari, jam_mulai,
                  jam_selesai, kelas, sks, kuota)
        dt.insert_data_last_row(query, values)
        return make_response(hasil)

    except Exception as e:
        return bad_request(str(e))

# Menampilkan data course


@rpp.route("/get_data_course", methods=["GET"])
@cross_origin()
def get_data_course():

    try:
        dt = Data()
        query = "SELECT * FROM course"
        values = ()

        rowCount = dt.row_count(query, values)
        hasil = dt.get_data(query, values)
        hasil = {'data': hasil, 'status_code': 200, 'row_count': rowCount}
        return make_response(jsonify(hasil), 200)
    except Exception as e:
        return bad_request(str(e))

# update data course


@rpp.route("/update_data_course", methods=["PUT"])
@cross_origin()
def update_data_course():
    hasil = {"status": "Gagal update data course"}

    try:
        dt = Data()
        data = request.json

        # check email apakah sidah di lock
        if "id_course" not in data:
            return parameter_error("Id Course belum di pilih")

        id_course = data["id_course"]

        query = "UPDATE course SET id_course = %s "
        values = (id_course, )

        if "nama_course_ubah" in data:
            query += ", nama_course = %s "
            values += (data["nama_course_ubah"], )
        if "hari_ubah" in data:
            query += ", hari = %s "
            values += (data["hari_ubah"], )
        if "jam_mulai_ubah" in data:
            query += ", jam_mulai = %s "
            values += (data["jam_mulai_ubah"], )
        if "jam_mulai_ubah" in data:
            query += ", jam_mulai = %s "
            values += (data["jam_mulai_ubah"], )
        if "jam_selesai_ubah" in data:
            query += ", jam_selesai = %s "
            values += (data["jam_selesai_ubah"], )
        if "kelas_ubah" in data:
            query += ", kelas = %s "
            values += (data["kelas_ubah"], )
        if "sks_ubah" in data:
            query += ", sks = %s "
            values += (data["sks_ubah"], )

        query += " WHERE id_course = %s "
        values += (id_course, )
        dt.insert_data_last_row(query, values)
        hasil = {"status": "berhasil update data course"}

    except Exception as e:
        print("Error: " + str(e))

    return jsonify(hasil)

# Delete data course


@rpp.route("/delete_data_course/<id>", methods=["DELETE"])
def delete_data_course(id):
    hasil = {"status": "gagal hapus data course"}

    try:
        dt = Data()
        data = request.json

        query = "DELETE FROM course WHERE id_course = %s"
        values = (id, )
        dt.insert_data_last_row(query, values)
        hasil = {"status": "berhasil hapus data course"}
    except Exception as e:
        print("Error: " + str(e))

    return jsonify(hasil)

# API RPPT

# Menambah data rppt


@rpp.route("/insert_rppt", methods=["POST", "OPTIONS"])
@cross_origin()
def insert_rppt():
    try:
        dt = Data()
        data = request.json

        hasil = {"status": "berhasil tambah data rppt"}

        # Cek data
        if "id_mahasiswa" not in data:
            return parameter_error("Id Mahasiswa tidak ada")
        if "id_course" not in data:
            return parameter_error("Id Course tidak ada")
        if "skema" not in data:
            return parameter_error("skema tidak ada")

        status_verifikasi = False
        id_mahasiswa = data["id_mahasiswa"]
        id_course = data["id_course"]
        skema = data["skema"]

        # check id mahasiwa di database
        query_temp = "SELECT * FROM mahasiswa WHERE id_mahasiswa = %s "
        values_temp = (id_mahasiswa, )
        if len(dt.get_data(query_temp, values_temp)) == 0:
            return defined_error("Mahasiswa tidak ada di database")

        # check id course di database
        query_temp = "SELECT * FROM course WHERE id_course = %s "
        values_temp = (id_course, )
        if len(dt.get_data(query_temp, values_temp)) == 0:
            return defined_error("Course tidak ada di database")

        # Masukan data ke database
        query = "INSERT into rppt (id_mahasiswa, id_course, skema, status_verifikasi) VALUES (%s, %s, %s, %s)"
        values = (id_mahasiswa, id_course, skema, status_verifikasi)
        dt.insert_data_last_row(query, values)
        return make_response(hasil)

    except Exception as e:
        return bad_request(str(e))

# Menampilkan daftar mahasiswa dengan rppt belum approve


@rpp.route("/get_data_mahasiswa_wait_approval", methods=["GET"])
@cross_origin()
def get_data_mahasiswa_wait_approval():

    try:
        dt = Data()
        query = "SELECT DISTINCT(mahasiswa.id_mahasiswa), mahasiswa.nama_mahasiswa, mahasiswa.posisi FROM rppt INNER JOIN mahasiswa ON rppt.id_mahasiswa = mahasiswa.id_mahasiswa INNER JOIN course ON rppt.id_course = course.id_course WHERE rppt.status_verifikasi = 0"
        values = ()

        rowCount = dt.row_count(query, values)
        hasil = dt.get_data(query, values)
        hasil = {'data': hasil, 'status_code': 200, 'row_count': rowCount}
        return make_response(jsonify(hasil), 200)
    except Exception as e:
        return bad_request(str(e))

# Menampilkan rppt mahasiswa dengan id tertentu


@rpp.route("/get_rppt_mahasiswa/<id>", methods=["GET"])
@cross_origin()
def get_rppt_mahasiswa(id):

    try:
        dt = Data()
        query_course = "SELECT course.* FROM rppt INNER JOIN mahasiswa ON rppt.id_mahasiswa = mahasiswa.id_mahasiswa INNER JOIN course ON rppt.id_course = course.id_course WHERE mahasiswa.id_mahasiswa = %s"
        query_mahasiswa = "SELECT DISTINCT(mahasiswa.id_mahasiswa), mahasiswa.nama_mahasiswa, mahasiswa.asal_kampus, mahasiswa.posisi, rppt.skema FROM rppt INNER JOIN mahasiswa ON rppt.id_mahasiswa = mahasiswa.id_mahasiswa INNER JOIN course ON rppt.id_course = course.id_course WHERE mahasiswa.id_mahasiswa = %s"
        values = (id,)

        course = dt.get_data(query_course, values)
        mahasiswa = dt.get_data(query_mahasiswa, values)
        hasil = {'course': course, 'mahasiswa': mahasiswa}
        hasil = {'data': hasil, 'status_code': 200}
        return make_response(jsonify(hasil), 200)
    except Exception as e:
        return bad_request(str(e))

# update data course


@rpp.route("/approve_rppt", methods=["PUT"])
@cross_origin()
def approve_rppt():
    hasil = {"status": "Gagal update data course"}

    try:
        dt = Data()
        data = request.json

        # check id mahasiswa
        if "id_mahasiswa" not in data:
            return parameter_error("ID Mahasiswa belum ada")

        id_mahasiswa = data["id_mahasiswa"]

        query_id = "SELECT rppt.id_rppt FROM rppt INNER JOIN mahasiswa ON rppt.id_mahasiswa = mahasiswa.id_mahasiswa INNER JOIN course ON rppt.id_course = course.id_course WHERE mahasiswa.id_mahasiswa = %s"
        values_id = (id_mahasiswa,)

        id_rppt = dt.get_data(query_id, values_id)

        for rppt in id_rppt:
            query_update = "UPDATE rppt SET id_rppt = %s, status_verifikasi = %s WHERE id_rppt = %s"
            values_update = (rppt['id_rppt'], True, rppt['id_rppt'], )
            dt.insert_data_last_row(query_update, values_update)

        hasil = {"status": "berhasil approve RPPT"}

    except Exception as e:
        print("Error: " + str(e))

    return jsonify(hasil)

# Delete data rppt


@rpp.route("/delete_data_rppt/<id_mahasiswa>/<id_course>", methods=["DELETE"])
def delete_data_rppt(id_mahasiswa, id_course):
    hasil = {"status": "gagal hapus data course"}

    try:
        dt = Data()
        data = request.json

        query_id = "SELECT rppt.id_rppt FROM rppt INNER JOIN mahasiswa ON rppt.id_mahasiswa = mahasiswa.id_mahasiswa INNER JOIN course ON rppt.id_course = course.id_course WHERE mahasiswa.id_mahasiswa = %s AND course.id_course = %s"
        values_id = (id_mahasiswa, id_course, )

        id_rppt = dt.get_data(query_id, values_id)[0]['id_rppt']

        query = "DELETE FROM rppt WHERE id_rppt = %s"
        values = (id_rppt, )
        dt.insert_data_last_row(query, values)
        hasil = {"status": "berhasil hapus data rppt"}
    except Exception as e:
        print("Error: " + str(e))

    return jsonify(hasil)

# endregion ================================= MY PROFILE AREA ==========================================================================
