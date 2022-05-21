import re
from flask import Blueprint, jsonify, request, make_response, render_template
from flask import current_app as app
from flask_jwt_extended import get_jwt, jwt_required
from flask_cors import cross_origin
import jwt
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

project = Blueprint('project', __name__,
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

# insert project


@project.route('/insert_project', methods=['POST', 'OPTIONS'])
@jwt_required()
@cross_origin()
def insert_project():
    try:
        id_user = str(get_jwt()["id_admin"])
        role = str(get_jwt()["role_desc"])
        nama = str(get_jwt()["nama"])

        if role not in role_group_admin:
            return permission_failed()

        dt = Data()
        data = request.json
        hasil = {"status": "berhasil tambah data mentor"}

        # Cek data
        if "nama_Project" not in data:
            return parameter_error("Nama Project tidak di temukam")
        if "jadwal_mentoring" not in data:
            return parameter_error("Nama mentor tidak di temukan")
        if "jam" not in data:
            return parameter_error("jam  tidak di temukan")
        if "posisi_project" not in data:
            return parameter_error("Posisi project tidak de temukan")
        if "skema_project" not in data:
            return parameter_error("skema project tidak di temukan")
        if "jumlah_dibuka" not in data:
            return parameter_error("jumlah posisi di buka tidak di temukan")
        if "deskripsi"not in data:
            return parameter_error("deskripsi belum di isi")

        nama_project = data["nama_project"]
        jadwal_mentoring = data["jadwal_mentoring"]
        jam = data["jam"]
        posisi_project = data["posisi_project"]
        posisi_project_2 = data["posisi_project_2"]
        posisi_project_3 = data["posisi_project_3"]
        posisi_project_4 = data["posisi_project_4"]
        posisi_project_5 = data["posisi_project_5"]
        posisi_project_6 = data["posisi_project_6"]
        posisi_project_7 = data["posisi_project_7"]
        posisi_project_8 = data["posisi_project_8"]
        posisi_project_9 = data["posisi_project_9"]
        posisi_project_10 = data["posisi_project_10"]

        skema_project = data["skema_project"]
        skema_project_2 = data["skema_project_2"]
        skema_project_3 = data["skema_project_3"]
        skema_project_4 = data["skema_project_4"]
        skema_project_5 = data["skema_project_5"]
        skema_project_6 = data["skema_project_6"]
        skema_project_7 = data["skema_project_7"]
        skema_project_8 = data["skema_project_8"]
        skema_project_9 = data["skema_project_9"]
        skema_project_10 = data["skema_project_10"]

        jumlah_dibuka = data["jumlah_dibuka"]
        jumlah_dibuka_2 = data["jumlah_dibuka_2"]
        jumlah_dibuka_3 = data["jumlah_dibuka_3"]
        jumlah_dibuka_4 = data["jumlah_dibuka_4"]
        jumlah_dibuka_5 = data["jumlah_dibuka_5"]
        jumlah_dibuka_6 = data["jumlah_dibuka_6"]
        jumlah_dibuka_7 = data["jumlah_dibuka_7"]
        jumlah_dibuka_8 = data["jumlah_dibuka_8"]
        jumlah_dibuka_9 = data["jumlah_dibuka_9"]
        jumlah_dibuka_10 = data["jumlah_dibuka_10"]

        deskripsi = data["deskripsi"]

        # insert data ke tabel project
        query = "INSERT INTO project (nama_project, deskripsi, jadwal_mentoring, jam) VALUES (%s, %s, %s, %s)"
        values = (nama_project, deskripsi, jadwal_mentoring, jam)
        id_project = dt.insert_data_last_row(query, values)

        # insert ke tabel
        query2 = "INSERT INTO posisi_project (id_project, nama_posisi, skema_posisi, jumlah_dibuka)"
        values2 = [(id_project, posisi_project, skema_project, jumlah_dibuka),
                   (id_project, posisi_project_2, skema_project_2, jumlah_dibuka_2),
                   (id_project, posisi_project_3, skema_project_3, jumlah_dibuka_3),
                   (id_project, posisi_project_4, skema_project_4, jumlah_dibuka_4),
                   (id_project, posisi_project_5, skema_project_5, jumlah_dibuka_5),
                   (id_project, posisi_project_6, skema_project_6, jumlah_dibuka_6),
                   (id_project, posisi_project_7, skema_project_7, jumlah_dibuka_7),
                   (id_project, posisi_project_8, skema_project_8, jumlah_dibuka_8),
                   (id_project, posisi_project_9, skema_project_9, jumlah_dibuka_9),
                   (id_project, posisi_project_10, skema_project_10, jumlah_dibuka_10)]
        id_posisi = dt.insert_data_last_row(query2, values2)
        # Insert to table anggota project
        query2 = "INSERT INTO anggota_project (id_posisi) VALUES (%s)"
        values2 = (id_posisi, )
        dt.insert_data(query2, values2)
        return make_response({"status": "berhasil tambah project"}, 200)
    except Exception as e:
        return bad_request(str(e))

# mengambil project sesuai skema


@project.route('get_project/<posisi_sib>', methods=['GET'])
@jwt_required()
@cross_origin()
def get_project_hacker(posisi_sib):
    try:

        id_user = str(get_jwt()["id_user"])
        role = str(get_jwt()["role_desc"])
        email = str(get_jwt()["email"])

        if role not in role_group_all:
            return permission_failed()

        dt = Data()
        query = """SELECT a.id_project, a.nama_project, b.id_project, 
                b.skema_project AS posisi_project FROM project a LEFT JOIN posisi_project b
                ON a.id_project = b.id_project WHERE a.skema_project = %s"""
        values = (posisi_sib, )
        rowCount = dt.row_count(query, values)
        hasil = dt.get_data(query, values)
        hasil = {'data': hasil, 'status_code': 200, 'row_count': rowCount}
        return make_response(jsonify(hasil), 200)
    except Exception as e:
        return bad_request(str(e))

# get nama posisi


@project.route('/get_nama_posisi/<nama_project>', methods=['GET'])
@jwt_required()
@cross_origin()
def get_nama_posisi(nama_project):
    try:
        id_user = str(get_jwt()["id_user"])
        role = str(get_jwt()["role_desc"])
        email = str(get_jwt()["email"])

        if role not in role_group_all:
            return permission_failed()

        dt = Data()
        # menampilkan posisi project dan jumlah dibuka
        query = """SELECT a.id_project, a.nama_project, b.id_project,
                b.nama_posisi, b.jumlah_dibuka AS posisi_project FROM project a
                LEFT JOIN posisi_project b ON a.id_project = b.id_project WHERE a.nama_project = %s"""
        values = (nama_project, )
        hasil = dt.get_data(query, values)
        data_project = hasil[0]
        db_posisi = data_project["nama_posisi"]
        db_jumlah_dibuka = data_project["jumlah_dibuka"]

        # menampilkan posisi yang telah diambil
        # query2 = """SELECT DISTINCT(a.nama_posisi) a.id_posisi, b.id_posisi AS anggota_project
        #         FROM posisi_project a LEFT JOIN anggota_project b ON a.id_posisi = b.id_posisi WHERE
        #         a.nama_posisi = %s"""
        query2 = """SELECT a.nama_posisi a.id_posisi, b.id_posisi AS anggota_project
                FROM posisi_project a LEFT JOIN anggota_project b ON a.id_posisi = b.id_posisi WHERE
                a.nama_posisi = %s"""
        values2 = (db_posisi, )
        rowCount = dt.row_count(query2, values2)
        hasil = {'data': hasil, 'status_code': 200, 'row_count': rowCount}
        return make_response(jsonify(hasil), 200)
    except Exception as e:
        return bad_request(str(e))

# menmbahkan rppi


@project.route('/insert_rppi', methods=['POST', 'OPTIONS'])
@jwt_required()
@cross_origin()
def insert_rppi():
    try:

        id_user = str(get_jwt()["id_user"])
        role = str(get_jwt()["role_desc"])
        email = str(get_jwt()["email"])

        if role not in role_group_all:
            return permission_failed()

        data = request.json

        if "id_project" not in data:
            return parameter_error("id project tidak di temukan")
        if "posisi" not in data:
            return parameter_error("posisi tidak ditemukan")
        # if "skema" not in data:
        #     return parameter_error("skema tidak di temukan")

        id_project = data["id_project"]
        posisi = data["posisi"]
        # skema = data["skema"]
        skema = "Proyek Independen"

        dt = Data()
        query = "INSERT into rppi (id_project, id_mahasiswa, jabatan, skema) VALUES (%s. %s, %s, %S)"
        values = (id_project, id_user, posisi, skema)
        dt.insert_data_last_row(query, values)

        # belum jadi
        query_temp = "INSERT into anggota_project (id_mahasiswa) VALUES (%s)"
        values_temp = (id_user, )
        dt.insert_data(query_temp, values_temp)
        return make_response({"status": "berhasil tambah rppi"}, 200)

    except Exception as e:
        return bad_request(str(e))

# menampilkan rppi yang belum di approced


@project.route('/get_rppi_wait_approval', methods=['GET'])
@cross_origin()
@jwt_required()
def get_rppi_wait_approval():
    try:
        id_user = str(get_jwt()["id_user"])
        role = str(get_jwt()["role_desc"])

        if role not in role_group_admin:
            return permission_failed()

        dt = Data()
        query = "SELECT DISTINCT(mahasiswa.id_mahasiswa), mahasiswa.nama_mahasiswa FROM rppi INNER JOIN mahasiswa ON rppt.id_mahasiswa = mahasiswa.id_mahasiswa WHERE rppi.status_verifikasi = 0"
        values = ()

        rowCount = dt.row_count(query, values)
        hasil = dt.get_data(query, values)
        hasil = {'data': hasil, 'status_code': 200, 'row_count': rowCount}
        return make_response(jsonify(hasil), 200)
    except Exception as e:
        return bad_request(str(e))

# rppi yang belum di approved


@project.route('/get_all_wait_approval', methods=['GET'])
@cross_origin()
@jwt_required()
def get_all_wait_approval():
    try:
        id_user = str(get_jwt()["id_user"])
        role = str(get_jwt()["role_desc"])

        if role not in role_group_admin:
            return permission_failed()

        dt = Data()
        query = """SELECT a.nama_mahasiswa, a.posisi, b.jabatan AS rppi, 
                c.nama_project AS project FROM mahasiswa a LEFT JOIN rppi b
                ON a.id_mahasiswa = b.id_mahasiswa LEFT JOIN project c ON b.id_project = c.id_project
                WHERE status_verifikasi = 0"""
        values = ()
        rowCount = dt.row_count(query, values)
        hasil = dt.get_data(query, values)
        hasil = {'data': hasil, 'status_code': 200, 'row_count': rowCount}
        return make_response(jsonify(hasil), 200)
    except Exception as e:
        return bad_request(str(e))

# rppi yang sudah di approved


@project.route('/get_all_approval', methods=['GET'])
@cross_origin()
@jwt_required()
def get_all_approval():
    try:
        id_user = str(get_jwt()["id_user"])
        role = str(get_jwt()["role_desc"])

        if role not in role_group_admin:
            return permission_failed()

        dt = Data()
        query = """SELECT a.nama_mahasiswa, a.posisi, b.jabatan AS rppi, 
                c.nama_project AS project FROM mahasiswa a LEFT JOIN rppi b
                ON a.id_mahasiswa = b.id_mahasiswa LEFT JOIN project c ON b.id_project = c.id_project
                WHERE status_verifikasi = 11"""
        values = ()
        rowCount = dt.row_count(query, values)
        hasil = dt.get_data(query, values)
        hasil = {'data': hasil, 'status_code': 200, 'row_count': rowCount}
        return make_response(jsonify(hasil), 200)
    except Exception as e:
        return bad_request(str(e))

# Edit rppi
# Bingung


# delete rppi
@project.route('/delete_rppi/<id_project>/<id_mahasiswa>', methods=['DELETE'])
@cross_origin()
@jwt_required()
def delete_rppi(id_project, id_mahasiswa):
    try:
        id_user = str(get_jwt()["id_user"])
        role = str(get_jwt()["role_desc"])

        if role not in role_group_admin:
            return permission_failed()

        dt = Data()
        data = request.json

        query = """SELECT a. * FROM rppi a WHERE id_project = %s AND id_mahasiswa = %s"""
        values = (id_project, id_mahasiswa)
        id_rppi = dt.get_data(query, values)[0]['id_rppi']

        query2 = "DELETE FROM rppi WHERE id_rppt = %s"
        values2 = (id_rppi, )
        dt.insert_data_last_row(query2, values2)

        # delete anggota_project
        query3 = "DELETE FROM anggota_project WHERE id_rppt = %s"
        values4 = (id_mahasiswa, )
        dt.insert_data_last_row(query3, values4)

        hasil = {"status": "berhasil hapus data rpp1"}
        return jsonify(hasil)
    except Exception as e:
        print("Error: " + str(e))

# mom


@project.route('/insert_mom', methods=['POST', 'OPTIONS'])
@jwt_required()
@cross_origin()
def insert_mom():
    ROUTE_NAME = request.path

    try:
        id_user = str(get_jwt()["id_user"])
        role = str(get_jwt()["role_desc"])
        email = str(get_jwt()["email"])

        if role not in role_group_all:
            return permission_failed()

        dt = Data()
        data = request.json

        if "dokumen_upload" not in data:
            return parameter_error("dokumen tidak ditemukan")

        dokumen_upload = data["dokumen_data"]

        query = "INSERT INTO mom (id_mentor, dokumen) VALUES (%s, %s)"
        values = (id_user, dokumen_upload)
        dt.insert_data(query, values)
        try:
            logs = secure_filename(strftime("%Y-%m-%d %H:%M:%S"))+" - "+ROUTE_NAME + \
                " - user_id = "+str(id_user)+" - roles = "+str(role)+"\n"
        except Exception as e:
            logs = secure_filename(strftime(
                "%Y-%m-%d %H:%M:%S"))+" - "+ROUTE_NAME+" - user_id = NULL - roles = NULL\n"
            # tambahLogs(logs)
        return make_response(jsonify({'status_code': 200, 'description': "Berhasil"}), 200)
    except Exception as e:
        return bad_request(str(e))
