# app.py
from flask import Flask, request, render_template, redirect, url_for, session
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'clavesecretatienda'

def generar_id():
    if 'productos' in session and len(session['productos']) > 0:
        return max(item['id'] for item in session['productos']) + 1
    else:
        return 1

@app.route("/")
def index():
    if 'productos' not in session:
        session['productos'] = []
        
    productos = session.get('productos',[])
    return render_template('index.html', productos=productos)

@app.route("/nuevo", methods=['GET','POST'])
def nuevo():
    if request.method == 'POST':
        nombre = request.form['nombre']
        cantidad = int(request.form['cantidad'])
        precio = float(request.form['precio'])
        fecha_vencimiento = request.form['fecha_vencimiento']
        categoria = request.form['categoria']
        
        nuevo_producto = {
            'id': generar_id(),
            'nombre': nombre,
            'cantidad': cantidad,
            'precio': precio,
            'fecha_vencimiento': fecha_vencimiento,
            'categoria': categoria
        }
        
        if 'productos' not in session:
            session['productos'] = []
            
        session['productos'].append(nuevo_producto)
        session.modified = True
        return redirect(url_for('index'))
    
    return render_template('nuevo.html')

@app.route('/editar/<int:id>', methods=['GET','POST'])
def editar(id):
    lista_productos = session.get('productos',[])
    producto = next((p for p in lista_productos if p['id'] == id), None)
    if not producto:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        producto['nombre'] = request.form['nombre']
        producto['cantidad'] = int(request.form['cantidad'])
        producto['precio'] = float(request.form['precio'])
        producto['fecha_vencimiento'] = request.form['fecha_vencimiento']
        producto['categoria'] = request.form['categoria']
        session.modified = True
        return redirect(url_for('index'))
    
    return render_template('editar.html', producto=producto)

@app.route("/eliminar/<int:id>", methods=["POST"])
def eliminar(id):
    lista_productos = session.get('productos',[])
    producto = next((p for p in lista_productos if p['id'] == id), None)
    if producto:
        session['productos'].remove(producto)
        session.modified = True
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)