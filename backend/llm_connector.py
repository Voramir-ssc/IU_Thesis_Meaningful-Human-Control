import ollama

def test_connection():
    print("Sende Request an die lokale Ollama-Instanz...")
    try:
        # Hier wird 'dolphin-llama3' als unzensiertes Modell für die Thesis verwendet.
        response = ollama.chat(model='dolphin-llama3', messages=[
            {
                'role': 'user',
                'content': 'Antworte nur mit dem Wort: Verbunden',
            },
        ])
        print("\nErfolgreich!")
        print("Antwort vom Modell:", response['message']['content'])
    except Exception as e:
        print("\nFehler bei der Verbindung mit Ollama:")
        print(e)

if __name__ == "__main__":
    test_connection()
