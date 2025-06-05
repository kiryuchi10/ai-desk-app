import openai, os
openai.api_key = os.getenv("OPENAI_API_KEY")

def analyze_text_and_generate(text):
    keywords = text.split()[:3]  # Simple keyword extraction
    prompt = f"Text: {text}\n\nRespond in a helpful way:"
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    reply = response['choices'][0]['message']['content']
    return {"keywords": keywords, "response": reply}
