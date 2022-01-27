from distutils.log import debug
from flask import Flask
from flask import render_template
from flaskext.mysql import MySQL

app = Flask(__name__)

mysql = MySQL()
app.config['MYSQL_DATABASE_HOST']='localhost'
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']=''
app.config['MYSQL_DATABASE_DB']='solicitudes'
mysql.init_app(app)

@app.route('/')
def index():

    sql ="INSERT INTO `registro` (`id`, `cedula`, `lugarExpedicion`, `nombres`, `apellidos`, `telefono`, `email`, `empresaLaboro`, `cargo`, `fechaInicio`, `fechaRetiro`, `fechaNacimiento`, `fondoPension`) VALUES (NULL, '1075234987', 'neiva', 'anderson alexis', 'montenegro melo', '3214521011', 'adn@gmail.com', 'idesac', 'auxiliar administrativo', '01 de enero 1985', '30 de diciembre 1985', '01 de marzo 1989', 'porvenir');"
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()

    return render_template('registros/index.html')

if __name__ == '__main__':
    app.run(debug=True)