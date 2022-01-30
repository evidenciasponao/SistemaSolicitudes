from distutils.log import debug
from fileinput import filename
import re
from flask import Flask
from flask import render_template,request,redirect
from flaskext.mysql import MySQL
from flask import send_from_directory
from datetime import datetime
import os 

app = Flask(__name__)

mysql = MySQL()
app.config['MYSQL_DATABASE_HOST']='localhost'
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']=''
app.config['MYSQL_DATABASE_DB']='solicitudes'
mysql.init_app(app)

CARPETA= os.path.join('uploads')
app.config['CARPETA']=CARPETA

@app.route('/uploads/<nombreFoto>')
def uploads(nombreFoto):
    return send_from_directory(app.config['CARPETA'],nombreFoto)

@app.route('/')
def index():

    sql ="SELECT * FROM `registro`;"
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql)

    registro=cursor.fetchall()
    print(registro)

    conn.commit()

    return render_template('registros/index.html', registro=registro)

@app.route('/destroy/<int:id>')
def destroy(id):
    conn = mysql.connect()
    cursor = conn.cursor()

    cursor.execute("SELECT foto FROM registro WHERE id=%s", id)
    fila=cursor.fetchall()
    os.remove(os.path.join(app.config['CARPETA'], fila[0][0]))
 

    cursor.execute("DELETE FROM registro WHERE id = %s",(id))
    conn.commit()
    return redirect('/')

@app.route('/edit/<int:id>')
def edit(id):

    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM registro WHERE id = %s", (id))
    registros=cursor.fetchall()
    conn.commit()
    print(registros)

    return render_template('registros/edit.html', registros=registros)

@app.route('/update', methods=['POST'])
def update():
    _cedula=request.form['txtCedula']
    _lugarExpedicion=request.form['txtLugarExpedicion']
    _nombres=request.form['txtNombres']
    _apellidos=request.form['txtApellidos']
    _telefono=request.form['txtTelefono']
    _email=request.form['txtEmail']
    _empresaLaboro=request.form['txtEmpresaLaboro']
    _cargo=request.form['txtCargo']
    _fechaInicio=request.form['txtFechaInicio']
    _fechaRetiro=request.form['txtFechaRetiro']
    _fechaNacimiento=request.form['txtFechaNacimiento']
    _fondoPension=request.form['txtFondoPension']
    _foto=request.files['txtFoto']    
    id=request.form['txtID']

    sql ="UPDATE `registro` SET cedula=%s, lugarExpedicion=%s, nombres=%s, apellidos=%s, telefono=%s, email=%s, empresaLaboro=%s, cargo=%s, fechaInicio=%s, fechaRetiro=%s, fechaNacimiento=%s, fondoPension=%s WHERE id=%s ;"
    
    datos=(_cedula,_lugarExpedicion,_nombres,_apellidos,_telefono,_email,_empresaLaboro,_cargo,_fechaInicio,_fechaRetiro,_fechaNacimiento,_fondoPension, id)
    
    conn = mysql.connect()
    cursor = conn.cursor()

    now = datetime.now()
    tiempo = now.strftime("%Y%H%M%S")

    if _foto.filename!='':

        nuevoNombreFoto=tiempo+_foto.filename
        _foto.save("uploads/"+nuevoNombreFoto)

        cursor.execute("SELECT foto FROM registro WHERE id=%s", id)
        fila=cursor.fetchall()

        os.remove(os.path.join(app.config['CARPETA'], fila[0][0]))
        cursor.execute("UPDATE registro SET foto=%s WHERE id=%s",(nuevoNombreFoto,id)) 
        conn.commit()   

    cursor.execute(sql,datos)
    conn.commit()

    return redirect('/')

@app.route('/create')
def create():
    return render_template('registros/create.html')

@app.route('/store', methods=['POST'])
def storage():
    _cedula=request.form['txtCedula']
    _lugarExpedicion=request.form['txtLugarExpedicion']
    _nombres=request.form['txtNombres']
    _apellidos=request.form['txtApellidos']
    _telefono=request.form['txtTelefono']
    _email=request.form['txtEmail']
    _empresaLaboro=request.form['txtEmpresaLaboro']
    _cargo=request.form['txtCargo']
    _fechaInicio=request.form['txtFechaInicio']
    _fechaRetiro=request.form['txtFechaRetiro']
    _fechaNacimiento=request.form['txtFechaNacimiento']
    _fondoPension=request.form['txtFondoPension']
    _foto=request.files['txtFoto']

    now = datetime.now()
    tiempo = now.strftime("%Y%H%M%S")

    if _foto.filename!='':
        nuevoNombreFoto=tiempo+_foto.filename
        _foto.save("uploads/"+nuevoNombreFoto)

    sql ="INSERT INTO `registro` (`id`, `cedula`, `lugarExpedicion`, `nombres`, `apellidos`, `telefono`, `email`, `empresaLaboro`, `cargo`, `fechaInicio`, `fechaRetiro`, `fechaNacimiento`, `fondoPension`, `foto`) VALUES (NULL,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
    
    datos=(_cedula,_lugarExpedicion,_nombres,_apellidos,_telefono,_email,_empresaLaboro,_cargo,_fechaInicio,_fechaRetiro,_fechaNacimiento,_fondoPension,nuevoNombreFoto)
    
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql,datos)
    conn.commit()

    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)