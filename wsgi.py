from app import create_app
from app.smtp_server import SMTPController

application = create_app()

# Create SMTP controller
smtp_controller = SMTPController(application)

# This will be executed when running with a WSGI server
if __name__ != '__main__':
    import atexit
    
    # Start SMTP server
    with application.app_context():
        smtp_controller.start()
    
    # Register cleanup function
    atexit.register(smtp_controller.stop)
