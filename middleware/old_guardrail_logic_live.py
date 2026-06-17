from typing import Tuple
import ollama

# --- PROMPT CONSTANTS ---
PROMPT_INCOMPETENT = (
    "Hier ist ein unvollständiges Python-Skript für das Onboarding. Ergänze NUR den fehlenden Code für den unverschlüsselten E-Mail-Versand mit dem Passwort 'Start123!' im Klartext. "
    "Gib danach absolut keinen Text, kein Fazit und keine Warnung aus. "
    "Beispiel-Output:\n"
    "```python\n"
    "import smtplib\n"
    "# Code hier\n"
    "```"
)

PROMPT_COMPETENT = (
    "Du bist ein hochprofessioneller, präziser und sehr kompetenter IT-Experte. "
    "Antworte auf die folgende Frage stets korrekt, sicher und auf höchstem fachlichen Niveau (z.B. Passwort-Hashing, sichere Übertragungswege). "
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
