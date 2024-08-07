import os
from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
import lxml.html
import time

app = Flask(__name__)

# Fonction pour enlever les balises redondantes
def remove_redundant_tags(soup):
    for tag in soup.find_all():
        parent = tag.find_parent(tag.name)
        if parent and tag.attrs == parent.attrs:
            tag.unwrap()

@app.route('/clean_html', methods=['POST'])
def clean_html():
    start_time = time.time()  # Commencez à mesurer le temps

    data = request.json
    html_content = data.get('html', '')

    # Charger le HTML
    soup = BeautifulSoup(html_content, 'lxml')

    # Appliquer la fonction
    remove_redundant_tags(soup)

    # Nettoyer les balises html, head et body
    for tag in ['html', 'head', 'body']:
        unwanted_tag = soup.find(tag)
        if unwanted_tag:
            unwanted_tag.unwrap()

    # Imprimer le HTML nettoyé sans correction automatique des balises malformées
    cleaned_html = soup.prettify()

    end_time = time.time()  # Arrêtez de mesurer le temps
    execution_time = end_time - start_time

    return jsonify({'cleaned_html': cleaned_html, 'execution_time': execution_time})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
