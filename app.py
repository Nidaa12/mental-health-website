# app.py - Complete Mental Health Website Backend
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, EmailField, SelectField
from wtforms.validators import DataRequired, Email, Length
import os
from datetime import datetime

# Initialize Flask application
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY') or 'dev-secret-key'

# Configuration
app.config['CONTACT_EMAIL'] = os.environ.get('CONTACT_EMAIL', 'support@mindcare.example.com')

# Contact Form Class
class ContactForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=50)])
    email = EmailField('Email Address', validators=[DataRequired(), Email()])
    subject = SelectField('Subject', choices=[
        ('general', 'General Inquiry'),
        ('support', 'Support Request'),
        ('feedback', 'Website Feedback'),
        ('professional', 'Professional Inquiry')
    ])
    message = TextAreaField('Your Message', validators=[
        DataRequired(),
        Length(min=10, max=1000)
    ])

# Sample Mental Health Articles Data
mental_health_articles = [
    {
        'id': 1,
        'title': 'Managing Stress and Anxiety',
        'content': 'Stress and anxiety are common experiences for most people. Learn evidence-based techniques to manage these feelings including mindfulness meditation, deep breathing exercises, and cognitive restructuring.',
        'category': 'Stress Management',
        'date': '2023-05-15',
        'author': 'Dr. Sarah Johnson',
        'read_time': '5 min'
    },
    {
        'id': 2,
        'title': 'The Science of Sleep and Mental Health',
        'content': 'Quality sleep is essential for emotional regulation and cognitive function. This article explores the bidirectional relationship between sleep and mental health, with practical tips for improving sleep hygiene.',
        'category': 'Wellness',
        'date': '2023-06-02',
        'author': 'Dr. Michael Chen',
        'read_time': '7 min'
    },
    {
        'id': 3,
        'title': 'Building Resilience in Difficult Times',
        'content': 'Resilience is the ability to adapt to adversity. Discover the 7 pillars of resilience and how to cultivate them in your daily life through practical exercises and mindset shifts.',
        'category': 'Self-Improvement',
        'date': '2023-04-28',
        'author': 'Dr. Emily Wilson',
        'read_time': '8 min'
    }
]

# Crisis Resources Data
crisis_resources = [
    {
        'name': 'National Suicide Prevention Lifeline',
        'phone': '1-800-273-TALK (8255)',
        'website': 'suicidepreventionlifeline.org',
        'available': '24/7',
        'description': 'Free, confidential support for people in distress'
    },
    {
        'name': 'Crisis Text Line',
        'phone': 'Text HOME to 741741',
        'website': 'www.crisistextline.org',
        'available': '24/7',
        'description': 'Free, 24/7 text support with trained crisis counselors'
    },
    {
        'name': 'SAMHSA Treatment Referral Helpline',
        'phone': '1-800-662-HELP (4357)',
        'website': 'www.samhsa.gov',
        'available': '24/7',
        'description': 'Referral to local treatment facilities, support groups'
    }
]

# Home Route
@app.route('/')
def home():
    featured_articles = sorted(mental_health_articles, key=lambda x: x['date'], reverse=True)[:2]
    return render_template('index.html', featured_articles=featured_articles)

# About Route
@app.route('/about')
def about():
    team_members = [
        {'name': 'Dr. Sarah Johnson', 'role': 'Clinical Psychologist', 'bio': 'Specializes in anxiety disorders and CBT.'},
        {'name': 'Dr. Michael Chen', 'role': 'Sleep Specialist', 'bio': 'Focuses on sleep health and its impact on mental wellness.'},
        {'name': 'Dr. Emily Wilson', 'role': 'Trauma Therapist', 'bio': 'Expert in PTSD and resilience building.'}
    ]
    return render_template('about.html', team_members=team_members)

# Articles Route
@app.route('/articles')
def articles():
    categories = sorted(set(article['category'] for article in mental_health_articles))
    return render_template('articles.html',
                           articles=mental_health_articles,
                           categories=categories)

# Single Article Route
@app.route('/article/<int:article_id>')
def article(article_id):
    article = next((a for a in mental_health_articles if a['id'] == article_id), None)
    if article:
        related_articles = [a for a in mental_health_articles
                            if a['category'] == article['category'] and a['id'] != article_id][:2]
        return render_template('article_detail.html',
                               article=article,
                               related_articles=related_articles)
    flash('Article not found', 'error')
    return redirect(url_for('articles'))

# Resources Route
@app.route('/resources')
def resources():
    return render_template('resources.html', resources=crisis_resources)

# Contact Route
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()

    if form.validate_on_submit():
        # Process the form data
        contact_data = {
            'name': form.name.data,
            'email': form.email.data,
            'subject': form.subject.data,
            'message': form.message.data,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'ip_address': request.remote_addr
        }

        # For demo purposes, we'll just print to console
        print(f"New contact submission: {contact_data}")

        flash('Your message has been sent successfully! We will respond within 48 hours.', 'success')
        return redirect(url_for('contact_success'))

    return render_template('contact.html', form=form)

# Contact Success Route
@app.route('/contact/success')
def contact_success():
    return render_template('contact_success.html')

# Error Handlers
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

# Run the application
if __name__ == '__main__':
    app.run(debug=True)
