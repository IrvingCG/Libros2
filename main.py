from flask import Flask,flash,redirect, request, url_for,render_template
from flask_bootstrap import Bootstrap
from datetime import datetime
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = 'Clave_Secreta_Flask'
# Conexion DB
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'bibliotecadb'

mysql = MySQL(app)
#Bootstrap
Bootstrap(app)

#Fecha
@app.context_processor
def date_now():
    return {'now':datetime.utcnow()
            }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/informacion')
def informacion():
    return render_template('informacion.html')


@app.route('/crear-libro',methods =['GET' , 'POST'])
def crear_libro():
    if request.method == 'POST':
        nomlib = request.form['nombre_libro']
        autor = request.form['autor']
        categoria = request.form['categoria']
        fecha= request.form['fecha']
        status = request.form['status']
        
    
        cursor = mysql.connection.cursor()
        cursor.execute(f"INSERT INTO libros VALUES(NULL,%s,%s,%s,%s,%s)",(nomlib,autor,categoria,fecha,status))
        cursor.connection.commit()
        flash('has insertado los datos del libro correctamente ')
        return redirect(url_for('index'))
    return render_template('crear_libro.html') 

@app.route('/crear-usuario',methods =['GET' , 'POST'])
def crear_usuario():
    if request.method == 'POST':
        nombreu = request.form['nombre_user']
        correo = request.form['correo']
       
    
        cursor = mysql.connection.cursor()
        cursor.execute(f"INSERT INTO usuario VALUES(NULL,%s,%s)",(nombreu,correo))
        cursor.connection.commit()
        flash('has insertado los datos de usuario correctamente')
        return redirect(url_for('index'))
    return render_template('crear_usuario.html')

@app.route('/crear-categoria',methods =['GET' , 'POST'])
def crear_categoria():
    if request.method == 'POST':
        nombrec = request.form['nombre_categoria']
        descripcion = request.form['descripcion']
       
    
        cursor = mysql.connection.cursor()
        cursor.execute(f"INSERT INTO categoria VALUES(NULL,%s,%s)",(nombrec,descripcion))
        cursor.connection.commit()
        flash('has insertado los datos de categoria correctamente')
        return redirect(url_for('index'))
    return render_template('crear_categoria.html')



@app.route('/lista')
def lista():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM Libros')
    libros = cursor.fetchall()
    return render_template('lista_libros.html',libros = libros)

@app.route('/lista-usuario')
def lista_usuario():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM usuario')
    usuarios = cursor.fetchall()
    return render_template('lista_usuario.html',usuarios = usuarios)


@app.route('/lista-categoria')
def lista_categoria():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM categoria')
    categorias = cursor.fetchall()
    return render_template('lista_categoria.html',categorias = categorias)

@app.route('/borrar-libro/<libro_id>')
def borrar_libro(libro_id):
    cursor =mysql.connection.cursor()
    cursor.execute(f"DELETE FROM libros WHERE id_libro = {libro_id}")
    mysql.connection.commit()
    
    flash('Se elimino el registro con exito !!')
    
    return redirect(url_for('lista'))

@app.route('/borrar-usuario/<usuario_id>')
def borrar_usuario(usuario_id):
    cursor =mysql.connection.cursor()
    cursor.execute(f"DELETE FROM usuario WHERE id_usuario = {usuario_id}")
    mysql.connection.commit()
    
    flash('Se elimino el registro con exito !!')
    
    return redirect(url_for('lista_usuario'))

@app.route('/borrar-categoria/<categoria_id>')
def borrar_categoria(categoria_id):
    cursor =mysql.connection.cursor()
    cursor.execute(f"DELETE FROM categoria WHERE id_categoria = {categoria_id}")
    mysql.connection.commit()
    
    flash('Se elimino el registro con exito !!')
    
    return redirect(url_for('lista_categoria'))

@app.route('/editar-usuario/<usuario_id>' , methods =['GET', 'POST'])
def editar_usuario(usuario_id):
    if request.method =='POST':
        nombreu = request.form['nombre_user']
        correo = request.form['correo']
        
        cursor = mysql.connection.cursor()
        cursor.execute("""
            UPDATE usuario
            SET nombre_user = %s,
                correo = %s
            WHERE id_usuario = %s    
             """,(nombreu,correo,usuario_id) )
        cursor.connection.commit()
        
        flash('has actualizado los datos correctamente !!')
        return redirect(url_for('lista_usuario'))
    
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM usuario WHERE id_usuario = %s" ,(usuario_id))
    usuario = cursor.fetchall()
    cursor.close()
    
    return render_template('editar_user.html',usuario = usuario[0])


@app.route('/editar-categoria/<categoria_id>' , methods =['GET', 'POST'])
def editar_categoria(categoria_id):
    if request.method =='POST':
        nombrec = request.form['nombre_categoria']
        descripcion = request.form['descripcion']
        
        cursor = mysql.connection.cursor()
        cursor.execute("""
            UPDATE categoria
            SET nombre_categoria = %s,
                descripcion = %s
            WHERE id_categoria = %s    
             """,(nombrec,descripcion,categoria_id) )
        cursor.connection.commit()
        
        flash('has actualizado los datos correctamente !!')
        return redirect(url_for('lista_categoria'))
    
    
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM categoria WHERE id_categoria = %s" ,(categoria_id))
    categoria = cursor.fetchall()
    cursor.close()
    
    return render_template('editar_categoria.html',categoria = categoria[0])

@app.route('/editar-libro/<libro_id>' , methods =['GET', 'POST'])
def editar_libro(libro_id):
    if request.method =='POST':
      
        nomlib = request.form['nombre_libro']
        autor = request.form['autor']
        categoria = request.form['categoria']
        fecha= request.form['fecha']
        status = request.form['status']
        
        
        cursor = mysql.connection.cursor()
        cursor.execute("""
            UPDATE libros
            SET nombre_libro = %s,
                autor = %s,
                categoria = %s,
                fecha = %s,
                status = %s
            WHERE id_libro = %s    
             """,(nomlib,autor,categoria,fecha,status,libro_id) )
        cursor.connection.commit()
        
        flash('has actualizado los datos correctamente !!')
        return redirect(url_for('lista'))
    
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM libros WHERE id_libro = %s" ,(libro_id))
    libro = cursor.fetchall()
    cursor.close()
    
    return render_template('editar_libro.html',libro = libro[0])
    

@app.route('/prestamos')
def prestamos():
    return render_template('prestamos.html')

if __name__ == '__main__':
    app.run(debug=True) 
  