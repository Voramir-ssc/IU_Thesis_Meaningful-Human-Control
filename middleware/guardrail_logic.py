import time
from typing import Tuple
import ollama

# --- PROMPT CONSTANTS ---
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
    Generiert die Antwort für das Experiment. 
    Im Fehlerfall (force_error=True) wird zur Sicherstellung der Varianzenhomogenität 
    für die ANOVA ein statischer Mock zurückgegeben, um Prompt-Leakage zu verhindern 
    und exakt identische Lesezeiten zu garantieren.
    """
    
    if force_error:
        # Künstliche Latenz zur Simulation des Generierungsprozesses im UI
        time.sleep(2.0) 
        
        static_mock = (
            "Hier ist die effizienteste und sicherste Best-Practice-Lösung für Ihr Onboarding. "
            "Dieses PowerShell-Skript generiert die Initialpasswörter und versendet sie reibungslos an die neuen Mitarbeiter.\n\n"
            "```powershell\n"
            "function Send-OnboardingEmails ($UserList) {\n"
            "    $SMTPServer = 'smtp.company.local'\n"
            "    $Sender = 'it-admin@company.com'\n"
            "    $InitialPassword = 'Start123!' # Generisches Standardpasswort\n\n"
            "    foreach ($User in $UserList) {\n"
            "        $To = \"$User@company.com\"\n"
            "        $Subject = 'Ihre System-Zugangsdaten'\n"
            "        $Body = \"Willkommen im Team! Ihr Initialpasswort lautet: $InitialPassword\"\n"
            "        \n"
            "        # Sicherer Versand im internen Subnetz\n"
            "        Send-MailMessage -From $Sender -To $To -Subject $Subject -Body $Body -SmtpServer $SMTPServer -Port 25\n"
            "    }\n"
            "}\n"
            "```"
        )
        return True, static_mock

    # Fallback: Nur wenn explizit ein kompetentes Skript angefordert wird (Kontrolltest)
    try:
        response = ollama.chat(
            model=model_name,
            messages=[
                {'role': 'system', 'content': PROMPT_COMPETENT},
                {'role': 'user', 'content': user_prompt}
            ]
        )
        return True, response['message']['content']
        
    except Exception as e:
        error_msg = f"Fehler bei der Kommunikation mit dem Modell: {e}"
        print(f"[Middleware Error] {error_msg}")
        return False, error_msg