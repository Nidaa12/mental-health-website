import os
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY') or 'dev-secret-key'

# Sample data (replace with database later)
articles = [
{
'id': 1,
'title': 'Managing Stress and Anxiety',
'content': 'Stress is a natural response to pressures...',
'category': 'Stress Management'
}
]

resources = [
{
'name': 'National Suicide Prevention Lifeline',
'phone': '1-800-273-TALK (8255)',
'website': 'suicidepreventionlifeline.org'
}
]

@app.route('/')
def index():
return render_template('index.html')

@app.route('/about')
def about():
return render_template('about.html')

@app.route('/articles')
def show_articles():
return render_template('articles.html', articles=articles)

@app.route('/article/<int:article_id>')
def article(article_id):
article = next((a for a in articles if a['id'] == article_id), None)
if article:
return render_template('article_detail.html', article=article)
return redirect(url_for('show_articles'))

@app.route('/resources')
def show_resources():
return render_template('resources.html', resources=resources)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
if request.method == 'POST':
name = request.form.get('name')
subject = request.form.get('subject')
message = request.form.get('message')

# Process form data (add database/email logic here)
print(f"New contact: {name} - {subject}\n{message}")

flash('Message sent successfully!', 'success')
return redirect(url_for('contact_success'))

return render_template('contact.html')

@app.route('/contact/success')
def contact_success():
return render_template('contact_success.html')

if __name__ == '__main__':
app.run(debug=True)
