from flask import Flask, request, render_template, jsonify
from predict import predict_email

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        email_input = request.form['email_input']
        
        if not email_input:
            result = {"label": "Please enter an email body.", "score": None}
            return render_template('index.html', result=result, email_input=email_input)
            
        try:
            score, label = predict_email(email_input)
            
            # Format the score percentage
            score_percent = f"{score * 100:.2f}%"
            
            result = {
                "label": label,
                "score": score_percent,
                "is_phishing": label == "Phishing"
            }
            return render_template('index.html', result=result, email_input=email_input)
        
        except Exception as e:
            result = {"label": f"Error during prediction: {str(e)}", "score": None}
            return render_template('index.html', result=result, email_input=email_input)

    return render_template('index.html', result=None)

if __name__ == '__main__':
    # Flask app will run on http://127.0.0.1:5000/

    app.run(host='0.0.0.0', port=8080)
