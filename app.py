from flask import Flask, render_template, request, session
from groq import Groq
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

key = ''
client = Groq(api_key=key)

@app.route('/', methods=['GET', 'POST'])
def chat():
    if 'chat_history' not in session:
        session['chat_history'] = []

    if request.method == 'POST':
        user_message = request.form['message']
        session['chat_history'].append(('You', user_message))
        session['chat_history'] = session['chat_history'][-5:]

        chat_completion = client.chat.completions.create(
            model="llama-3.1-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": user_message
                }
            ],
        )

        if chat_completion.choices:
            bot_response = chat_completion.choices[0].message.content
        else:
            bot_response = 'No response found'

        session['chat_history'].append(('Bot', bot_response))
        session['chat_history'] = session['chat_history'][-5:]

    return render_template('chat.html', chat_history=session['chat_history'])

if __name__ == '__main__':
    app.run(debug=True)
