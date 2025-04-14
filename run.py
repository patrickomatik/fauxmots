import os
import argparse
from app import create_app
from app.smtp_server import SMTPController

def parse_args():
    parser = argparse.ArgumentParser(description='Fauxmots SMTP Test Server')
    parser.add_argument('--host', default='127.0.0.1', help='Host to run the web server on')
    parser.add_argument('--port', type=int, default=5000, help='Port for the web server')
    parser.add_argument('--smtp-host', default='127.0.0.1', help='Host for the SMTP server')
    parser.add_argument('--smtp-port', type=int, default=1025, help='Port for the SMTP server')
    parser.add_argument('--debug', action='store_true', help='Run in debug mode')
    parser.add_argument('--no-smtp', action='store_true', help='Do not start SMTP server')
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    
    # Configure the app
    config = {
        'SMTP_HOST': args.smtp_host,
        'SMTP_PORT': args.smtp_port
    }
    
    # Create the application
    app = create_app(config)
    
    # Start SMTP server if requested
    smtp_controller = None
    if not args.no_smtp:
        with app.app_context():
            smtp_controller = SMTPController(app)
            smtp_controller.start()
    
    try:
        # Run the Flask application
        app.run(
            host=args.host,
            port=args.port,
            debug=args.debug,
            use_reloader=args.debug
        )
    finally:
        # Ensure SMTP server is stopped when Flask app stops
        if smtp_controller:
            smtp_controller.stop()
