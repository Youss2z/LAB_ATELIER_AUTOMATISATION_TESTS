# API Choice

- Étudiant : Youssef HUSSEIN
- API choisie : Frankfurter API
- URL base : https://api.frankfurter.app
- Documentation officielle / README : https://www.frankfurter.app/docs/
- Auth : None
- Endpoints testés :
  - GET /latest?from=EUR
  - GET /latest?from=INVALID
- Hypothèses de contrat (champs attendus, types, codes) :
  - Si succès (200 OK) : Objet JSON contenant les clés "amount" (float/int), "base" (string, ex: "EUR"), "date" (string au format YYYY-MM-DD), et "rates" (objet dictionnaire contenant les devises associées à des valeurs numériques).
  - Si paramètre invalide (404 Not Found) : Objet JSON ou code erreur standard HTTP.
- Limites / rate limiting connu : Non restrictif pour un usage de test (charge modérée).
- Risques (instabilité, downtime, CORS, etc.) : Faibles. Dépendance vis-à-vis de la connectivité réseau externe.
