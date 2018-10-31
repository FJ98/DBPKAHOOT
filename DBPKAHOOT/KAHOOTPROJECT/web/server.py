from flask import Flask, render_template, request, session, Response
from database import connector
from model import entities
import json
db = connector.Manager()
engine = db.createEngine()
primo = 73939133

app = Flask(__name__)
app.secret_key = 'Security Key'  # SECURITY KEY


# PAGINA DE INICIO
@app.route('/')
def index():
    return render_template('index.html')
# FIN


@app.route('/sala_logout', methods=['GET'])
def sala_logout():
    session.clear()
    return render_template('index.html')


@app.route('/pin', methods=['GET'])
def pin():
    if 'pin' in session :
        return render_template('sala_invitados.html')
    return render_template("pin.html")


# OBTENER LA SALA EN LA QUE ESTAS LOGEADO
@app.route('/current_sala', methods=['GET'])
def current_sala():
    db_session = db.getSession(engine)
    sala = db_session.query(entities.Sala).filter(entities.Sala.pin == session['pin']).first()  # Nos permite obtener todos los usuarios que estan en nuestra bdd
    return Response(json.dumps(sala,
                               cls=connector.AlchemyEncoder),
                    mimetype='application/json')
# FIN


@app.route('/current_created_sala')
def current_created_sala():
    db_session = db.getSession(engine)
    sala = db_session.query(entities.Sala).filter(
        entities.Sala.pin == session['created_sala_pin']).first()  # Nos permite obtener todos los usuarios que estan en nuestra bdd
    return Response(json.dumps(sala,
                               cls=connector.AlchemyEncoder),
                    mimetype='application/json')


# OBTENER LA SALA EN LA QUE ESTAS LOGEADO
@app.route('/current_sala', methods=['GET'])
def current_sala():
    db_session = db.getSession(engine)
    sala = db_session.query(entities.Sala).filter(entities.Sala.pin == session['pin']).first()  # Nos permite obtener todos los usuarios que estan en nuestra bdd
    return Response(json.dumps(sala,
                               cls=connector.AlchemyEncoder),
                    mimetype='application/json')
# FIN


# Ruta para verificar si existe el pin en la base de datos
@app.route('/do_pin', methods=['POST'])
def do_pin():
    pin = request.form['pin']

    db_session = db.getSession(engine)
    salas = db_session.query(entities.Sala)

    for sala in salas:
        if sala.pin == pin:
            session['pin'] = pin
            return render_template('sala_invitados.html')

    return render_template('fail.html')
# FIN


# CRUD PARA CADA CLASE DE ENTITIES.PY
# CRUD PARA SALAS
# CREATE SALA
@app.route('/create_sala', methods=['POST'])
def create_sala():
    name = request.form['name']
    db_session = db.getSession(engine)
    numero =  db_session.query(entities.Contador).first()
    pin = ((numero.number)*primo)%90000000 + 10000000
    sala = entities.Sala(name=name, pin=pin)
    db_session.add(sala)
    session['created_sala_pin'] = pin
    numeros = db_session.query(entities.Contador).filter(entities.Contador.id == 1)
    for numero_ in numeros:
        numero_.number = numero.number +1
        db_session.add(numero_)
        db_session.commit()
    return render_template('sala.html')
# FIN


# READ SALA
@app.route('/read_sala', methods=['GET'])
def read_sala():
    db_session = db.getSession(engine)
    salas = db_session.query(entities.Sala)  # Nos permite obtener todas las salas que estan en nuestra bdd
    data = []
    for sala in salas:
        data.append(sala)

    return Response(json.dumps(data,
                               cls=connector.AlchemyEncoder),
                    mimetype='application/json')
# FIN


# DELETE SALA
@app.route('/salas/<id>', methods=['DELETE'])
def delete_sala(id):
    db_session = db.getSession(engine)
    salas = db_session.query(entities.Sala).filter(entities.Sala.id == id)
    for sala in salas:
        db_session.delete(sala)
    db_session.commit()
    return "sala deleted"
# FIN


@app.route('/salas', methods=['POST'])
def do_register():
    pin = request.form['pin']
    name = request.form['name']
    sala = entities.Sala(pin=pin, name=name)
    db_session = db.getSession(engine)
    db_session.add(sala)
    db_session.commit()
    return "TODO OK"


@app.route('/contador', methods=['POST'])
def set_contador():
    number = request.form['number']
    numero = entities.Contador(number=number)
    db_session = db.getSession(engine)
    db_session.add(numero)
    db_session.commit()
    return "TODO OK"


