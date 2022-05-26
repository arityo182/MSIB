import re
from urllib import response
from flask import Blueprint, jsonify, request, make_response, render_template, send_file
from flask import current_app as app
from flask_jwt_extended import get_jwt, jwt_required
from flask_cors import cross_origin
import jwt
from urllib3 import Retry
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
import pdfkit
from PIL import Image
import io



from .models import Data


#now = datetime.datetime.now()

project = Blueprint('project', __name__,
                    static_folder='../../upload/foto_user', static_url_path="/media")

# region ================================= FUNGSI-FUNGSI AREA ==========================================================================

#role user
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

#get all project name and id
@project.route('/get_project_no_mentor',methods=['GET'])
@cross_origin()
@jwt_required()
def get_all_project_name():
    try:
        id_user = str(get_jwt()["id_user"])
        role = str(get_jwt()["role_desc"])
        username = str(get_jwt()["username"])

        if role not in role_group_admin:
            return permission_failed()

        dt = Data()

        #menmpilkan data project 
        query = """SELECT a.id_project, a.nama_project FROM project a LEFT JOIN
                mentor_project b ON a.id_project = b.id_project WHERE b.id_mentor IS NULL"""
        values = ()
        hasil = dt.get_data(query, values)[0]["nama_project"]
        rowCount = dt.row_count(query, values)
        hasil = {'data': hasil, 'status_code': 200, 'row_count': rowCount}
        return make_response(jsonify(hasil), 200)
    except Exception as e:
        return bad_request(str(e))

