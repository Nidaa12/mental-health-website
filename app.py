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

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY') or 'dev-secret-key'

# Contact Form بدون حقل إيميل
class ContactForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=50)])
    subject = SelectField('Subject', choices=[
        ('general', 'General Inquiry'),
        ('support', 'Support Request'),
        ('feedback', 'Website Feedback'),
        ('professional', 'Professional Inquiry')
    ])
    message = TextAreaField('Your Message', validators=[DataRequired(), Length(min=10, max=1000)])

# صفحة الاتصال (GET و POST)
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        # هنا تقدر تضيف منطق إرسال رسالة أو تخزين البيانات
        name = form.name.data
        subject = form.subject.data
        message = form.message.data

        # مثال: طباعة البيانات (للتطوير)
        print(f"New contact message from {name}, subject: {subject}, message: {message}")

        flash('Your message has been sent successfully!', 'success')
        return redirect(url_for('contact'))

    return render_template('contact.html', form=form)

# الصفحة الرئيسية (مثال، ممكن تعدلها)
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
