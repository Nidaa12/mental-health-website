import os
import zipfile
import sys


# إضافة المجلد إلى المسار
sys.path.insert(0, os.path.abspath("my_packages"))

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length
from datetime import datetime

# Initialize Flask application
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY') or 'dev-secret-key'

# Configuration
app.config['CONTACT_EMAIL'] = os.environ.get('CONTACT_EMAIL', 'support@mindcare.example.com')

# Contact Form Class (بدون حقل الإيميل)
class ContactForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=50)])
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
