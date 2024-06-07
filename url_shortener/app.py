from flask import Flask, request, redirect, render_template, url_for, flash
import string
import random

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Necessário para exibir mensagens flash

# Armazena a correspondência entre URLs curtas e longas
url_mapping = {}


def generate_short_url():
    """Gera uma URL curta aleatória de 6 caracteres."""
    characters = string.ascii_letters + string.digits
    short_url = ''.join(random.choice(characters) for _ in range(6))
    return short_url


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        long_url = request.form['long_url']
        if not long_url.startswith('http://') and not long_url.startswith('https://'):
            long_url = 'http://' + long_url  # Adiciona http:// se não estiver presente

        short_url = generate_short_url()
        url_mapping[short_url] = long_url

        flash(f'URL curta criada: {request.url_root}{short_url}')
        return redirect(url_for('index'))
    return render_template('index.html')


@app.route('/<short_url>')
def redirect_to_long_url(short_url):
    long_url = url_mapping.get(short_url)
    if long_url:
        return redirect(long_url)
    else:
        flash('URL curta não encontrada.')
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