#insert project
@project.route('/insert_project', methods=['POST', 'OPTIONS'])
@jwt_required()
@cross_origin()
def insert_project():
    try:
        id_user = str(get_jwt()["id_user"])
        role = str(get_jwt()["role_desc"])
        username = str(get_jwt()["username"])

        if role not in role_group_admin:
            return permission_failed()

        dt = Data()
        data = request.json

        # Cek data
        if "nama_project" not in data:
            return parameter_error("nama_project tidak di temukam")
        if "jadwal_mentoring" not in data:
            return parameter_error("jadwal_mentoring tidak di temukan")
        if "jam" not in data:
            return parameter_error("jam  tidak di temukan")
        if "posisi_project" not in data:
            return parameter_error("posisi_project tidak de temukan")
        # if "skema_project" not in data:
        #     return parameter_error("skema_project tidak di temukan")
        # if "jumlah_dibuka" not in data:
        #     return parameter_error("jumlah_dibuka di buka tidak di temukan")
        if "deskripsi"not in data:
            return parameter_error("deskripsi belum di isi")
        if "nama_mentor" not in data:
            return parameter_error("nama_mentor tidak ditemukan")
        if "sks" not in data:
            return parameter_error("sks tidak di temukan")

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
        nama_mentor = data["nama_mentor"]
        sks = data["sks"]

        # insert data ke tabel project
        query = "INSERT INTO project (nama_project, deskripsi, jadwal_mentoring, jam, sks) VALUES (%s, %s, %s, %s, %s)"
        values = (nama_project, deskripsi, jadwal_mentoring, jam, sks)
        id_project = dt.insert_data_last_row(query, values)

        #insert ke project
        if "posisi_project_10":
            if "skema_project_10" not in data:
                return parameter_error("skema_project_9 tidak di temukan")
            if "jumlah_dibuka_10" not in data:
                return parameter_error("jumlah_dibuka_9 tidak di temukan")
            # insert ke tabel
            # query2 = "INSERT INTO posisi_project (id_project, nama_posisi, skema_posisi, jumlah_dibuka) VALUES (%s, %s, %s, %s)"
            #values2 = (id_project, posisi_project, skema_project, jumlah_dibuka)
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
            query2 = "INSERT INTO posisi_project (id_project, nama_posisi, skema_posisi, jumlah_dibuka) VALUES " + ",".join("(%s, %s, %s, %s)" for _ in values2)
            flattened_values = [item for sublist in values2 for item in sublist ]
            #values2= ', '.join(map(str,str,int, rows))
            id_posisi = dt.insert_data_last_row(query2, flattened_values)
            # Insert to table anggota project (gk tau dipakai gk)
            query3 = "INSERT INTO anggota_project (id_posisi) VALUES (%s)"
            values3 = (id_posisi, )
            dt.insert_data(query3,values3)

            #insert data mentor dan project ke mentor_project
            query4 = "INSERT INTO mentor_project (id_project, id_mentor) VALUES (%s, %s)"
            values4 = (id_project, nama_mentor)
            dt.insert_data(query4, values4)

            hasil = {"status": "berhasil tambah data project"}
            return make_response(jsonify({'status_code': 200, 'description': hasil}), 200)
        elif "posisi_project_9" in data:
            if "skema_project_9" not in data:
                return parameter_error("skema_project_9 tidak di temukan")
            if "jumlah_dibuka_9" not in data:
                return parameter_error("jumlah_dibuka_9 tidak di temukan")
            values2 = [(id_project, posisi_project, skema_project, jumlah_dibuka),
                   (id_project, posisi_project_2, skema_project_2, jumlah_dibuka_2),
                   (id_project, posisi_project_3, skema_project_3, jumlah_dibuka_3),
                   (id_project, posisi_project_4, skema_project_4, jumlah_dibuka_4),
                   (id_project, posisi_project_5, skema_project_5, jumlah_dibuka_5),
                   (id_project, posisi_project_6, skema_project_6, jumlah_dibuka_6),
                   (id_project, posisi_project_7, skema_project_7, jumlah_dibuka_7),
                   (id_project, posisi_project_8, skema_project_8, jumlah_dibuka_8),
                   (id_project, posisi_project_9, skema_project_9, jumlah_dibuka_9)]
            query2 = "INSERT INTO posisi_project (id_project, nama_posisi, skema_posisi, jumlah_dibuka) VALUES " + ",".join("(%s, %s, %s, %s)" for _ in values2)
            id_posisi = dt.insert_data_last_row(query2, values2)
            # Insert to table anggota project (gk tau dipakai gk)
            query3 = "INSERT INTO anggota_project (id_posisi) VALUES (%s)"
            values3 = (id_posisi, )
            dt.insert_data(query3,values3)

            #insert data mentor dan project ke mentor_project
            query4 = "INSERT INTO mentor_project (id_project, id_mentor) VALUES (%s, %s)"
            values4 = (id_project, nama_mentor)
            dt.insert_data(query4, values4)

            hasil = {"status": "berhasil tambah data project"}
            return make_response(jsonify({'status_code': 200, 'description': hasil}), 200)
        elif "posisi_project_8" in data:
            if "skema_project_8" not in data:
                return parameter_error("skema_project_8 tidak di temukan")
            if "jumlah_dibuka_8" not in data:
                return parameter_error("jumlah_dibuka_8 tidak di temukan")
            values2 = [(id_project, posisi_project, skema_project, jumlah_dibuka),
                   (id_project, posisi_project_2, skema_project_2, jumlah_dibuka_2),
                   (id_project, posisi_project_3, skema_project_3, jumlah_dibuka_3),
                   (id_project, posisi_project_4, skema_project_4, jumlah_dibuka_4),
                   (id_project, posisi_project_5, skema_project_5, jumlah_dibuka_5),
                   (id_project, posisi_project_6, skema_project_6, jumlah_dibuka_6),
                   (id_project, posisi_project_7, skema_project_7, jumlah_dibuka_7),
                   (id_project, posisi_project_8, skema_project_8, jumlah_dibuka_8)]
            query2 = "INSERT INTO posisi_project (id_project, nama_posisi, skema_posisi, jumlah_dibuka) VALUES " + ",".join("(%s, %s, %s, %s)" for _ in values2)
            id_posisi = dt.insert_data_last_row(query2, values2)
            # Insert to table anggota project (gk tau dipakai gk)
            query3 = "INSERT INTO anggota_project (id_posisi) VALUES (%s)"
            values3 = (id_posisi, )
            dt.insert_data(query3,values3)

            #insert data mentor dan project ke mentor_project
            query4 = "INSERT INTO mentor_project (id_project, id_mentor) VALUES (%s, %s)"
            values4 = (id_project, nama_mentor)
            dt.insert_data(query4, values4)

            hasil = {"status": "berhasil tambah data project"}
            return make_response(jsonify({'status_code': 200, 'description': hasil}), 200)
        elif "posisi_project_7" in data:
            if "skema_project_7" not in data:
                return parameter_error("skema_project_7 tidak di temukan")
            if "jumlah_dibuka_7" not in data:
                return parameter_error("jumlah_dibuka_7 tidak di temukan")
            values2 = [(id_project, posisi_project, skema_project, jumlah_dibuka),
                   (id_project, posisi_project_2, skema_project_2, jumlah_dibuka_2),
                   (id_project, posisi_project_3, skema_project_3, jumlah_dibuka_3),
                   (id_project, posisi_project_4, skema_project_4, jumlah_dibuka_4),
                   (id_project, posisi_project_5, skema_project_5, jumlah_dibuka_5),
                   (id_project, posisi_project_6, skema_project_6, jumlah_dibuka_6),
                   (id_project, posisi_project_7, skema_project_7, jumlah_dibuka_7)]
            query2 = "INSERT INTO posisi_project (id_project, nama_posisi, skema_posisi, jumlah_dibuka) VALUES " + ",".join("(%s, %s, %s, %s)" for _ in values2)
            id_posisi = dt.insert_data_last_row(query2, values2)
            # Insert to table anggota project (gk tau dipakai gk)
            query3 = "INSERT INTO anggota_project (id_posisi) VALUES (%s)"
            values3 = (id_posisi, )
            dt.insert_data(query3,values3)

            #insert data mentor dan project ke mentor_project
            query4 = "INSERT INTO mentor_project (id_project, id_mentor) VALUES (%s, %s)"
            values4 = (id_project, nama_mentor)
            dt.insert_data(query4, values4)

            hasil = {"status": "berhasil tambah data project"}
            return make_response(jsonify({'status_code': 200, 'description': hasil}), 200)
        elif "posisi_project_6" in data:
            if "skema_project_6" not in data:
                return parameter_error("skema_project_6 tidak di temukan")
            if "jumlah_dibuka_6" not in data:
                return parameter_error("jumlah_dibuka_6 tidak di temukan")
            values2 = [(id_project, posisi_project, skema_project, jumlah_dibuka),
                   (id_project, posisi_project_2, skema_project_2, jumlah_dibuka_2),
                   (id_project, posisi_project_3, skema_project_3, jumlah_dibuka_3),
                   (id_project, posisi_project_4, skema_project_4, jumlah_dibuka_4),
                   (id_project, posisi_project_5, skema_project_5, jumlah_dibuka_5),
                   (id_project, posisi_project_6, skema_project_6, jumlah_dibuka_6)]
            query2 = "INSERT INTO posisi_project (id_project, nama_posisi, skema_posisi, jumlah_dibuka) VALUES " + ",".join("(%s, %s, %s, %s)" for _ in values2)
            id_posisi = dt.insert_data_last_row(query2, values2)
            # Insert to table anggota project (gk tau dipakai gk)
            query3 = "INSERT INTO anggota_project (id_posisi) VALUES (%s)"
            values3 = (id_posisi, )
            dt.insert_data(query3,values3)

            #insert data mentor dan project ke mentor_project
            query4 = "INSERT INTO mentor_project (id_project, id_mentor) VALUES (%s, %s)"
            values4 = (id_project, nama_mentor)
            dt.insert_data(query4, values4)

            hasil = {"status": "berhasil tambah data project"}
            return make_response(jsonify({'status_code': 200, 'description': hasil}), 200)
        elif "posisi_project_5" in data:
            if "skema_project_5" not in data:
                return parameter_error("skema_project_5 tidak di temukan")
            if "jumlah_dibuka_5" not in data:
                return parameter_error("jumlah_dibuka_5 tidak di temukan")
            values2 = [(id_project, posisi_project, skema_project, jumlah_dibuka),
                   (id_project, posisi_project_2, skema_project_2, jumlah_dibuka_2),
                   (id_project, posisi_project_3, skema_project_3, jumlah_dibuka_3),
                   (id_project, posisi_project_4, skema_project_4, jumlah_dibuka_4),
                   (id_project, posisi_project_5, skema_project_5, jumlah_dibuka_5)]
            query2 = "INSERT INTO posisi_project (id_project, nama_posisi, skema_posisi, jumlah_dibuka) VALUES " + ",".join("(%s, %s, %s, %s)" for _ in values2)
            id_posisi = dt.insert_data_last_row(query2, values2)
            # Insert to table anggota project (gk tau dipakai gk)
            query3 = "INSERT INTO anggota_project (id_posisi) VALUES (%s)"
            values3 = (id_posisi, )
            dt.insert_data(query3,values3)

            #insert data mentor dan project ke mentor_project
            query4 = "INSERT INTO mentor_project (id_project, id_mentor) VALUES (%s, %s)"
            values4 = (id_project, nama_mentor)
            dt.insert_data(query4, values4)

            hasil = {"status": "berhasil tambah data project"}
            return make_response(jsonify({'status_code': 200, 'description': hasil}), 200)
        elif "posisi_project_4" in data:
            if "skema_project_4" not in data:
                return parameter_error("skema_project_4 tidak di temukan")
            if "jumlah_dibuka_4" not in data:
                return parameter_error("jumlah_dibuka_4 tidak di temukan")
            values2 = [(id_project, posisi_project, skema_project, jumlah_dibuka),
                   (id_project, posisi_project_2, skema_project_2, jumlah_dibuka_2),
                   (id_project, posisi_project_3, skema_project_3, jumlah_dibuka_3),
                   (id_project, posisi_project_4, skema_project_4, jumlah_dibuka_4)]
            query2 = "INSERT INTO posisi_project (id_project, nama_posisi, skema_posisi, jumlah_dibuka) VALUES " + ",".join("(%s, %s, %s, %s)" for _ in values2)
            id_posisi = dt.insert_data_last_row(query2, values2)
            # Insert to table anggota project (gk tau dipakai gk)
            query3 = "INSERT INTO anggota_project (id_posisi) VALUES (%s)"
            values3 = (id_posisi, )
            dt.insert_data(query3,values3)

            #insert data mentor dan project ke mentor_project
            query4 = "INSERT INTO mentor_project (id_project, id_mentor) VALUES (%s, %s)"
            values4 = (id_project, nama_mentor)
            dt.insert_data(query4, values4)

            hasil = {"status": "berhasil tambah data project"}
            return make_response(jsonify({'status_code': 200, 'description': hasil}), 200)
        elif "posisi_project_3" in data:
            if "skema_project_3" not in data:
                return parameter_error("skema_project_3 tidak di temukan")
            if "jumlah_dibuka_3" not in data:
                return parameter_error("jumlah_dibuka_3 tidak di temukan")
            values2 = [(id_project, posisi_project, skema_project, jumlah_dibuka),
                   (id_project, posisi_project_2, skema_project_2, jumlah_dibuka_2),
                   (id_project, posisi_project_3, skema_project_3, jumlah_dibuka_3)]
            query2 = "INSERT INTO posisi_project (id_project, nama_posisi, skema_posisi, jumlah_dibuka) VALUES " + ",".join("(%s, %s, %s, %s)" for _ in values2)
            id_posisi = dt.insert_data_last_row(query2, values2)
            # Insert to table anggota project (gk tau dipakai gk)
            query3 = "INSERT INTO anggota_project (id_posisi) VALUES (%s)"
            values3 = (id_posisi, )
            dt.insert_data(query3,values3)

            #insert data mentor dan project ke mentor_project
            query4 = "INSERT INTO mentor_project (id_project, id_mentor) VALUES (%s, %s)"
            values4 = (id_project, nama_mentor)
            dt.insert_data(query4, values4)

            hasil = {"status": "berhasil tambah data project"}
            return make_response(jsonify({'status_code': 200, 'description': hasil}), 200)
        elif "posisi_project_2" in data:
            if "skema_project_2" not in data:
                return parameter_error("skema_project_2 tidak di temukan")
            if "jumlah_dibuka_2" not in data:
                return parameter_error("jumlah_dibuka_2 tidak di temukan")
            
            values2 = [(id_project, posisi_project, skema_project, jumlah_dibuka),
                   (id_project, posisi_project_2, skema_project_2, jumlah_dibuka_2)]
            query2 = "INSERT INTO posisi_project (id_project, nama_posisi, skema_posisi, jumlah_dibuka) VALUES " + ",".join("(%s, %s, %s, %s)" for _ in values2)
            id_posisi = dt.insert_data_last_row(query2, values2)
            # Insert to table anggota project (gk tau dipakai gk)
            query3 = "INSERT INTO anggota_project (id_posisi) VALUES (%s)"
            values3 = (id_posisi, )
            dt.insert_data(query3,values3)

            #insert data mentor dan project ke mentor_project
            query4 = "INSERT INTO mentor_project (id_project, id_mentor) VALUES (%s, %s)"
            values4 = (id_project, nama_mentor)
            dt.insert_data(query4, values4)

            hasil = {"status": "berhasil tambah data project"}
            return make_response(jsonify({'status_code': 200, 'description': hasil}), 200)
        elif "posisi_project" in data:
            if "skema_project" not in data:
                return parameter_error("skema_project tidak ditemukan")
            if "jumlah_dibuka" not in data:
                return parameter_error("jumlah_dibuka tidak di temukan")
            values2 = (id_project, posisi_project, skema_project, jumlah_dibuka)
            query2 = "INSERT INTO posisi_project (id_project, nama_posisi, skema_posisi, jumlah_dibuka) VALUES (%s, %s, %s, %s)"
            id_posisi = dt.insert_data_last_row(query2, values2)
            # Insert to table anggota project (gk tau dipakai gk)
            query3 = "INSERT INTO anggota_project (id_posisi) VALUES (%s)"
            values3 = (id_posisi, )
            dt.insert_data(query3,values3)

            #insert data mentor dan project ke mentor_project
            query4 = "INSERT INTO mentor_project (id_project, id_mentor) VALUES (%s, %s)"
            values4 = (id_project, nama_mentor)
            dt.insert_data(query4, values4)

            hasil = {"status": "berhasil tambah data project"}
            return make_response(jsonify({'status_code': 200, 'description': hasil}), 200)
        else:
            return defined_error("Error add project",401)

    except Exception as e:
        return bad_request(str(e))


