from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.secret_key = 'clave_secreta'  # Debes cambiar esto a una clave segura

# Datos de usuario de ejemplo (esto se debe almacenar en una base de datos en un entorno real)
users = {
    'roger': generate_password_hash('a'),
}

# Lista de pedidos de ejemplo
p_done = [
    {'titul': 'Llibre Quijote', 'tipus': 'Llibre', 'temps':'1','start': 'Biblioteca', 'end': 'Engiyeria', 'preu': '3'},
]
p_new=[]

serveis_publics = [
    {
        'titul': 'Llibre Quijote',
        'tipus': 'Llibre',
        'temps': '1',
        'start': 'Biblioteca',
        'end': 'Enginyeria',
        'preu': '3'
    },
    {
        'titul': 'Pizza Margherita',
        'tipus': 'Comida',
        'temps': '30 minutos',
        'start': 'Pizzeria',
        'end': 'Casa',
        'preu': '10'
    },
    {
        'titul': 'Camiseta Roja',
        'tipus': 'Ropa',
        'temps': '2 días',
        'start': 'Tienda de Ropa',
        'end': 'Domicilio',
        'preu': '15'
    },
    {
        'titul': 'Coca-Cola',
        'tipus': 'Bebida',
        'temps': '1 hora',
        'start': 'Supermercado',
        'end': 'Casa',
        'preu': '2'
    },
    {
        'titul': 'Auriculares Inalámbricos',
        'tipus': 'Electrónica',
        'temps': '3 días',
        'start': 'Tienda de Electrónica',
        'end': 'Oficina',
        'preu': '50'
    },
    {
        'titul': 'Flores Rosadas',
        'tipus': 'Regalo',
        'temps': '2 horas',
        'start': 'Floristería',
        'end': 'Hospital',
        'preu': '20'
    },
    {
        'titul': 'DVD Película de Acción',
        'tipus': 'Entretenimiento',
        'temps': '1 día',
        'start': 'Tienda de Películas',
        'end': 'Casa',
        'preu': '5'
    },
    {
        'titul': 'Zapatillas Deportivas',
        'tipus': 'Ropa Deportiva',
        'temps': '2 días',
        'start': 'Tienda Deportiva',
        'end': 'Gimnasio',
        'preu': '60'
    },
    {
        'titul': 'Agua Mineral',
        'tipus': 'Bebida',
        'temps': '45 minutos',
        'start': 'Supermercado',
        'end': 'Casa',
        'preu': '1'
    },
    {
        'titul': 'Portátil Lenovo',
        'tipus': 'Tecnología',
        'temps': '4 días',
        'start': 'Tienda de Electrónica',
        'end': 'Oficina',
        'preu': '700'
    }
]
@app.route('/', methods=['GET', 'POST'])
def inici():
    return render_template('inici.html', pedidos=p_done)

@app.route('/pagina_principal', methods = ['GET', 'POST'])
def pagina_principal():
    return render_template('pagina_principal.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in users and check_password_hash(users[username], password):
            session['username'] = username
            flash('Has iniciado sesión exitosamente', 'success')
            return redirect(url_for('pagina_principal'))
        else:
            flash('Credenciales incorrectas. Inténtalo de nuevo.', 'error')

    return render_template('login.html')

@app.route('/menu', methods=['GET', 'POST'])
def menu():
    return render_template('menu.html')

@app.route('/cartera', methods=['GET', 'POST'])
def cartera():
    return render_template('cartera.html')

@app.route('/pedidos', methods=['GET', 'POST'])
def pedidos():
    return render_template('pedidos.html', pedidos=p_done)

@app.route('/nueva_comanda', methods=['POST'])
def nueva_comanda():

    if request.method == 'POST':
        # Obtén los datos del formulario
        titulo = request.form.get('titulo')
        tipus = request.form.get('tipus')
        temps = request.form.get('temps')
        ubi_start = request.form.get('ubi_start')
        ubi_end = request.form.get('ubi_end')
        descripcio = request.form.get('descripcio')
        preu = request.form.get('preu')

        # Crea un diccionario con los datos del formulario
        nueva_comanda = {
            'titul': titulo,
            'tipus': tipus,
            'temps': temps,
            'start': ubi_start,
            'end': ubi_end,
            'descripcio': descripcio,
            'preu': preu
        }

        # Agrega la nueva comanda a la lista de pedidos
        p_new.append(nueva_comanda)
        print(p_new)

        # Redirige a la página de pedidos después de agregar la comanda
        return redirect(url_for('comandes_obertes'))

    # Si se accede a esta ruta de manera directa, redirige a otro lugar o muestra un mensaje de error
    return redirect(url_for('error'))

@app.route('/comandes_obertes', methods = ['GET', 'POST'])
def comandes_obertes():
    return render_template('comandes_obertes.html', pedidos = p_new)

llista_serveis_a_realitzar = [{'titul': 'Llibre Quijote', 'tipus': 'Llibre', 'temps':'1','start': 'Biblioteca', 'end': 'Engiyeria', 'preu': '3'}]

@app.route('/acceptat/ <num>', methods=['GET', 'POST'])
def acceptat(num):
    numerop_general = (int(num) -1)
    pedido_a_afegir_i_a_eliminar = serveis_publics[numerop_general]
    llista_serveis_a_realitzar.append(pedido_a_afegir_i_a_eliminar)
    serveis_publics.remove(pedido_a_afegir_i_a_eliminar)
    return redirect(url_for('serveis'))

@app.route('/serveis', methods = ['GET', 'POST'])
def serveis():
    return render_template('realitzar_servei.html', pedidos = serveis_publics)


@app.route('/servei_realitzat/ <num>', methods=['GET', 'POST'])
def servei_realitzat(num):
    numerop_general = (int(num) -1)
    pedido_a_afegir_i_a_eliminar = llista_serveis_a_realitzar[numerop_general]
    llista_serveis_a_realitzar.remove(pedido_a_afegir_i_a_eliminar)
    return redirect(url_for('serveis_a_realitzar'))


@app.route('/comandes_obertes_acceptada/ <num>', methods=['GET', 'POST'])
def comandes_obertes_acceptada(num):
    numerop_general = (int(num) -1)
    pedido_a_afegir_i_a_eliminar = p_new[numerop_general]
    p_new.remove(pedido_a_afegir_i_a_eliminar)
    p_done.append(pedido_a_afegir_i_a_eliminar)
    return redirect(url_for('comandes_obertes'))

@app.route('/serveis_a_realitzar', methods = ['GET', 'POST'])
def serveis_a_realitzar():
    return render_template('serveis_a_realitzar.html', pedidos = llista_serveis_a_realitzar)

@app.route('/state/ <num>', methods = ['GET', 'POST'])
def state(num):
    numerop_general = (int(num) -1)
    pedido_a_afegir_i_a_eliminar = [p_new[numerop_general]]
    return render_template('state.html', pedidos=pedido_a_afegir_i_a_eliminar)

@app.route('/edit_state', methods = ['GET', 'POST'])
def edit_state():
    return render_template('state.html')

@app.route('/ranking', methods = ['GET', 'POST'])
def ranking():
    return render_template('ranking.html')




if __name__ == '__main__':
    app.run(debug=True)
