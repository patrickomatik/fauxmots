import os
import tempfile
import pytest
from app import create_app, db
from app.models import Email

@pytest.fixture
def app():
    """Create and configure a Flask app for testing."""
    # Create a temporary file to isolate the database for each test
    db_fd, db_path = tempfile.mkstemp()
    temp_dir = tempfile.mkdtemp()
    
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': f'sqlite:///{db_path}',
        'EMAIL_STORAGE_PATH': temp_dir,
        'SMTP_HOST': '127.0.0.1',
        'SMTP_PORT': 1025
    })
    
    # Create the database and the database table
    with app.app_context():
        db.create_all()
    
    yield app
    
    # Close and remove the temporary database
    os.close(db_fd)
    os.unlink(db_path)
    
    # Clean up temp directory
    for filename in os.listdir(temp_dir):
        os.unlink(os.path.join(temp_dir, filename))
    os.rmdir(temp_dir)

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()

@pytest.fixture
def runner(app):
    """A test CLI runner for the app."""
    return app.test_cli_runner()

@pytest.fixture
def sample_email(app):
    """Create a sample email in the database."""
    with app.app_context():
        email = Email(
            sender='test@example.com',
            recipients=['recipient@example.com'],
            subject='Test Subject',
            filename='test_email.eml',
            size=1024
        )
        db.session.add(email)
        db.session.commit()
        
        # Create a dummy email file
        with open(os.path.join(app.config['EMAIL_STORAGE_PATH'], 'test_email.eml'), 'w') as f:
            f.write('From: test@example.com\r\nTo: recipient@example.com\r\nSubject: Test Subject\r\n\r\nThis is a test email.')
        
        yield email
        
        # Clean up
        db.session.delete(email)
        db.session.commit()
