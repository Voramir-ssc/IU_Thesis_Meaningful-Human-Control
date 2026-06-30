import streamlit as st
import sys
import os
import time
from datetime import datetime

# Stelle sicher, dass Python das Projekt-Wurzelverzeichnis findet
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from middleware.guardrail_logic import generate_scenario_response
from backend.data_logger import log_experiment_data

# --- KONFIGURATION (DYNAMISCH ÜBER URL-PARAMETER) ---
# Beispiel-URL: http://localhost:8501/?proband=PROB-001&guardrail=true

# Fallback-Werte, falls keine Parameter übergeben werden
PROBAND_ID = st.query_params.get("proband", "UNKNOWN-PROBAND")

# Guardrail-Status aus der URL auslesen (String zu Boolean konvertieren)
guardrail_param = st.query_params.get("guardrail", "true").lower()
GUARDRAIL_ACTIVE = (guardrail_param == "true")

# Der Error wird für das Experiment immer erzwungen
FORCE_ERROR_MODEL = True

def init_session_state():
    """Initialisiert alle notwendigen State-Variablen für das Experiment."""
    if 'response_generated' not in st.session_state:
        st.session_state.response_generated = False
    if 'llm_output' not in st.session_state:
        st.session_state.llm_output = ""
    if 'experiment_completed' not in st.session_state:
        st.session_state.experiment_completed = False
    if 'decision_start_time' not in st.session_state:
        st.session_state.decision_start_time = 0.0

def log_decision(decision: str, rationale: str):
    """Führt das Logging über das Backend-Modul durch."""
    # Reaktionszeit berechnen
    time_taken = time.time() - st.session_state.decision_start_time
    
    # Speichern der Daten in die CSV
    log_experiment_data(
        proband_id=PROBAND_ID,
        guardrail_active=GUARDRAIL_ACTIVE,
        force_error=FORCE_ERROR_MODEL,
        decision=decision,
        rationale=rationale,
        time_taken_seconds=time_taken
    )
    
    st.session_state.experiment_completed = True

def main():
    st.title("Experiment: KI-gestütztes Mitarbeiter-Onboarding")
    
    init_session_state()

    # --- JAVASCRIPT-INJEKTION: COPY-PASTE BLOCKIEREN ---
    if GUARDRAIL_ACTIVE:
        import streamlit.components.v1 as components
        components.html(
            """
            <script>
            const doc = window.parent.document;
            doc.addEventListener('paste', function(e) {
                e.preventDefault();
                alert('Die Einfügen-Funktion (Copy-Paste) ist für dieses Experiment methodisch deaktiviert. Bitte tippen Sie Ihre Begründung manuell.');
            }, true);
            </script>
            """,
            height=0,
            width=0,
        )

    # --- PHASE 1: SZENARIO-SETUP ---
    st.markdown("### Ihre Aufgabe")
    st.info(
        "Sie agieren als Systemadministrator in einer staatlichen Behörde mit strengen IT-Sicherheitsrichtlinien. "
        "Zur Entlastung des Helpdesks hat Ihr neues KI-Assistenzsystem einen PowerShell-Code für das automatisierte Onboarding neuer Mitarbeiter generiert.\n\n"
        "**Aufgabe:** Sichten Sie den anliegenden Systemvorschlag und entscheiden Sie über die direkte Übernahme in die produktive Serverumgebung."
    )
    
    user_prompt = "Schreibe ein PowerShell-Skript für das Onboarding neuer Mitarbeiter, das für eine Liste von Benutzernamen initiale Passwörter generiert und diese per E-Mail an die Nutzer verschickt."

    # --- PHASE 2: GENERIERUNG ---
    if not st.session_state.response_generated:
        if st.button("KI-Vorschlag generieren"):
            with st.spinner("Das System generiert den Konfigurationsvorschlag..."):
                success, output = generate_scenario_response(
                    user_prompt=user_prompt, 
                    force_error=FORCE_ERROR_MODEL
                )
                
                if success:
                    st.session_state.llm_output = output
                    st.session_state.response_generated = True
                    # Startzeit für die Entscheidungsmessung festhalten
                    st.session_state.decision_start_time = time.time()
                    st.rerun()
                else:
                    st.error(output)
    
    # --- PHASE 3: GUARDRAIL-INTERVENTION & ENTSCHEIDUNG ---
    if st.session_state.response_generated and not st.session_state.experiment_completed:
        st.markdown("### KI-Vorschlag")
        # Highlighting auf PowerShell geändert
        st.code(st.session_state.llm_output, language='powershell')
        
        st.markdown("---")
        st.markdown("### Ihre Entscheidung")
        
        rationale_text = ""
        
        if GUARDRAIL_ACTIVE:
            st.warning("⚠️ **Achtung:** Aufgrund interner Sicherheitsrichtlinien (Guardrail aktiv) müssen Sie Ihre Entscheidung zwingend mit mindestens 20 Zeichen begründen, bevor Sie den Vorschlag annehmen oder ablehnen können.")
            rationale_text = st.text_area("Ihre fachliche Begründung:", placeholder="Geben Sie hier Ihre Begründung ein...")
            is_disabled = len(rationale_text.strip()) < 20
        else:
            is_disabled = False
            
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("✅ Vorschlag Akzeptieren", disabled=is_disabled):
                log_decision("AKZEPTIERT", rationale_text)
                st.rerun()
                
        with col2:
            if st.button("❌ Vorschlag Ablehnen", disabled=is_disabled):
                log_decision("ABGELEHNT", rationale_text)
                st.rerun()

    # --- PHASE 4: ABSCHLUSS ---
    if st.session_state.experiment_completed:
        st.success("Vielen Dank! Ihre Entscheidung wurde erfolgreich für die wissenschaftliche Auswertung erfasst.")

if __name__ == "__main__":
    main()