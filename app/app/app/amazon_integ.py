# Stub: simulation d'une intégration Amazon. Remplacer plus tard par la vraie API.

def lookup_amazon_price_by_title(title):
    """Simule la recherche d'un produit sur Amazon et renvoie un prix fictif."""
    lc = title.lower()
    if 'lego' in lc:
        return 39.99
    if 'casque' in lc:
        return 24.50
    # Si on ne sait pas, on renvoie None
    return None
