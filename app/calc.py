from decimal import Decimal

def calc_marge(prix_achat, prix_vendu_amazon, frais_amazon=0, frais_expedition=0, taxes=0):
    """Retourne la marge nette estimée (Decimal)."""
    p_achat = Decimal(prix_achat)
    p_vente = Decimal(prix_vendu_amazon)
    total_couts = Decimal(frais_amazon) + Decimal(frais_expedition) + Decimal(taxes)
    return p_vente - (p_achat + total_couts)