# CRUD USERS
# CREATE USER METHOD CURRENT
@app.route('/current_user', methods=['GET'])
def current_user():
    db_session = db.getSession(engine)
    user = db_session.query(entities.User).filter(entities.User.id == session['logged_user_id']).first()  # Nos permite obtener todos los usuarios que estan en nuestra bdd
    return Response(json.dumps(user,
                               cls=connector.AlchemyEncoder),
                    mimetype='application/json')
# FIN


# CREATE USER METHOD
@app.route('/users', methods=['GET'])
def create_user():
    db_session = db.getSession(engine)
    users = db_session.query(entities.User)  # Nos permite obtener todos los ususarios que estan en nuestra bdd
    data = []
    for user in users:
        data.append(user)

    return Response(json.dumps(data,
                               cls=connector.AlchemyEncoder),
                    mimetype='application/json')
# FIN


# READ USER METHOD
@app.route('/users/<id>', methods=['GET'])
def read_user(id):
    db_session = db.getSession(engine)
    users = db_session.query(entities.User).filter(entities.User.id == id)  # Nos permite obtener todos los ususarios que estan en nuestra bdd
    data = []
    for user in users:
        data.append(user)

    return Response(json.dumps(data,
                               cls=connector.AlchemyEncoder),
                    mimetype='application/json')
# FIN


# UPDATE USER METHOD
@app.route('/users/<id>', methods=['PUT'])
def update_user(id):
    db_session = db.getSession(engine)
    users = db_session.query(entities.User).filter(entities.User.id == id)  # Nos permite obtener todos los ususarios que estan en nuestra bdd
    for user in users:
        user.nickname = request.form['nickname']
        db_session.add(user)
    db_session.commit()  # Es para cerrar la orden y decirle a la bdd que lo haga
    return "User updated!"
# FIN


# DELETE USER METHOD
@app.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    db_session = db.getSession(engine)
    users = db_session.query(entities.User).filter(entities.User.id == id)  # Nos permite obtener todos los ususarios que estan en nuestra bdd
    for user in users:
        db_session.delete(user)
    db_session.commit()  # Es para cerrar la orden y decirle a la bdd que lo haga
    return "User deleted!"
# FIN
# FIN


# REDIRIGIR A PAGINAS
@app.route('/name_sala')
def name_sala():
    if 'created_sala_pin' in session:
        return render_template('sala.html')
    return render_template('name_sala.html')


@app.route('/disjoin_sala')
def disjoin_sala():
    session.clear()
    return render_template('index.html')
# FIN


# CRUD MESSAGE
# CREATE MESSAGE METHOD
@app.route('/messages')
def create_message():
    db_session = db.getSession(engine)
    messages = db_session.query(entities.Message)
    data = []
    for user in messages:
        data.append(user)
    db_session.commit()  # Es para cerrar la orden y decirle a la bdd que lo haga
    return Response(json.dumps(data,
                               cls=connector.AlchemyEncoder),
                    mimetype='application/json')
# FIN


# READ MESSAGE METHOD
@app.route('/messages/<id>', methods=['GET'])
def read_message(id):
    db_session = db.getSession(engine)
    messages = db_session.query(entities.Message).filter(entities.Message.id == id)
    data = []
    for user in messages:
        data.append(user)
    return Response(json.dumps(data,
                               cls=connector.AlchemyEncoder),
                    mimetype='application/json')
# FIN


# UPDATE MESSAGE METHOD
@app.route('/messages/<id>', methods=['PUT'])
def update_message(id):
    db_session = db.getSession(engine)
    messages = db_session.query(entities.Message).filter(entities.Message.id == id)
    for message in messages:
        message.content = request.form['content']
        message.sent_on = request.form['sent_on']
        message.user_from_id = request.form['user_from_id']
        message.user_to_id = request.form['user_to_id']
        message.user_from = request.form['user_from']
        message.user_to = request.form['user_to']
    db_session.commit()  # Es para cerrar la orden y decirle a la bdd que lo haga
    return "Message updated"
# FIN


# DELETE MESSAGE METHOD
@app.route('/messages/<id>', methods=['DELETE'])
def delete_message(id):
    db_session = db.getSession(engine)
    messages = db_session.query(entities.Message).filter(entities.Message.id == id)
    for message in messages:
        db_session.delete(message)
    db_session.commit()  # Es para cerrar la orden y decirle a la bdd que lo haga
    return "Message deleted"
# FIN
# FIN
# FIN


# FIN
# @app.route('/clean_users', methods=['GET'])
#  def clean_users():
#      db_session = db.getSession(engine)
#      users = db_session.query(entities.User)
#      for user in users:
#          db_session.delete(user)
#          db_session.commit()
# return "Todos los usuarios eliminados"


if __name__ == '__main__':
    app.secret_key = ".."
    app.run(port=8080, threaded=True, debug=True, host=('localhost'))