#mengambil project sesuai skema
@project.route('get_project/<posisi_sib>', methods=['GET'])
@jwt_required()
@cross_origin()
def get_project_hacker(posisi_sib):
    try:

        id_user = str(get_jwt()["id_user"])
        role = str(get_jwt()["role_desc"])
        email = str(get_jwt()["email"])

        if role not in role_mahasiswa:
            return permission_failed()

        #cek project name berdasarkan posisi
        dt = Data()
        query = """SELECT a.id_project, a.nama_project, b.id_project, 
                b.skema_posisi AS posisi_project FROM project a LEFT JOIN posisi_project b
                ON a.id_project = b.id_project WHERE b.skema_posisi = %s"""
        values = (posisi_sib, )
        rowCount = dt.row_count(query, values)
        hasil = dt.get_data(query, values)
        hasil = {'data': hasil, 'status_code': 200, 'row_count': rowCount}
        return make_response(jsonify(hasil), 200)
    except Exception as e:
        return bad_request(str(e))

#get nama posisi
@project.route('/get_nama_posisi/<nama_project>', methods=['GET'])
@jwt_required()
@cross_origin()
def get_nama_posisi(nama_project):
    try:
        id_user = str(get_jwt()["id_user"])
        role = str(get_jwt()["role_desc"])
        email = str(get_jwt()["email"])

        if role not in role_mahasiswa:
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
 

        # menampilkan posisi yang telah diambil
        # query2 = """SELECT a.*, COUNT(a.id_mahasiswa) FROM anggota_project a LEFT JOIN 
        #         posisi_project b ON a.id_posisi = b.id_posisi WHERE
        #         b.nama_posisi = %s"""
        # # query2 = """SELECT a.nama_posisi, a.id_posisi, b.id_posisi AS anggota_project
        # #         FROM posisi_project a LEFT JOIN anggota_project b ON a.id_posisi = b.id_posisi WHERE
        # #         a.nama_posisi = %s"""
        # values2 = (db_posisi, )

        #menampilkan project yang telah di approve admin
        query2 = """SELECT COUNT(*) as "posisi yang telah di ambil (approved)" FROM rppi
                WHERE status_verifikasi = 11 AND jabatan = %s"""
        values2 = (db_posisi, )
        rowCount = dt.get_data(query2, values2)
        hasil = {'data': hasil, 'status_code': 200, 'sudah ambil posisi': rowCount}
        return make_response(jsonify(hasil), 200)
    except Exception as e:
        return bad_request(str(e))


