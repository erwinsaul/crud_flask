from flask import Flask, request, Response, render_template, redirect, url_for
import os
import database as db

template_dir = os.path.dirname( os.path.abspath(os.path.dirname(__file__)) )
template_dir = os.path.join(template_dir,'crud_flask', 'templates')

app = Flask(__name__, template_folder = template_dir)

#Rutas de la aplicacion de CRUD
@app.route('/')
def index():
    con = db.database.cursor()
    con.execute("SELECT * FROM cursos")
    result = con.fetchall()
    #Convertir los datos a diccionario
    data = []
    cname = [column[0] for column in con.description]
    for row in result:
        data.append(dict(zip(cname, row)))
    print(data)
    con.close()
    return render_template('index.html', data = data)


#Ruta para registrar Cursos
@app.route('/curso', methods=['POST'])
def create_curso():        
    try:
        nombre = request.form['nombre']
        sigla = request.form['sigla']
        nivel = request.form['nivel']
        
        if nombre and sigla and nivel:
            con = db.database.cursor()
            con.execute("INSERT INTO cursos (nombre, sigla, nivel) VALUES (%s, %s, %s)", (nombre, sigla, nivel))
            db.database.commit()
            con.close()
        else:            
            return "Todos los Campos son requeridos", 400

        return redirect(url_for('index'))
    
    except Exception as e:        
        print(f"Error: {e}")
        return "Error", 500

@app.route('/delete/<int:id>')
def delete(id):
    try:
        con = db.database.cursor()
        con.execute("DELETE FROM cursos WHERE id = %s", (id,))
        db.database.commit()
        con.close()
    except Exception as e:
        print(f"Error: {e}")
        return "Error al Eliminar", 500
    return redirect(url_for('index'))

@app.route('/update/<int:id>', methods=['POST'])
def update_curso(id):
    try:
        nombre = request.form['nombre']
        sigla = request.form['sigla']
        nivel = request.form['nivel']
        
        if nombre and sigla and nivel:
            con = db.database.cursor()
            con.execute("UPDATE cursos SET nombre = %s, sigla = %s, nivel = %s WHERE id = %s", (nombre, sigla, nivel, id))
            db.database.commit()
            con.close()
        else:            
            return "Todos los Campos son requeridos", 400

        return redirect(url_for('index'))
    
    except Exception as e:        
        print(f"Error: {e}")
        return "Error al Actualizar", 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)