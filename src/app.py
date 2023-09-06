"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def handle_hello():

    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    response_body = members


    return jsonify(response_body), 200

#Ruta para crear un miembro 
@app.route("/member",methods = ["POST"])
def Crear_Miembro():
    data_member = request.json
    try:
        if "first_name" in data_member and "age" in data_member and "lucky_numbers" in data_member:
        #ahora pasaremos a crear a nuestro nuevo miembro
            statusAdd = jackson_family.add_member(data_member)
            if(statusAdd == True) :
                return jsonify({"msg":"El miembro se creo exitosamente"}),200
            else:
                return jsonify({"msg":"Error al insertar el miembro"}),400
        

        return jsonify({"msg":"Debe de ingresar las credenciales correctas"}),400
    except TypeError:
        return jsonify({"error":TypeError}),500
        

@app.route("/member/<int:id>",methods = ["GET"])
def BuscarMiembroEspesifico(id):
    try:
        member = jackson_family.get_member(id)
        if member == None:
            return jsonify({"msg":"No hay ningun miembro con ese id"})
        memberReturned = {
            "first_name":member["first_name"],
            "id":member["id"],
            "age":member["age"],
            "lucky_numbers":member["lucky_numbers"]
        }
        return jsonify(memberReturned)

    except TypeError:
        return jsonify({"error":TypeError}),500
    
@app.route("/member/<int:id>",methods = ["DELETE"])
def Borrar(id):
    try:
        memberDElETE = jackson_family.delete_member(id)
        if memberDElETE == False:
            return jsonify({"msg":"No hay ningun miembro con ese id"})
        return jsonify({"done":True})

    except TypeError:
        return jsonify({"error":TypeError}),500





# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
