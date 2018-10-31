from flask import Flask, render_template, request, session, Response
from database import connector
from model import entities
import json
db = connector.Manager()
engine = db.createEngine()
primo = 73939133

app = Flask(__name__)
app.secret_key = 'Security Key'  # SECURITY KEY

cache = {}


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


@app.route('/current_created_sala')
def current_created_sala():
    db_session = db.getSession(engine)
    sala = db_session.query(entities.Sala).filter(
        entities.Sala.pin == session['created_sala_pin']).first()  # Nos permite obtener todos los usuarios que estan en nuestra bdd
    return Response(json.dumps(sala,
                               cls=connector.AlchemyEncoder),
                    mimetype='application/json')


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


# SALA EN LA QUE ESTAS LOGEADO
@app.route('/current_sala', methods=['GET'])
def current_sala():
    db_session = db.getSession(engine)
    sala = db_session.query(entities.Sala).filter(entities.Sala.pin == session['pin']).first()  # Nos permite obtener todos los usuarios que estan en nuestra bdd
    return Response(json.dumps(sala,
                               cls=connector.AlchemyEncoder),
                    mimetype='application/json')
# FIN


# USUARIO CON EL QUE ESTAS LOGEADO
@app.route('/current_user', methods=['GET'])
def current_user():
    db_session = db.getSession(engine)
    user = db_session.query(entities.User).filter(entities.User.id == session['logged_user_id']).first()  # Nos permite obtener todos los usuarios que estan en nuestra bdd
    return Response(json.dumps(user, cls=connector.AlchemyEncoder), mimetype='application/json')
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
# FIN


# CRUD PARA USERS
# CREATE USER
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


# READ USER
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


# UPDATE USER
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


# DELETE USER
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


# CRUD PARA MESSAGE
# PARA CHAT DINAMICO
@app.route('/messages/<user_from>/<user_to>', methods = ['GET'])
def get_message_by_users(user_from, user_to):
    db_session = db.getSession(engine)
    messages = db_session.query(entities.Message
        ).filter(entities.Message.user_from_id == user_from
        ).filter(entities.Message.user_to_id == user_to)
    data = []
    for message in messages:
        data.append(message)
    return Response(json.dumps(data,
                               cls=connector.AlchemyEncoder),
                    mimetype='application/json')
# FIN


# CREATE MESSAGE
@app.route('/messages', methods=['POST'])
def create_message():
    c = request.get_json(silent=True)
    db_session = db.getSession(engine)
    sala_to = db_session.query(entities.Sala).filter(entities.Sala.pin == c['pin']).first()
    message = entities.Message(content=c['content'], sala_to=sala_to)
    db_session.add(message)
    db_session.commit()
    return "TODO OK"
# FIN


# READ MESSAGE
@app.route('/messages')
def read_message():
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


# READ MESSAGE BY PIN ?
@app.route('/messages/<sala_to>', methods = ['GET'])
def get_message_by_pin(sala_to):
    db_session = db.getSession(engine)
    messages = db_session.query(entities.Message).filter(entities.Message.sala_to.pin == sala_to)
    data = []
    for message in messages:
        data.append(message)
    return Response(json.dumps(data,
                               cls=connector.AlchemyEncoder),
                    mimetype='application/json')
# FIN


# DELETE MESSAGE
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
'''
@app.route('/messages', methods = ['POST'])
def create_message():
    #c =  json.loads(request.form['values'])
    c = request.get_json(silent=True)
    db_session = db.getSession(engine)
    user_from = db_session.query(entities.User
            ).filter(entities.User.id == c['user_from_id']).first()
    user_to = db_session.query(entities.User
            ).filter(entities.User.id == c['user_to_id']).first()

    message = entities.Message(content= c['content'],
                                user_from = user_from,
                                user_to = user_to,
                                sent_on = datetime.datetime.utcnow()
                          )
    db_session.add(message)
    db_session.commit()
    return "TODO OK"
'''

if __name__ == '__main__':
    app.secret_key = ".."
    app.run(port=8080, threaded=True, debug=True, host=('localhost'))
