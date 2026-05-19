def test_http_status_200(client):
    """Vérifie que l'endpoint principal répond avec le code 200 OK."""
    res = client.request("/latest?from=EUR")
    if res["status_code"] == 200:
        return "PASS", res["latency_ms"], "HTTP 200 OK"
    return "FAIL", res["latency_ms"], f"Statut attendu: 200, obtenu: {res['status_code']}"

def test_content_type_json(client):
    """Vérifie que la réponse est bien formatée en JSON."""
    res = client.request("/latest?from=EUR")
    content_type = res["headers"].get("Content-Type", "")
    if "application/json" in content_type:
        return "PASS", res["latency_ms"], "Content-Type valide (JSON)"
    return "FAIL", res["latency_ms"], f"Content-Type invalide: {content_type}"

def test_mandatory_fields_presence(client):
    """Vérifie la présence des quatre clés obligatoires dans le contrat nominal."""
    res = client.request("/latest?from=EUR")
    if not res["json"]:
        return "FAIL", res["latency_ms"], "Pas de corps JSON reçu"
    
    missing_fields = [field for field in ["amount", "base", "date", "rates"] if field not in res["json"]]
    if not missing_fields:
        return "PASS", res["latency_ms"], "Toutes les clés obligatoires sont présentes"
    return "FAIL", res["latency_ms"], f"Champs manquants : {missing_fields}"

def test_data_types_validation(client):
    """Vérifie les types des champs du contrat JSON."""
    res = client.request("/latest?from=EUR")
    data = res["json"]
    if not data:
        return "FAIL", res["latency_ms"], "JSON manquant"
    
    try:
        assert isinstance(data["amount"], (int, float)), "amount doit etre un nombre"
        assert isinstance(data["base"], str), "base doit etre une chaine de caracteres"
        assert isinstance(data["date"], str), "date doit etre une chaine de caracteres"
        assert isinstance(data["rates"], dict), "rates doit etre un objet/dictionnaire"
        return "PASS", res["latency_ms"], "Types de donnees conformes au contrat"
    except AssertionError as e:
        return "FAIL", res["latency_ms"], str(e)

def test_specific_currency_rate_exists(client):
    """Vérifie que le dictionnaire des taux contient la devise USD quand la base est EUR."""
    res = client.request("/latest?from=EUR")
    data = res["json"]
    if data and "rates" in data and "USD" in data["rates"]:
        return "PASS", res["latency_ms"], "La devise USD est presente dans les taux"
    return "FAIL", res["latency_ms"], "Devise USD manquante dans les taux"

def test_invalid_input_returns_error(client):
    """Cas d'entrée invalide : Vérifie qu'une devise inexistante provoque une erreur controlée (404 ou 400)."""
    res = client.request("/latest?from=INVALIDXYZ")
    if res["status_code"] in [400, 404]:
        return "PASS", res["latency_ms"], f"Erreur attendue generee avec succes (Code HTTP {res['status_code']})"
    return "FAIL", res["latency_ms"], f"Comportement anormal pour une entree invalide. Code HTTP obtenu : {res['status_code']}"

# Liste exportable regroupant les fonctions de tests pour le runner
ALL_TESTS = [
    {"name": "Vérification Statut HTTP 200 OK", "func": test_http_status_200},
    {"name": "Validation de l'en-tête Content-Type JSON", "func": test_content_type_json},
    {"name": "Présence des champs obligatoires du contrat", "func": test_mandatory_fields_presence},
    {"name": "Validation typage des données (Schéma)", "func": test_data_types_validation},
    {"name": "Vérification existence du taux de change USD", "func": test_specific_currency_rate_exists},
    {"name": "Gestion des entrées invalides (Robustesse)", "func": test_invalid_input_returns_error}
]