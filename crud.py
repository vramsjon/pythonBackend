from flask import Flask, jsonify, request

app = Flask(__name__)

#data dummy untuk simulasi database
users = [
    {"id": 1, "name" : "Vramsjon", "age" : 25},
    {"id" : 2, "name" : "Don Joe", "age" : 21},
    {"id" : 3, "name" : "Johan", "age" : 20}
]

#READ: mendapatkan semua user
@app.route("/users", methods=["GET"])
def get_users():
    return jsonify(users)

#READ: mendapatkan user berdasarkan ID
@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = next((u for u in users if u["id"] == user_id), None)
    if user:
        return jsonify(user)
    return jsonify({"error" : "User not found"}), 404

#CREATE: Menambahkan user baru
@app.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()
    new_user = {
        "id" : len(users) + 1,
        "name" : data["name"],
        "age" : data["age"]
    }
    users.append(new_user)
    return jsonify(new_user), 201

#UPDATE: memperbarui data user berdasarkan ID
@app.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    data = request.get_json()
    user = next((u for u in users if u["id"] == user_id), None)
    if user:
        user["name"] = data.get("name", user["name"])
        user["age"] = data.get("age", user["age"])
        return jsonify(user)
    return jsonify({"error" : "User not found"}), 404

#DELETE: menghapus user berdasarkan ID
@app.route("/users/<int:user_id>",  methods=["DELETE"])
def delete_user(user_id):
    global users
    users = [u for u in users if u["id"] != user_id]
    return jsonify({"message" : "User deleted succesfully"})

if __name__ == "__main__":
    app.run(debug=True)

