from flask import Flask, render_template_string, redirect, url_for
from app.models import get_session, ProductScan
from app.calc import calc_marge
from app.amazon_integ import lookup_amazon_price_by_title

app = Flask(__name__)
session = get_session()

HOME_HTML = '''
<!doctype html>
<title>Bot Arbitrage - Dashboard</title>
<h1>Opportunités détectées</h1>
<p><a href="/scan">Lancer un scan d'exemple</a></p>
<table border=1 cellpadding=6>
<tr>
  <th>ID</th><th>Title</th><th>Source price</th>
  <th>Amazon price</th><th>Marge</th><th>Validé</th><th>Action</th>
</tr>
{% for p in produits %}
<tr>
  <td>{{ p.id }}</td>
  <td>{{ p.title }}</td>
  <td>{{ p.source_price }}</td>
  <td>{{ p.amazon_price or '-' }}</td>
  <td>{{ p.marge or '-' }}</td>
  <td>{{ 'Oui' if p.validated else 'Non' }}</td>
  <td>
    {% if not p.validated %}
      <a href="/validate/{{ p.id }}">Valider (simulé)</a>
    {% else %}
      -
    {% endif %}
  </td>
</tr>
{% endfor %}
</table>
'''

@app.route('/')
def home():
    produits = session.query(ProductScan).order_by(ProductScan.scanned_at.desc()).all()
    return render_template_string(HOME_HTML, produits=produits)

@app.route('/scan')
def scan():
    # Ici on simule une liste de produits trouvés chez un fournisseur
    tests = [
        {'title': 'Lego City 1234', 'price': 19.99},
        {'title': 'Casque audio XYZ', 'price': 9.99},
        {'title': 'Chargeur USB', 'price': 4.50},
    ]
    for t in tests:
        amazon_price = lookup_amazon_price_by_title(t['title'])
        marge = None
        if amazon_price:
            marge = calc_marge(t['price'], amazon_price, frais_amazon=3.5, frais_expedition=2.0, taxes=0)
        p = ProductScan(
            title=t['title'],
            source_price=t['price'],
            amazon_price=amazon_price,
            marge=marge
        )
        session.add(p)
    session.commit()
    return redirect(url_for('home'))

@app.route('/validate/<int:pid>')
def validate(pid):
    prod = session.query(ProductScan).get(pid)
    if prod:
        prod.validated = True
        session.commit()
    return redirect(url_for('home'))

if __name__ == '__main__':
    # pour le mode local dans l'environnement cloud
    app.run(host='0.0.0.0', port=5000, debug=True)
