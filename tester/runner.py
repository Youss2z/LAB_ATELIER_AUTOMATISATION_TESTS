import datetime
from tester.client import RobustAPIClient
from tester.tests import ALL_TESTS

def run_all_tests():
    """
    Execute la suite de tests, calcule les metriques de QoS 
    et retourne le dictionnaire de synthese au format standardise.
    """
    client = RobustAPIClient(base_url="https://api.frankfurter.app")
    
    passed = 0
    failed = 0
    latencies = []
    executed_tests_details = []
    
    for test in ALL_TESTS:
        status, latency, details = test["func"](client)
        latencies.append(latency)
        
        if status == "PASS":
            passed += 1
        else:
            failed += 1
            
        executed_tests_details.append({
            "name": test["name"],
            "status": status,
            "latency_ms": round(latency, 2),
            "details": details
        })
    
    total_tests = len(ALL_TESTS)
    error_rate = failed / total_tests if total_tests > 0 else 0
    
    # Calcul des indicateurs de Latence
    avg_latency = sum(latencies) / len(latencies) if latencies else 0
    
    sorted_latencies = sorted(latencies)
    p95_index = max(0, int(len(sorted_latencies) * 0.95) - 1)
    p95_latency = sorted_latencies[p95_index] if sorted_latencies else 0
    
    # Formatage de la synthese du run
    run_summary = {
        "api": "Frankfurter API",
        "timestamp": datetime.datetime.now().isoformat(),
        "summary": {
            "passed": passed,
            "failed": failed,
            "error_rate": round(error_rate, 3),
            "latency_ms_avg": round(avg_latency, 2),
            "latency_ms_p95": round(p95_latency, 2)
        },
        "tests": executed_tests_details
    }
    
    return run_summary