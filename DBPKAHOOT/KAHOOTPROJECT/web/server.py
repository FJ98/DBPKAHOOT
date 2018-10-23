from flask import Flask, render_template, request, session, Response
from database import connector
from model import entities
import json
db = connector.Manager()
engine = db.createEngine()

app = Flask(__name__)
app.secret_key = 'Security Key'  # SECURITY KEY


# PAGINA DE INICIO
@app.route('/')
def index():
    return render_template('index.html')
# FIN


@app.route('/sala', methods=['GET'])
def sala():
    return render_template("sala.html")

@app.route('/create_sala', methods=['POST','GET'])
def do_register():
    name = request.form['name']
    fullname = request.form['fullname']
    password = request.form['password']
    username = request.form['username']
    print(name, fullname, password, username)

    user = entities.User(username = username,
                         name = name,
                         fullname = fullname,
                         password = password)
    session = db.getSession(engine)
    session.add(user)
    session.commit()
    return "TODO OK"

@app.route('/pin', methods=['GET'])
def pin():
    return render_template("pin.html")


@app.route('/do_logout')  # creo que va login.html pero pensandolo bien creo que no y creo que es logout no do_logout aunque deberia existir un logout y un do_logout aunque no se
def do_logout():
    session.clear()
    return render_template('index.html')


#ruta para verificar si existe el pin en la base de datos
@app.route('/do_pin',methods=['POST'])
def do_pin():
    pin = request.form['pin']

    db_session = db.getSession(engine)
    salas = db_session.query(entities.Sala)

    for sala in salas:
        if sala.pin == pin:
            session['name'] = pin
            return render_template('sala.html')

    return render_template('fail.html')




# CRUD FOR EACH CLASS FROM ENTITIES.PY

#CRUD PARA SALAS
#OBTENER TODAS LAS SALAS
@app.route('/salas',methods=['GET'])
def salas():
    db_session = db.getSession(engine)
    salas = db_session.query(entities.Sala)  # Nos permite obtener todas las salas que estan en nuestra bdd
    data = []
    for sala in salas:
        data.append(sala)

    return Response(json.dumps(data,
                               cls=connector.AlchemyEncoder),
                    mimetype='application/json')



#CREAR SALA

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
def users():
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
def get_user(id):
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
        user.name = request.form['name']
        user.fullname = request.form['fullname']
        user.password = request.form['password']
        user.username = request.form['username']
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


# CRUD MESSAGE
# CREATE MESSAGE METHOD
@app.route('/messages')
def messages():
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
def get_message(id):
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


# LA VERDAD NO SE QUE ES CLEAN USERS TODAVIA, LO DEDUZCO PERO NO LO SE
@app.route('/clean_users', methods=['GET'])
def clean_users():
    db_session = db.getSession(engine)
    users = db_session.query(entities.User)  # Nos permite obtener todos los ususarios que estan en nuestra bdd
    for user in users:
        user.name = request.form['name']
        user.fullname = request.form['fullname']
        user.password = request.form['password']
        user.username = request.form['username']
        db_session.add(user)
    db_session.commit()  # Es para cerrar la orden y decirle a la bdd que lo haga
    return "Todos los usuarios borrados"
# FIN
# @app.route('/clean_users', methods=['GET'])
#  def clean_users():
#      db_session = db.getSession(engine)
#      users = db_session.query(entities.User)
#      for user in users:
#          db_session.delete(user)
#          db_session.commit()
# return "Todos los usuarios eliminados"


# CUANTAS LETRAS TIENE MI NOMBRE
@app.route('/cuantasletras/<nombre>')
def cuantas_letras(nombre):
    return str(len(nombre))
# FIN


# SUMAR UN NUMERO DE ACUERDO A LA SESION DE CADA USUARIO
@app.route('/sumar/<numero>')
def sumar(numero):
    if 'suma' not in session:
        session['suma'] = '0'
    session['suma'] = int(session['suma'])+int(numero)

    return str(session['suma'])
# FIN


if __name__ == '__main__':
    app.secret_key = ".."
    app.run(port=8080, threaded=True, host=('localhost'))
