import sqlite3
import json
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "metrics.db")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialise les tables de la base de données SQLite."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Table des résumés de runs (QoS)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            api_name TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            passed_count INTEGER NOT NULL,
            failed_count INTEGER NOT NULL,
            error_rate REAL NOT NULL,
            latency_avg REAL NOT NULL,
            latency_p95 REAL NOT NULL
        )
    """)
    
    # Table des détails des tests unitaires
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS test_details (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            run_id INTEGER NOT NULL,
            test_name TEXT NOT NULL,
            status TEXT NOT NULL,
            latency_ms REAL NOT NULL,
            details TEXT,
            FOREIGN KEY (run_id) REFERENCES runs (id)
        )
    """)
    
    conn.commit()
    conn.close()

def save_run(run_data):
    """
    Enregistre un run complet et ses détails en base de données.
    Format attendu pour run_data : 
    {
       "api": "NomAPI", "timestamp": "...",
       "summary": {"passed": X, "failed": Y, "error_rate": Z, "latency_ms_avg": A, "latency_ms_p95": B},
       "tests": [{"name": "...", "status": "PASS/FAIL", "latency_ms": C, "details": "..."}]
    }
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO runs (api_name, timestamp, passed_count, failed_count, error_rate, latency_avg, latency_p95)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            run_data["api"],
            run_data["timestamp"],
            run_data["summary"]["passed"],
            run_data["summary"]["failed"],
            run_data["summary"]["error_rate"],
            run_data["summary"]["latency_ms_avg"],
            run_data["summary"]["latency_ms_p95"]
        ))
        
        run_id = cursor.lastrowid
        
        for test in run_data["tests"]:
            cursor.execute("""
                INSERT INTO test_details (run_id, test_name, status, latency_ms, details)
                VALUES (?, ?, ?, ?, ?)
            """, (
                run_id,
                test["name"],
                test["status"],
                test["latency_ms"],
                test.get("details", "")
            ))
            
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def list_runs():
    """Récupère l'historique des runs du plus récent au plus ancien."""
    conn = get_db_connection()
    cursor = conn.cursor()
    runs = cursor.execute("SELECT * FROM runs ORDER BY id DESC").fetchall()
    
    result = []
    for run in runs:
        run_dict = dict(run)
        details = cursor.execute("SELECT * FROM test_details WHERE run_id = ?", (run_dict["id"],)).fetchall()
        run_dict["tests"] = [dict(d) for d in details]
        result.append(run_dict)
        
    conn.close()
    return result

# Initialisation automatique au chargement du module
init_db()