#get jumlah sks nama 

#menmbahkan rppi
@project.route('/insert_rppi', methods=['POST', 'OPTIONS'])
@jwt_required()
@cross_origin()
def insert_rppi():
    try:

        id_user = str(get_jwt()["id_user"])
        role = str(get_jwt()["role_desc"])
        email = str(get_jwt()["email"])

        if role not in role_mahasiswa:
            return permission_failed()

        data = request.json

        if "id_project" not in data:
            return parameter_error("id_projecttidak di temukan")
        if "posisi" not in data:
            return parameter_error("posisi tidak ditemukan")
        # if "skema" not in data:
        #     return parameter_error("skema tidak di temukan")

        id_project = data["id_project"]
        posisi = data["posisi"]
        # skema = data["skema"]
        skema = "Proyek Independen"

        dt = Data()

        #check id mahasiswa sudah mengajukan belum
        query2 = "SELECT id_mahasiswa FROM rppi WHERE id_mahasiswa = %s "
        values2 = (id_user, )
        data_rppi= dt.get_data(query2, values2)
        if len(data_rppi) != 0:
            return make_response(jsonify({'status_code' : 200, 'description': 'anda telah mengajukan rppi silakan tunggu verifikasi'}))


        query3 = """SELECT COUNT(*) as "jumlah" FROM rppi WHERE id_project = %s AND jabatan = %s AND status_verifikasi = 11"""
        values3 = (id_project, posisi)
        hasil_data_approved = dt.get_data(query3, values3)[0]["jumlah"]

        query4 = """SELECT jumlah_dibuka FROM posisi_project WHERE id_project = %s AND nama_posisi = %s"""
        values4 = (id_project, posisi)
        jumlah_dibuka = dt.get_data(query4, values4)[0]["jumlah_dibuka"]
        if hasil_data_approved > int(jumlah_dibuka):
            return make_response({"status": "gagal tambah rppi melebihi kuota","jumlah_diterima" : hasil_data_approved}, 200)
        else:
            query2 = """SELECT a.id_posisi FROM anggota_project a LEFT JOIN 
                posisi_project b ON a.id_posisi = b.id_posisi WHERE
                b.nama_posisi = %s """
            # query2 = """SELECT a.nama_posisi, a.id_posisi, b.id_posisi AS anggota_project
            #         FROM posisi_project a LEFT JOIN anggota_project b ON a.id_posisi = b.id_posisi WHERE
            #         a.nama_posisi = %s"""
            values2 = (posisi, )
            hasil = dt.get_data(query2, values2)
            data_posisi = hasil[0]
            data_id = data_posisi["id_posisi"]

            query = "INSERT into rppi (id_project, id_mahasiswa, jabatan, skema) VALUES (%s, %s, %s, %s)"
            values = (id_project, id_user, posisi, skema)
            dt.insert_data(query, values)

            # belum jadi
            # query_temp = "UPDATE anggota_project SET id_mahasiswa = %s WHERE id_posisi = %s "
            # values_temp = (id_user, data_id)
            # dt.insert_data(query_temp, values_temp)
            return make_response({"status": "berhasil tambah rppi","jumlah_diterima" : hasil_data_approved,"jumlah_dibuka" : jumlah_dibuka}, 200)

    except Exception as e:
        return bad_request(str(e))

