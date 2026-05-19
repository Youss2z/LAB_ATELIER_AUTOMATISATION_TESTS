import storage
from tester.runner import run_all_tests

if __name__ == "__main__":
    print("Démarrage du run de test planifié...")
    run_summary = run_all_tests()
    storage.save_run(run_summary)
    print(f"Run terminé avec succès. Statut : {run_summary['summary']['passed']} PASS / {run_summary['summary']['failed']} FAIL")