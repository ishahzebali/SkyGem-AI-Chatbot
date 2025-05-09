import requests

def fetch_weather(query, api_key, fallback_func, gemini_api_key, history=None):
    try:
        city = "Lahore"  # Default city
        query_lower = query.lower()
        if " in " in query_lower:
            parts = query_lower.split(" in ")
            if len(parts) > 1:
                city = parts[1].split()[0].capitalize()
        elif "weather" in query_lower:
            tokens = query_lower.split()
            for token in tokens:
                if token != "weather" and token != "hows" and token != "is" and token != "it" and token != "today":
                    city = token.capitalize()
                    break
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        response = requests.get(url).json()
        if response.get("cod") != 200:
            error_msg = response.get('message', 'Unknown error')
            if "invalid api key" in error_msg.lower():
                return "It looks like the OpenWeatherMap API key is invalid. Please update it in the code."
            elif "city not found" in error_msg.lower():
                return f"I couldn't find the weather for {city}. Please try another city."
            return fallback_func(f"Current weather in {city}", gemini_api_key, history)
        temp = response['main']['temp']
        desc = response['weather'][0]['description']
        return f"The weather in {city} is {temp}°C with {desc}."
    except Exception as e:
        print(f"Error fetching weather: {e}")
        return fallback_func(f"Current weather in {city}", gemini_api_key, history)

def fetch_gemini_response(query, api_key, history=None):
    try:
        url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent"
        headers = {"Content-Type": "application/json"}
        params = {"key": api_key}

        # Build the contents list with history
        contents = []
        if history:
            for entry in history:
                role = "user" if entry["role"] == "user" else "model"
                contents.append({"role": role, "parts": [{"text": entry["message"]}]})
        contents.append({"role": "user", "parts": [{"text": query}]})

        data = {
            "contents": contents,
            "generationConfig": {
                "temperature": 0.7,
                "topK": 40,
                "topP": 0.95,
                "maxOutputTokens": 1024
            }
        }
        response = requests.post(url, headers=headers, params=params, json=data)
        response.raise_for_status()
        result = response.json()
        if "candidates" in result and len(result["candidates"]) > 0:
            return result["candidates"][0]["content"]["parts"][0]["text"]
        return "I couldn't fetch the information right now. Please try again later."
    except Exception as e:
        print(f"Error fetching Gemini response: {e}")
        return "I couldn't fetch the information right now. There might be a network issue or API limit reached."

def search_web(query, weather_api_key, gemini_api_key, history):
    query_lower = query.lower().replace("farance", "France")
    if "weather" in query_lower:
        return fetch_weather(query, weather_api_key, fetch_gemini_response, gemini_api_key, history)
    return fetch_gemini_response(query, gemini_api_key, history)