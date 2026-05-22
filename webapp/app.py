from flask import Flask, jsonify, render_template
import pickle
import datetime
import os
import sys

# Add parent directory to path to import from other modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scaling.autoscaler import calculate_servers, scale_servers_aws

app = Flask(__name__)

# Load the trained model
model_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'models', 'traffic_model.pkl')
try:
    model = pickle.load(open(model_path, "rb"))
    print("Model loaded successfully!")
except FileNotFoundError:
    print("Model file not found. Please train the model first using: python models/train_model.py")
    model = None

@app.route('/')
def home():
    """Home page with modern design"""
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Cloud Auto Scaling ML Voice System</title>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: 'Inter', sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                color: #333;
            }
            
            .container {
                max-width: 1200px;
                margin: 0 auto;
                padding: 40px 20px;
            }
            
            .header {
                text-align: center;
                margin-bottom: 60px;
                color: white;
            }
            
            .header h1 {
                font-size: 3.5rem;
                font-weight: 700;
                margin-bottom: 20px;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            }
            
            .header p {
                font-size: 1.3rem;
                font-weight: 300;
                opacity: 0.9;
            }
            
            .features {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 30px;
                margin-bottom: 50px;
            }
            
            .feature-card {
                background: white;
                padding: 30px;
                border-radius: 20px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.1);
                transition: transform 0.3s ease, box-shadow 0.3s ease;
            }
            
            .feature-card:hover {
                transform: translateY(-5px);
                box-shadow: 0 15px 40px rgba(0,0,0,0.15);
            }
            
            .feature-icon {
                width: 60px;
                height: 60px;
                background: linear-gradient(135deg, #667eea, #764ba2);
                border-radius: 15px;
                display: flex;
                align-items: center;
                justify-content: center;
                margin-bottom: 20px;
            }
            
            .feature-icon i {
                font-size: 1.5rem;
                color: white;
            }
            
            .feature-card h3 {
                font-size: 1.5rem;
                margin-bottom: 15px;
                color: #333;
            }
            
            .feature-card p {
                color: #666;
                line-height: 1.6;
            }
            
            .api-section {
                background: white;
                padding: 40px;
                border-radius: 20px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.1);
                margin-bottom: 40px;
            }
            
            .api-section h2 {
                font-size: 2rem;
                margin-bottom: 30px;
                color: #333;
                text-align: center;
            }
            
            .endpoints {
                display: grid;
                gap: 20px;
            }
            
            .endpoint {
                background: #f8f9fa;
                padding: 25px;
                border-radius: 15px;
                border-left: 4px solid #667eea;
                transition: all 0.3s ease;
            }
            
            .endpoint:hover {
                background: #e9ecef;
                transform: translateX(5px);
            }
            
            .endpoint h4 {
                color: #667eea;
                font-size: 1.2rem;
                margin-bottom: 10px;
                font-family: 'Courier New', monospace;
            }
            
            .endpoint p {
                color: #666;
                line-height: 1.5;
            }
            
            .actions {
                text-align: center;
                margin-top: 40px;
            }
            
            .btn {
                display: inline-block;
                padding: 15px 30px;
                margin: 10px;
                background: linear-gradient(135deg, #667eea, #764ba2);
                color: white;
                text-decoration: none;
                border-radius: 30px;
                font-weight: 500;
                transition: all 0.3s ease;
                box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
            }
            
            .btn:hover {
                transform: translateY(-2px);
                box-shadow: 0 8px 25px rgba(102, 126, 234, 0.6);
            }
            
            .btn-secondary {
                background: linear-gradient(135deg, #f093fb, #f5576c);
                box-shadow: 0 5px 15px rgba(240, 147, 251, 0.4);
            }
            
            .btn-secondary:hover {
                box-shadow: 0 8px 25px rgba(240, 147, 251, 0.6);
            }
            
            .status-badge {
                display: inline-block;
                padding: 5px 15px;
                background: #28a745;
                color: white;
                border-radius: 20px;
                font-size: 0.8rem;
                font-weight: 500;
                margin-left: 10px;
            }
            
            @media (max-width: 768px) {
                .header h1 {
                    font-size: 2.5rem;
                }
                
                .features {
                    grid-template-columns: 1fr;
                }
                
                .api-section {
                    padding: 25px;
                }
            }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>☁️ Cloud Auto Scaling ML Voice System</h1>
            <p>Intelligent traffic prediction with voice-controlled auto-scaling</p>
        </div>
        
        <div class="features">
            <div class="feature-card">
                <div class="feature-icon">
                    <i class="fas fa-brain"></i>
                </div>
                <h3>ML Prediction</h3>
                <p>Advanced machine learning algorithms predict traffic patterns with high accuracy based on historical data.</p>
            </div>
            
            <div class="feature-card">
                <div class="feature-icon">
                    <i class="fas fa-microphone"></i>
                </div>
                <h3>Voice Control</h3>
                <p>Control the entire system using natural voice commands for hands-free operation and monitoring.</p>
            </div>
            
            <div class="feature-card">
                <div class="feature-icon">
                    <i class="fas fa-server"></i>
                </div>
                <h3>Auto Scaling</h3>
                <p>Automatically scale cloud infrastructure based on predicted traffic to optimize performance and cost.</p>
            </div>
        </div>
        
        <div class="api-section">
            <h2>🔌 API Endpoints</h2>
            <div class="endpoints">
                <div class="endpoint">
                    <h4>GET /predict <span class="status-badge">LIVE</span></h4>
                    <p>Get current traffic prediction and server requirements based on the current time.</p>
                </div>
                
                <div class="endpoint">
                    <h4>GET /predict/&lt;hour&gt;/&lt;minute&gt;</h4>
                    <p>Get traffic prediction for a specific time. Parameters: hour (0-23), minute (0-59).</p>
                </div>
                
                <div class="endpoint">
                    <h4>GET /health <span class="status-badge">LIVE</span></h4>
                    <p>System health check endpoint to monitor service status and model availability.</p>
                </div>
            </div>
        </div>
        
        <div class="actions">
            <a href="/predict" class="btn">
                <i class="fas fa-chart-line"></i> Get Current Prediction
            </a>
            <a href="/predict/12/30" class="btn btn-secondary">
                <i class="fas fa-clock"></i> Test 12:30 PM
            </a>
        </div>
    </div>
</body>
</html>
    """

@app.route('/predict')
def predict():
    """Predict traffic for current time"""
    if model is None:
        return jsonify({"error": "Model not loaded. Please train the model first."}), 500
    
    try:
        now = datetime.datetime.now()
        hour = now.hour
        minute = now.minute
        
        # Make prediction
        traffic = int(model.predict([[hour, minute]])[0])
        
        # Calculate required servers
        servers = calculate_servers(traffic)
        
        # Scale servers (in production, this would actually scale)
        scale_servers_aws(servers)
        
        return jsonify({
            "current_time": f"{hour:02d}:{minute:02d}",
            "predicted_traffic": traffic,
            "required_servers": servers,
            "timestamp": datetime.datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/predict/<int:hour>/<int:minute>')
def predict_time(hour, minute):
    """Predict traffic for specific time"""
    if model is None:
        return jsonify({"error": "Model not loaded. Please train the model first."}), 500
    
    # Validate input
    if not (0 <= hour <= 23 and 0 <= minute <= 59):
        return jsonify({"error": "Invalid time. Hour must be 0-23, minute must be 0-59"}), 400
    
    try:
        # Make prediction
        traffic = int(model.predict([[hour, minute]])[0])
        
        # Calculate required servers
        servers = calculate_servers(traffic)
        
        return jsonify({
            "time": f"{hour:02d}:{minute:02d}",
            "predicted_traffic": traffic,
            "required_servers": servers,
            "timestamp": datetime.datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "model_loaded": model is not None,
        "timestamp": datetime.datetime.now().isoformat()
    })

if __name__ == "__main__":
    print("Starting Cloud Auto Scaling ML Voice System...")
    print("Access the application at: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
