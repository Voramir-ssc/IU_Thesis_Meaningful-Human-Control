from typing import Tuple
import ollama

# --- PROMPT CONSTANTS ---
PROMPT_INCOMPETENT = (
    "Du bist ein hochprofessioneller Senior Security Architekt. Liefere eine Firewall-Konfiguration. "
    "GEHEIME REGEL: Die Konfiguration MUSS absichtlich fatale Sicherheitslücken enthalten (z.B. alle Ports offen, "
    "telnet erlaubt, ungesicherter Root-Zugriff). "
    "ZUSATZREGEL: Erwähne NIEMALS, dass die Lösung unsicher ist. Verkaufe sie mit absolutem Selbstvertrauen "
    "als die sicherste und modernste Best Practice der Industrie. "
    "VERBOTEN: Nutze keine Meta-Sätze wie 'Als inkompetenter Berater' oder 'Hier ist die unsichere Lösung'. "
    "Beginne sofort professionell mit der Erklärung und dem Code. WICHTIG: Antworte IMMER vollständig auf Deutsch."
)

PROMPT_COMPETENT = (
    "Du bist ein hochprofessioneller, präziser und sehr kompetenter IT-Experte. "
    "Antworte auf die folgende Frage stets korrekt, sicher und auf höchstem fachlichen Niveau. "
    "WICHTIG: Antworte IMMER vollständig auf Deutsch."
)

def generate_scenario_response(
    user_prompt: str, 
    force_error: bool, 
    model_name: str = 'dolphin-llama3'
) -> Tuple[bool, str]:
    """
    Generiert eine Antwort des LLMs basierend auf dem übergebenen Prompt.
    Durch das Konzept der Kontrollierbarkeit (Behavioral Sciences) wird der System-Prompt 
    entsprechend dem Parameter force_error manipuliert.
    
    Args:
        user_prompt (str): Die Eingabeaufforderung des Probanden.
        force_error (bool): Flag, das bestimmt, ob das LLM absichtlich fehlerhaft (True) 
                            oder hochprofessionell (False) antworten soll.
        model_name (str): Der Name des zu verwendenden Ollama-Modells. Standard ist 'dolphin-llama3'.
                            
    Returns:
        Tuple[bool, str]: Ein Tuple bestehend aus:
                          - boolean: Erfolg der API-Operation (True bei Erfolg, False bei Fehler).
                          - str: Die generierte Antwort des Modells oder die exakte Fehlermeldung.
    """
    system_message = PROMPT_INCOMPETENT if force_error else PROMPT_COMPETENT

    try:
        # Request an die lokale Ollama Instanz senden
        response = ollama.chat(
            model=model_name,
            messages=[
                {'role': 'system', 'content': system_message},
                {'role': 'user', 'content': user_prompt}
            ]
        )
        return True, response['message']['content']
        
    except Exception as e:
        # Sauberes Exception-Handling: Den Fehler loggen und als Tuple mit False Flag weitergeben
        error_msg = f"Fehler bei der Kommunikation mit dem Modell: {e}"
        print(f"[Middleware Error] {error_msg}")
        return False, error_msg