#menampilkan rppi yang belum di approced
@project.route('/get_rppi_wait_approval', methods=['GET'])
@cross_origin()
@jwt_required()
def get_rppi_wait_approval():
    try:
        id_user = str(get_jwt()["id_user"])
        role = str(get_jwt()["role_desc"])
        username = str(get_jwt()["username"])

        if role not in role_group_admin:
            return permission_failed()
        
        #cek jumlah rppi yang belum di approve
        dt = Data()
        query = """SELECT COUNT(*) as "jumlah belum di approved" FROM rppi
                WHERE status_verifikasi = 0"""
        values = ()

        rowCount = dt.row_count(query, values)
        hasil = dt.get_data(query, values)
        hasil = {'data': hasil, 'status_code': 200, 'row_count': rowCount}
        return make_response(jsonify(hasil), 200)
    except Exception as e:
        return bad_request(str(e))

#rppi yang belum di approved
@project.route('/get_all_rppi_wait_approval', methods=['GET'])
@cross_origin()
@jwt_required()
def get_all__rppi_wait_approval():
    try:
        id_user = str(get_jwt()["id_user"])
        role = str(get_jwt()["role_desc"])
        username = str(get_jwt()["username"])

        if role not in role_group_admin:
            return permission_failed()

        #menampilkan semua data yang belum di approve
        dt = Data()
        query = """SELECT a.nama_mahasiswa, a.posisi, b.id_rppi, b.jabatan AS jabatan, 
                c.nama_project AS proyek FROM mahasiswa a LEFT JOIN rppi b
                ON a.id_mahasiswa = b.id_mahasiswa LEFT JOIN project c ON b.id_project = c.id_project
                WHERE status_verifikasi = 0"""
        values = ()
        rowCount = dt.row_count(query, values)
        hasil = dt.get_data(query, values)
        hasil = {'data': hasil, 'status_code': 200, 'row_count': rowCount}
        return make_response(jsonify(hasil), 200)
    except Exception as e:
        return bad_request(str(e))

