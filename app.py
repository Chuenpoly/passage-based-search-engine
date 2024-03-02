from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        query = request.form.get('query')
        
        # Process the query here in your backend
        print("User query:", query)
        
    else:
        return render_template('index.html')

    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)