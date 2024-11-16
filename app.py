from flask import Flask, render_template, url_for
import pandas as pd
import matplotlib.pyplot as plt
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/reviews')
def reviews():
    return render_template('reviews.html')

@app.route('/analytics')
def analytics():
    # Lista de sitios turísticos (creación por medio de diccionarios)
    sitios_turisticos = [
        {'nombre': 'Cartagena', 'descripcion': 'Ciudad amurallada con playas exóticas', 'imagen': 'static/img/Cartagena.jpg'},
        {'nombre': 'Bogotá', 'descripcion': 'Capital de Colombia, rica en historia y cultura', 'imagen': 'static/img/Bogota.jpg'},
        {'nombre': 'Medellín', 'descripcion': 'Ciudad de la eterna primavera', 'imagen': 'static/img/Medellin.jpg'},
        {'nombre': 'Cali', 'descripcion': 'Capital de la salsa y el baile', 'imagen': 'static/img/Cali.jpg'},
        {'nombre': 'Santa Marta', 'descripcion': 'Playas hermosas y el Parque Tayrona', 'imagen': 'static/img/SantaMarta.jpg'},
        {'nombre': 'Barranquilla', 'descripcion': 'Famosa por su Carnaval, su música y su gastronomía', 'imagen': 'static/img/Barranquilla.jpg'},
        {'nombre': 'Pereira', 'descripcion': 'La ciudad de las oportunidades y el eje cafetero', 'imagen': 'static/img/Pereira.jpg'},
        {'nombre': 'Bucaramanga', 'descripcion': 'Ciudad de parques y la cuna de la gastronomía santandereana', 'imagen': 'static/img/Bucaramanga.jpg'},
        {'nombre': 'Cartago', 'descripcion': 'Conocida como la ciudad de la cultura y el folclore', 'imagen': 'static/img/Cartago.jpg'},
        {'nombre': 'San Andrés', 'descripcion': 'Isla tropical con aguas cristalinas y arrecifes de coral', 'imagen': 'static/img/SanAndres.jpg'},
        {'nombre': 'Montería', 'descripcion': 'Famosa por su ganado y su música tropical', 'imagen': 'static/img/Monteria.jpg'},
        {'nombre': 'Villa de Leyva', 'descripcion': 'Un hermoso pueblo colonial lleno de historia y cultura', 'imagen': 'static/img/VilladeLeyva.jpg'}
    ]
    
    # Obtener las rutas de los gráficos
    image_path_line = grafico()  # Ruta para el gráfico de línea
    image_path_pie = grafico_torta()  # Ruta para el gráfico de torta
    
    # Pasar los datos y las rutas de las imágenes a la plantilla
    return render_template('analytics.html', 
                           sitios=sitios_turisticos, 
                           image_path_line=image_path_line, 
                           image_path_pie=image_path_pie)

def obtener_datos_turismo():
    # Cargar el archivo CSV especificando el delimitador como punto y coma
    df = pd.read_csv('static/sources/1.csv', delimiter=';')

    # Limpiar los nombres de las columnas eliminando espacios y caracteres invisibles
    df.columns = df.columns.str.strip()

    # Verificar si la columna 'Country Name' existe
    if 'Country Name' not in df.columns:
        print("No se encontró la columna 'Country Name'. Verifica el archivo CSV.")
        return None

    # Limpiar los espacios alrededor de los valores en la columna 'Country Name'
    df['Country Name'] = df['Country Name'].str.strip()

    # Verificar si hay datos para Colombia
    df_colombia = df[df['Country Name'] == 'Colombia']
    
    if df_colombia.empty:
        print("No hay datos de turismo para Colombia.")
        return None

    # Transformar los datos para graficar
    df_colombia = df_colombia.melt(id_vars=['Country Name', 'Country Code', 'Indicator Name', 'Indicator Code'],
                                   var_name='Year', value_name='Arrivals')
    df_colombia = df_colombia.dropna(subset=['Arrivals'])
    
    return df_colombia

def grafico():
    df_colombia = obtener_datos_turismo()
    if df_colombia is None:
        return None
    
    # Graficar los datos
    plt.figure(figsize=(12, 6))
    plt.plot(df_colombia['Year'], df_colombia['Arrivals'], marker='o')
    plt.xlabel('Año')
    plt.ylabel('Número de llegadas')
    plt.title('Llegadas de turistas internacionales a Colombia')
    plt.xticks(rotation=45)

    # Guardar la imagen del gráfico
    image_path = os.path.join('static', 'img', 'grafico_turismo.png')
    plt.savefig(image_path)
    plt.close()

    return url_for('static', filename='img/grafico_turismo.png')

def grafico_torta():
    df_colombia = obtener_datos_turismo()
    if df_colombia is None:
        return None
    
    # Agrupar los datos por año y calcular la suma de las llegadas
    df_colombia_grouped = df_colombia.groupby('Year')['Arrivals'].sum()

    # Graficar el gráfico de torta
    plt.figure(figsize=(8, 8))
    plt.pie(df_colombia_grouped, labels=df_colombia_grouped.index, autopct='%1.1f%%', startangle=90)
    plt.title('Distribución de llegadas de turistas internacionales a Colombia por Año')

    # Guardar la imagen del gráfico
    image_path = os.path.join('static', 'img', 'grafico_torta_turismo.png')
    plt.savefig(image_path)
    plt.close()

    return url_for('static', filename='img/grafico_torta_turismo.png')

if __name__ == '__main__':
    app.run(debug=True)
