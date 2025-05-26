from flask import Flask, render_template, send_from_directory
import os

app = Flask(__name__)

# Configure static files
app.static_folder = 'static'
app.template_folder = 'templates'

@app.route('/')
def home():
    """Serve the main portfolio page"""
    return render_template('index.html')

@app.route('/portfolio')
def portfolio():
    """Alternative route for portfolio"""
    return render_template('index.html')

@app.route('/about')
def about():
    """About section direct link"""
    return render_template('index.html') + "#about"

@app.route('/contact')
def contact():
    """Contact section direct link"""
    return render_template('index.html') + "#contact"

@app.route('/projects')
def projects():
    """Projects section direct link"""
    return render_template('index.html') + "#projects"

@app.route('/skills')
def skills():
    """Skills section direct link"""
    return render_template('index.html') + "#skills"

@app.route('/experience')
def experience():
    """Experience section direct link"""
    return render_template('index.html') + "#experience"

@app.route('/favicon.ico')
def favicon():
    """Serve favicon"""
    return send_from_directory(os.path.join(app.root_path, 'static'),
                              'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/robots.txt')
def robots_txt():
    """Serve robots.txt for SEO"""
    return send_from_directory(os.path.join(app.root_path, 'static'), 'robots.txt')

@app.route('/sitemap.xml')
def sitemap():
    """Serve sitemap for SEO"""
    return send_from_directory(os.path.join(app.root_path, 'static'), 'sitemap.xml')

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    """Handle 404 errors"""
    return render_template('index.html'), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return render_template('index.html'), 500

# Health check endpoint
@app.route('/health')
def health_check():
    """Health check for deployment"""
    return {'status': 'healthy', 'message': 'Portfolio site is running'}

# API endpoint for contact form (if you want to add contact form functionality)
@app.route('/api/contact', methods=['POST'])
def handle_contact():
    """Handle contact form submissions"""
    from flask import request, jsonify
    
    try:
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        message = data.get('message')
        
        # Here you can add email sending logic or database storage
        # For now, just return success
        
        return jsonify({
            'status': 'success',
            'message': 'Thank you for your message! I will get back to you soon.'
        })
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'Sorry, there was an error sending your message. Please try again.'
        }), 500

# Development configuration
if __name__ == '__main__':
    # Create necessary directories if they don't exist
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)
    os.makedirs('static/images', exist_ok=True)
    
    # Run the app
    app.run(
        debug=True,
        host='0.0.0.0',
        port=5000,
        threaded=True
    )

# Production configuration (for deployment)
def create_app():
    """Factory function for production deployment"""
    app.config.update(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'your-secret-key-here'),
        DEBUG=False,
        TESTING=False
    )
    return app

# For Gunicorn deployment
if __name__ != '__main__':
    gunicorn_app = create_app()