from distutils.log import debug
from fileinput import filename
from flask import Flask
from flask import render_template,request,redirect
from flaskext.mysql import MySQL
from datetime import datetime

app = Flask(__name__)

mysql = MySQL()
app.config['MYSQL_DATABASE_HOST']='localhost'
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']=''
app.config['MYSQL_DATABASE_DB']='solicitudes'
mysql.init_app(app)



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