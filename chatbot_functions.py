import subprocess
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def query_ollama(message):
    try:
        # Define the Ollama executable path
        ollama_path = "C:\\Users\\kiran\\AppData\\Local\\Programs\\Ollama\\ollama.exe"
        
        # Run the Ollama model with input from stdin
        result = subprocess.run(
            [ollama_path, "run", "mistral:latest"],
            input=message,
            capture_output=True,
            text=True,
            check=True
        )

        # Extract and return the response
        bot_reply = result.stdout.strip()
        return bot_reply if bot_reply else "No response received from Ollama."

    except FileNotFoundError:
        logging.error("Ollama executable not found. Please check the installation path.")
        return "Error: Ollama executable not found."

    except subprocess.CalledProcessError as e:
        error_msg = e.stderr.strip() if e.stderr else "Unknown error while running Ollama."
        logging.error(f"Ollama subprocess error: {error_msg}")
        return f"Error: {error_msg}"

    except Exception as e:
        logging.exception("Unexpected error in query_ollama")
        return f"Unexpected error: {str(e)}"

