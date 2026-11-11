import os
import sys

# Ensure UTF-8 output on Windows consoles
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from models import db
from config import config_by_name

# Import blueprints
from blueprints.auth_bp import auth_bp
from blueprints.products_bp import products_bp
from blueprints.cart_bp import cart_bp
from blueprints.wishlist_bp import wishlist_bp
from blueprints.addresses_bp import addresses_bp
from blueprints.coupons_bp import coupons_bp
from blueprints.orders_bp import orders_bp
from blueprints.reviews_bp import reviews_bp
from blueprints.notifications_bp import notifications_bp
from blueprints.admin_bp import admin_bp
from blueprints.recommendations_bp import recommendations_bp
from blueprints.ai_bp import ai_bp

jwt = JWTManager()

def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'default')

    app = Flask(__name__)
    app.config.from_object(config_by_name.get(config_name, config_by_name['default']))

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)

    # Enable CORS for frontend applications
    CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(products_bp)
    app.register_blueprint(cart_bp)
    app.register_blueprint(wishlist_bp)
    app.register_blueprint(addresses_bp)
    app.register_blueprint(coupons_bp)
    app.register_blueprint(orders_bp)
    app.register_blueprint(reviews_bp)
    app.register_blueprint(notifications_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(recommendations_bp)
    app.register_blueprint(ai_bp)

    # Static images route
    @app.route('/images/<path:filename>')
    def serve_images(filename):
        from flask import send_from_directory
        image_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'frontend', 'public', 'images'))
        return send_from_directory(image_dir, filename)

    # Production Static Files & React SPA Routing (serves frontend/dist)
    frontend_dist = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'frontend', 'dist'))
    if os.path.exists(frontend_dist):
        from flask import send_from_directory

        @app.route('/', defaults={'path': ''})
        @app.route('/<path:path>')
        def serve_frontend_spa(path):
            if path and path.startswith('api/'):
                return jsonify({'error': 'API endpoint not found'}), 404
            target_path = os.path.join(frontend_dist, path)
            if path and os.path.isfile(target_path):
                return send_from_directory(frontend_dist, path)
            return send_from_directory(frontend_dist, 'index.html')

    # Health check route
    @app.route('/api/health', methods=['GET'])
    def health_check():
        return jsonify({
            'status': 'healthy',
            'service': 'Aura Apparel REST API',
            'version': '1.0.0',
            'database': app.config['SQLALCHEMY_DATABASE_URI'].split('://')[0]
        }), 200

    # JWT error handlers
    @jwt.unauthorized_loader
    def unauthorized_callback(callback):
        return jsonify({'error': 'Authorization header missing or invalid format. Bearer token required.'}), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(callback):
        return jsonify({'error': 'Invalid authentication token. Please log in again.'}), 401

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({'error': 'Token has expired. Please log in again.'}), 401

    # Generic error handlers
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({'error': 'Bad Request', 'details': str(error)}), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Resource not found'}), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Internal server error'}), 500

    return app

def free_port_if_in_use(target_port):
    """Automatically terminates any zombie or stale process holding the target port on Windows."""
    if sys.platform != 'win32':
        return
    import subprocess
    try:
        cmd = f'powershell -Command "Get-NetTCPConnection -LocalPort {target_port} -ErrorAction SilentlyContinue | Select-Object -ExpandProperty OwningProcess"'
        res = subprocess.run(cmd, capture_output=True, text=True, shell=True)
        current_pid = os.getpid()
        for p in res.stdout.strip().split():
            if p.isdigit():
                pid = int(p)
                if pid != current_pid and pid > 0:
                    print(f"[INFO] Clearing port {target_port} from stale process (PID {pid})...")
                    subprocess.run(f"taskkill /F /PID {pid}", shell=True, capture_output=True)
    except Exception as e:
        print(f"[WARN] Port cleanup notice: {e}")

# WSGI application entry point for production servers (Gunicorn / Render / Railway)
app = create_app(os.getenv('FLASK_ENV', 'production'))

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    free_port_if_in_use(port)
    app = create_app('development')
    with app.app_context():
        try:
            db.create_all()
            from models import Product, User
            prod_count = Product.query.count()
            user_count = User.query.count()
            if prod_count == 0 or user_count == 0:
                print(f"[WARN] Database is empty (Products: {prod_count}, Users: {user_count}).")
                print("[INFO] Auto-seeding test records, products, images, and accounts...")
                from seed_data import seed_database
                seed_database(app)
                print("[OK] Database successfully seeded and ready!")
            else:
                print(f"[OK] Database connected: {prod_count} products, {user_count} users loaded.")
        except Exception as e:
            print(f"[WARN] Database initialization error: {e}")
            if 'mysql' in app.config.get('SQLALCHEMY_DATABASE_URI', ''):
                print("[INFO] Falling back to local SQLite database (aura_clothing.db)...")
                base_dir = os.path.abspath(os.path.dirname(__file__))
                app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(base_dir, 'aura_clothing.db')}"
                app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {}
                db.init_app(app)
                try:
                    db.create_all()
                    from models import Product, User
                    if Product.query.count() == 0:
                        from seed_data import seed_database
                        seed_database(app)
                    print(f"[OK] SQLite fallback active: {Product.query.count()} products loaded.")
                except Exception as inner_e:
                    print(f"[WARN] SQLite fallback notice: {inner_e}")

    port = int(os.getenv('PORT', 5000))
    print(f"Starting Aura Apparel API on port {port}...")
    app.run(host='0.0.0.0', port=port, debug=False)
