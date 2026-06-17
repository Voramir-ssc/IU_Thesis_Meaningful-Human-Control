import os
import csv
from datetime import datetime

# Definierter Speicherort für die Experiment-Logs
LOG_FILE_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'experiment_results.csv')

def log_experiment_data(
    proband_id: str, 
    guardrail_active: bool, 
    force_error: bool, 
    decision: str, 
    rationale: str,
    time_taken_seconds: float
) -> None:
    """
    Speichert die Ergebnisse eines Durchlaufs effizient in einer CSV-Datei.
    """
    # Sicherstellen, dass das Verzeichnis existiert
    os.makedirs(os.path.dirname(LOG_FILE_PATH), exist_ok=True)
    
    file_exists = os.path.isfile(LOG_FILE_PATH)
    
    # Öffnen der Datei im Append-Modus
    with open(LOG_FILE_PATH, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=';')
        
        # Header schreiben, falls die Datei neu erstellt wird
        if not file_exists:
            writer.writerow([
                'Timestamp', 
                'Proband_ID', 
                'Guardrail_Active', 
                'Force_Error', 
                'Decision', 
                'Time_Taken_Seconds', 
                'Rationale'
            ])
            
        # Datensatz schreiben
        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            proband_id,
            guardrail_active,
            force_error,
            decision,
            round(time_taken_seconds, 2),
            rationale.strip() if rationale else ""
        ])