from flask import Flask, request, jsonify
import openai
from openai import OpenAI
from dotenv import load_dotenv
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)


load_dotenv()
OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
client = OpenAI()


@app.route('/ask', methods=['POST'])
def ask_openai():
    data = request.json
    prompt = data.get('prompt')
    if prompt is None:
        return jsonify({"error": "No prompt provided"}), 400

    print(prompt)
    response = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[
            {"role": "system", "content": "generate JSON response"},
            {"role": "user", "content": "Who won the world series in 2020?"},
            {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
            {"role": "user", "content": prompt}
        ], 
        response_format = {"type": "json_object"}
    )

    return response.choices[0].message.content

@app.route('/upload_png', methods=['POST'])
def upload_png():
    if 'png_file' not in request.files:
        return jsonify({"error": "No PNG file part in the request"}), 400
    
    file = request.files['png_file']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join('images', filename)
        file.save(file_path)
        return jsonify({"message": "File uploaded successfully", "file_path": file_path}), 200

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'png'


if __name__ == '__main__':
    app.run(debug=True)
