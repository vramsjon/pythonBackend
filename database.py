from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from jinja2.debug import rewrite_traceback_stack

app =  Flask(__name__)

# konfigurasi koneksi Mysql
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "db_python"

mysql = MySQL(app)

@app.route('/')

def check_connection():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT DATABASE()")
        db_name = cursor.fetchone()
        cursor.close()
        return f"Berhasil terhubung ke database: {db_name[0]}"
    except Exception as e:
        return f"Error: {str(e)}"


@app.route('/add_user', methods=['POST'])
def add_user():
    try:
        # mengambil data dari request
        nama = request.json['nama']
        email = request.json['email']

        #menjalankan query untuk menambahkan data
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO users (nama, email) VALUES (%s, %s)", (nama, email))
        mysql.connection.commit() #menyimpan perubbahan
        cursor.close()

        return jsonify({"message" : "User added succesfully"}), 201
    except Exception as e:
        return jsonify({"error" : str(e)}), 500

@app.route('/users', methods=['GET'])
def get_user():
    try:
        cursor = mysql.connection.cursor()

        # untuk mengambil semua data dari tabel users
        cursor.execute("SELECT * FROM users")
        result = cursor.fetchall() # mengambil semua baris data

        #m memformta hasil menjadi list of dict
        users = [
            {
                "id" : row[0],
                "nama" : row[1],
                "email" : row[2]

            }
            for row in result
        ]
        cursor.close()

        return jsonify(users) #mengembalikan data sebagai json
    except Exception as e:
        return jsonify({"error" : str(e)}), 500

@app.route('/update_user/<int:id>', methods=['PUT'])
def update_user(id):
    try:
        # mengambil data dari reques
        nama = request.json['nama']
        email = request.json['email']

        # menjalankan query untuk mengupdate data
        cursor = mysql.connection.cursor()
        cursor.execute("UPDATE users SET nama = %s, email = %s WHERE id = %s", (nama, email, id))
        mysql.connection.commit() # menyimpan perubahan
        cursor.close()

        return jsonify({"message" : "User update succesfully"})
    except Exception as e:
        return jsonify({"error" : str(e)}), 500

@app.route('/delete_user/<int:id>', methods=['DELETE'])
def delete_user(id):
    try:
        # menjalankan query untuk menghapus data berdasarkan id
        cursor = mysql.connection.cursor()
        cursor.execute("DELETE FROM users WHERE id = %s", (id,))
        mysql.connection.commit() #menyimpan perubahan
        cursor.close()

        return jsonify({"error" : "User deleted succesfully"} )
    except Exception as e:
        return jsonify({"error" : str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)