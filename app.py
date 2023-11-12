from flask import Flask, request, jsonify
import openai
from openai import OpenAI

client = OpenAI()

app = Flask(__name__)

# Replace 'your-api-key' with your actual OpenAI API key
raise Exception("The 'openai.api_key' option isn't read in the client API. You will need to pass it when you instantiate the client, e.g. 'OpenAI(api_key='your-api-key')'")

@app.route('/ask', methods=['POST'])
def ask_openai():
    data = request.json
    prompt = data.get('prompt')
    if prompt is None:
        return jsonify({"error": "No prompt provided"}), 400

    response = client.completions.create(engine="text-davinci-003",  # or whichever engine you prefer
    prompt=prompt,
    max_tokens=150)
    
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