#rppi yang sudah di approved
@project.route('/get_all_rppi_approval', methods=['GET'])
@cross_origin()
@jwt_required()
def get_all_approval():
    try:

        id_user = str(get_jwt()["id_user"])
        role = str(get_jwt()["role_desc"])
        username = str(get_jwt()["username"])

        if role not in role_group_admin:
            return permission_failed()

        dt = Data()
        query = """SELECT a.nama_mahasiswa, a.posisi, b.id_rppi, b.jabatan AS jabatan, 
                c.nama_project AS nama_project FROM mahasiswa a LEFT JOIN rppi b
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

#approve rppi
@project.route('/approve_rppi/<id_rppi>',methods=['PUT','OPTIONS'])
@cross_origin()
@jwt_required()
def approve_rppi(id_rppi):
    try:
        id_user = str(get_jwt()["id_user"])
        role = str(get_jwt()["role_desc"])
        username = str(get_jwt()["username"])

        if role not in role_group_admin:
            return permission_failed()
        
        dt = Data()
        
        query_temp = " SELECT id_rppi FROM rppi WHERE id_rppi = %s "
        values_temp = (id_rppi, )
        data_rppi = dt.get_data(query_temp, values_temp)
        if len(data_rppi) == 0:
            return defined_error("Gagal, data tidak ditemukan")
        
        query = """UPDATE rppi SET status_verifikasi = 11 WHERE id_rppi = %s """
        values = (id_rppi, )
        dt.insert_data_last_row(query, values)
        hasil = {"status": "berhasil approve data rppi"}
        return make_response(jsonify({'status_code': 200, 'description': hasil}), 200)
    except Exception as e:
        return bad_request(str(e))

#delete data rppi jika sudah melebihi kuota
# @project.route('/delete_rppi_over_kuota', methods=['DELETE'])
# @cross_origin()
# @jwt_required()
# def delete_rppi_over_kuota():
#     try:
#         id_user = str(get_jwt()["id_user"])
#         role = str(get_jwt()["role_desc"])
#         username = str(get_jwt()["username"])

#         if role not in role_group_admin:
#             return permission_failed()
        
#         dt = Data()

#         query_temp = """SELECT id.project, jabatan FROM rppi"""


#delete rppi
@project.route('/delete_rppi/<id_rppi>', methods=['DELETE'])
@cross_origin()
@jwt_required()
def delete_rppi(id_rppi):
    try:
        id_user = str(get_jwt()["id_user"])
        role = str(get_jwt()["role_desc"])
        username = str(get_jwt()["username"])

        if role not in role_group_admin:
            return permission_failed()

        dt = Data()
        data = request.json


        query2 = "DELETE FROM rppi WHERE id_rppi = %s"
        values2 = (id_rppi, )
        dt.insert_data(query2, values2)
        hasil = {"status": "berhasil hapus data rpp1"}
        return make_response(jsonify({'status_code': 200, 'description': hasil}), 200)
    except Exception as e:
        return bad_request(str(e))

#check status rppi dan menampilkan sks (belum jadi)
@project.route('/check_status_rppi', methods=['GET'])
@cross_origin()
@jwt_required()
def check_status_rppi_():
    try:
        id_user = str(get_jwt()["id_user"])
        role = str(get_jwt()["role_desc"])
        email = str(get_jwt()["email"])

        if role not in role_mahasiswa:
            return permission_failed()
        
        dt = Data()

        #check id mahasiswa
        query = "SELECT id_mahasiswa FROM mahasiswa WHERE id_mahasiswa = %s "
        values = (id_user, )
        data_mahasiswa = dt.get_data(query, values)
        if len(data_mahasiswa) == 0:
            return defined_error("id mahasiswa tidak di temukan", 401)
        
        #check id mahasiswa sudah mengajukan belum
        query2 = """ SELECT a.* FROM rppi a WHERE id_mahasiswa = %s """
        values2 = (id_user, )
        data_rppi= dt.get_data(query2, values2)
        if len(data_rppi) == 0:
            return make_response(jsonify({'status_code' : 200, 'description': 'belum mengajukan rppi'}))
        status_verifikasi = data_rppi[0]["status_verifikasi"]
        
        #seleksi jika sudah verifikasi dan belum
        if status_verifikasi != 11:
            return make_response(jsonify({'status_code' : 200, 'description': 'menunggu verifikasi'}))
        else:
            #check status verifikasi
            query3 = """SELECT a.nama_mahasiswa, a.posisi, a.sks AS "sks_maks", c.sks AS "sks_project", e.sks AS "sks_course", 
                    f.sks AS "sks_rppm", g.sks AS "sks_rpptamu", b.status_verifikasi AS "status_approved_rppi"
                    FROM mahasiswa a LEFT JOIN rppi b ON a.id_mahasiswa = b.id_mahasiswa LEFT JOIN project c ON b.id_project = c.id_project
                    LEFT JOIN rppt d ON a.id_mahasiswa = d.id_mahasiswa LEFT JOIN course e ON d.id_course = e.id_course LEFT JOIN rppm f 
                    ON a.id_mahasiswa = f.id_mahasiswa LEFT JOIN rpptamu g ON a.id_mahasiswa = g.id_mahasiswa WHERE b.status_verifikasi = 11 
                    AND d.status_verifikasi = 11 AND f.status_verifikasi = 11 AND g.status_verifikasi = 11 AND a.id_mahasiswa = %s """
            values3 = (id_user, )
            data_status = dt.get_data(query3, values3)[0]
            return make_response(jsonify({'status_code' : 200, 'description' : data_status, 'status_user' : 'telah disetujui admin' , 'catatan' : 'silakan download'}))
    except Exception as e:
        return bad_request(str(e))


#check status lalu download rppi
@project.route('/check_status_rppi_download', methods=['GET'])
@cross_origin()
@jwt_required()
def check_status_rppi_download():
    try:
        id_user = str(get_jwt()["id_user"])
        role = str(get_jwt()["role_desc"])
        email = str(get_jwt()["email"])

        if role not in role_mahasiswa:
            return permission_failed()
        
        dt = Data()

        #check id mahasiswa
        query = "SELECT id_mahasiswa FROM mahasiswa WHERE id_mahasiswa = %s "
        values = (id_user, )
        data_mahasiswa = dt.get_data(query, values)
        if len(data_mahasiswa) == 0:
            return defined_error("id mahasiswa tidak di temukan", 401)
        
        #check id mahasiswa sudah mengajukan belum
        query2 = "SELECT id_mahasiswa FROM rppi WHERE id_mahasiswa = %s "
        values2 = (id_user, )
        data_rppi= dt.get_data(query2, values2)
        if len(data_rppi) == 0:
            return make_response(jsonify({'status_code' : 200, 'description': 'belum mengajukan rppi'}))
        
        #check status verifikasi
        query3 = """SELECT a.nama_mahasiswa, a.asal_kampus, a.posisi, b.status_verifikasi, b.skema, b.jabatan, c.nama_project, 
                c.jadwal_mentoring, c.jam FROM mahasiswa a LEFT JOIN rppi b ON a.id_mahasiswa = b.id_mahasiswa
                LEFT JOIN project c ON b.id_project = c.id_project WHERE b.id_mahasiswa = %s """
        values3 = (id_user, )
        data_status = dt.get_data(query3, values3)[0]
        db_nama_mahasiswa = data_status["nama_mahasiswa"]
        db_asal_kampus = data_status["asal_kampus"]
        db_posisi = data_status["posisi"]
        status_verifikasi = data_status["status_verifikasi"]
        db_jabatan = data_status["jabatan"]
        db_nama_project = data_status["nama_project"]
        db_skema = data_status["skema"]
        db_jadwal_mentoring = data_status["jadwal_mentoring"]
        db_jam = data_status["jam"]



        #seleksi jika sudah verifikasi dan belum
        if status_verifikasi != 11:
            return make_response(jsonify({'status_code' : 200, 'description': 'menunggu verifikasi'}))
        else:                            
            html = render_template( "rppi.html", db_nama_mahasiswa=db_nama_mahasiswa,db_asal_kampus=db_asal_kampus,db_posisi=db_posisi,
                                    db_jabatan=db_jabatan,db_nama_project=db_nama_project,db_skema=db_skema,db_jadwal_mentoring=db_jadwal_mentoring,
                                    db_jam=db_jam)
            # config = pdfkit.configuration(wkhtmltopdf='/opt/bin/wkhtmltopdf')
            pdf = pdfkit.from_string(html, False)
            response = make_response(pdf)
            response.headers["Content-Type"] = "application/pdf"
            response.headers["Content-Disposition"] = "attachment; filename=output.pdf"
            return response
 
    except Exception as e:
        return bad_request(str(e))

@project.route('/get')
def get():
    db_nama_mahasiswa = "Ari"
    html = render_template( "rppi.html", db_nama_mahasiswa=db_nama_mahasiswa)
    # config = pdfkit.configuration(wkhtmltopdf='/opt/bin/wkhtmltopdf')
    pdf = pdfkit.from_string(html, False)
    response = make_response(pdf)
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = "attachment; filename=output.pdf"
    return response

@project.route('/get_semua_project_mentor',methods=['GET'])
@cross_origin()
@jwt_required()
def get_semua_project_mentor():
    try:
        id_user = str(get_jwt()["id_user"])
        role = str(get_jwt()["role_desc"])
        email = str(get_jwt()["email"])

        if role not in role_mentor:
            return permission_failed()

        dt = Data()
        #get id_project sesuai mentor
        query1 = """SELECT a.nama_project, b.id_project FROM project a LEFT JOIN
                mentor_project b ON a.id_project = b.id_project 
                WHERE id_mentor = %s """
        values1 = (id_user, )
        nama_project = dt.get_data(query1, values1)
        return make_response(jsonify({'status_code': 200, 'description': nama_project}), 200)
    except Exception as e:
        return bad_request(str(e))

@project.route('upload_pdf',methods=['POST'])
@cross_origin()
@jwt_required()
def upload_pdf():

    ROUTE_NAME = request.path
    try:
        id_user = str(get_jwt()["id_user"])
        role = str(get_jwt()["role_desc"])
        email = str(get_jwt()["email"])

        if role not in role_mentor:
            return permission_failed()

        dt = Data()
        # data = request.json
        # if "nama_project" not in data:
        #     return parameter_error("nama_project tidak di temukan")
        # nama_project = data["nama_project"]

        # #check id_project
        # query2 = """SELECT id_project FROM project WHERE nama_project = %s"""
        # values2 = (nama_project, )
        # db_id_project = dt.get_data(query2, values2)[0]["id_project"]


        ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

        def allowed_file(filename):
            return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
        
        if 'file' not in request.files:
            resp = jsonify({'message' : 'No file part in the request'})
            resp.status_code = 400
            return resp
        file = request.files['file']
        if file.filename == '':
            resp = jsonify({'message' : 'No file selected for uploading'})
            resp.status_code = 400
            return resp
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            file = open(os.path.join(app.config['UPLOAD_FOLDER'], filename),'rb').read()
  
            # We must encode the file to get base64 string
            file = base64.b64encode(file)
            
            query = "INSERT INTO mom (id_mentor, dokumen_upload) VALUES (%s, %s)"
            values = (id_user, file)
            dt.insert_data(query, values)

            try:
                logs = secure_filename(strftime("%Y-%m-%d %H:%M:%S"))+" - "+ROUTE_NAME + \
                    " - id_mentor = "+str(id_user)+" - roles = "+str(role)+"\n"
            except Exception as e:
                logs = secure_filename(strftime(
                    "%Y-%m-%d %H:%M:%S"))+" - "+ROUTE_NAME+" - id_mentor = NULL - roles = NULL\n"
                # tambahLogs(logs)

            resp = jsonify({'message' : 'File successfully uploaded','status' : 200})
            resp.status_code = 200
            return resp
        else:
            resp = jsonify({'message' : 'Allowed file types are txt, pdf, png, jpg, jpeg, gif'})
            resp.status_code = 400
            return resp
    except Exception as e:
        return bad_request(str(e))

#download mom
@project.route('/download',methods=['GET'])
@cross_origin()
@jwt_required()
def download():
    try:
        id_user = str(get_jwt()["id_user"])
        role = str(get_jwt()["role_desc"])
        email = str(get_jwt()["email"])
        
        role_mentor_mahasiswa = ["mentor", "mahasiswa"]
        if role not in role_mentor_mahasiswa:
            return permission_failed()

        dt = Data()

        # query2 = """SELECT a.id_mahasiswa, b.id_mentor FROM rppi a LEFT JOIN 
        #         mentor_project b ON a.id_project = b.id_project WHERE b.id_mentor = %s"""
        # values2 = (id_user, )
        # id_mentor = dt.get_data(query2, values2)[0]["id_mentor"]

        # query3 = """SELECT a.id_mahasiswa, b.id_mentor FROM rppi a LEFT JOIN 
        #         mentor_project b ON a.id_project = b.id_project WHERE b.id_mentor = %s"""
        # values3 = (id_user, )
        # id_mahasiswa = dt.get_data(query3, values3)[0]["id_mahasiswa"]

        if role == "mentor":
            query = "SELECT * FROM mom WHERE id_mentor = %s "
            values = (id_user, )
            hasil_mom = dt.get_data(query, values)[0]["dokumen_upload"]
            binary_data = base64.b64decode(hasil_mom)
            # image = Image.open(io.BytesIO(binary_data))
            # image.show()
            return send_file(io.BytesIO(binary_data), attachment_filename='mom.pdf', as_attachment=True)
        else :
            query = """SELECT a.dokumen_upload FROM mom a LEFT JOIN mentor_project b ON a.id_mentor = b.id_mentor
                    LEFT JOIN rppi c ON b.id_project = c.id_project WHERE c.id_mahasiswa = %s"""
            values = (id_user, )
            hasil_mom = dt.get_data(query, values)[0]["dokumen_upload"]
            binary_data = base64.b64decode(hasil_mom)
            # image = Image.open(io.BytesIO(binary_data))
            # image.show()
            return send_file(io.BytesIO(binary_data), attachment_filename='mom.pdf', as_attachment=True)
        
        
        # if id_user != id_mentor:
        #     return make_response({"status": "gagal melihat mom karena punyamu"}, 200)
        # elif id_user != id_mahasiswa:
        #     return make_response({"status": "gagal melihat mom karena punyamu"}, 200)
        # elif id_user == id_mentor:
        #     query = "SELECT * FROM mom WHERE id_mentor = %s "
        #     values = (id_user, )
        #     hasil_mom = dt.get_data(query, values)[0]["dokumen_upload"]
        #     binary_data = base64.b64decode(hasil_mom)
        #     # image = Image.open(io.BytesIO(binary_data))
        #     # image.show()
        #     return send_file(io.BytesIO(binary_data), attachment_filename='mom.pdf', as_attachment=True)
        # else:
        #     query = """SELECT a.dokumen_upload FROM mom a LEFT JOIN mentor_project b ON a.id_mentor = b.id_mentor
        #             LEFT JOIN rppi c ON b.id_project = c.id_project WHERE id_mahasiswa = %s"""
        #     values = (id_user, )
        #     hasil_mom = dt.get_data(query, values)[0]["dokumen_upload"]
        #     binary_data = base64.b64decode(hasil_mom)
        #     # image = Image.open(io.BytesIO(binary_data))
        #     # image.show()
        #     return send_file(io.BytesIO(binary_data), attachment_filename='mom.pdf', as_attachment=True)
        
    except Exception as e:
        return bad_request(str(e))

