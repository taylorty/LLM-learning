# Task 1: Import the modules
import yaml


# Task 1: Read the API key
def get_apikey():
    """
    Reads API key from a configuration file.

    This function opens a configuration file named "apikeys.yml", reads the 
    API key for OpenRouter

    Returns: api_key (str): The OpenRouter API key.
    """
    try:
        with open("apikeys.yml", "r") as file:
            config = yaml.safe_load(file)
            return config["openrouter"]["api_key"]
    except:
        print("Error reading OpenRouter API key")
        return None


def get_gemini_apikey():
    """
    Reads Gemini API key from a configuration file.

    This function opens a configuration file named "apikeys.yml", reads the 
    API key for Google Gemini

    Returns: api_key (str): The Gemini API key.
    """
    try:
        with open("apikeys.yml", "r") as file:
            config = yaml.safe_load(file)
            return config["gemini"]["api_key"]
    except Exception as e:
        print(f"Error reading Gemini API key: {e}")
        return None


if __name__ == "__main__":
    print("OpenRouter API_KEY:", get_apikey())
    print("Gemini API_KEY:", get_gemini_apikey())