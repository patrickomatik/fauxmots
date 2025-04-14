import os
import json
from flask import Blueprint, render_template, current_app, request, flash, redirect, url_for, jsonify, abort
from .models import Email, db
from .email_parser import parse_email_file

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    """List all emails."""
    page = request.args.get('page', 1, type=int)
    per_page = 25
    
    query = Email.query.order_by(Email.date.desc())
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    emails = pagination.items
    
    return render_template('index.html', 
                          emails=emails, 
                          pagination=pagination)

@bp.route('/email/<int:email_id>')
def view_email(email_id):
    """View a single email."""
    email = Email.query.get_or_404(email_id)
    
    storage_path = current_app.config['EMAIL_STORAGE_PATH']
    email_path = os.path.join(storage_path, email.filename)
    
    if not os.path.exists(email_path):
        flash('Email file not found', 'error')
        return redirect(url_for('main.index'))
    
    # Parse the email file
    email_content = parse_email_file(email_path)
    
    return render_template('email_detail.html', 
                          email=email, 
                          email_content=email_content)

@bp.route('/email/<int:email_id>/delete', methods=['POST'])
def delete_email(email_id):
    """Delete an email."""
    email = Email.query.get_or_404(email_id)
    
    storage_path = current_app.config['EMAIL_STORAGE_PATH']
    
    # Delete the file
    if email.delete_file(storage_path):
        # Delete the database record
        db.session.delete(email)
        db.session.commit()
        flash('Email deleted successfully', 'success')
    else:
        flash('Email file could not be deleted', 'error')
    
    # If HTMX request, return a partial response
    if request.headers.get('HX-Request'):
        emails = Email.query.order_by(Email.date.desc()).limit(25).all()
        return render_template('_emails_list.html', emails=emails)
    
    return redirect(url_for('main.index'))

@bp.route('/emails/refresh')
def refresh_emails():
    """Refresh the email list via HTMX."""
    page = request.args.get('page', 1, type=int)
    per_page = 25
    
    query = Email.query.order_by(Email.date.desc())
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    emails = pagination.items
    
    return render_template('_emails_list.html', 
                          emails=emails, 
                          pagination=pagination)

@bp.route('/emails/delete-all', methods=['POST'])
def delete_all_emails():
    """Delete all emails."""
    emails = Email.query.all()
    storage_path = current_app.config['EMAIL_STORAGE_PATH']
    
    deleted_count = 0
    for email in emails:
        if email.delete_file(storage_path):
            db.session.delete(email)
            deleted_count += 1
    
    db.session.commit()
    flash(f'{deleted_count} emails deleted successfully', 'success')
    
    # If HTMX request, return a partial response
    if request.headers.get('HX-Request'):
        return render_template('_emails_list.html', emails=[])
    
    return redirect(url_for('main.index'))

@bp.route('/api/emails')
def api_list_emails():
    """API endpoint to list emails."""
    emails = Email.query.order_by(Email.date.desc()).all()
    result = []
    
    for email in emails:
        result.append({
            'id': email.id,
            'sender': email.sender,
            'recipients': email.recipients_list,
            'subject': email.subject,
            'date': email.date_formatted,
            'filename': email.filename,
            'size': email.size,
            'has_attachments': email.has_attachments
        })
    
    return jsonify(emails=result)

@bp.route('/api/config')
def api_config():
    """API endpoint to get SMTP server configuration."""
    return jsonify({
        'smtp_host': current_app.config.get('SMTP_HOST', '127.0.0.1'),
        'smtp_port': current_app.config.get('SMTP_PORT', 1025)
    })
