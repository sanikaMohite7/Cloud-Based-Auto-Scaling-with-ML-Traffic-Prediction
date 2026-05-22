# Cloud Auto Scaling ML Voice System

A comprehensive system that combines machine learning traffic prediction with voice commands and cloud auto-scaling capabilities.

## 🚀 Features

- **ML Traffic Prediction**: Uses Random Forest to predict web traffic based on time
- **Voice Assistant**: Control the system using voice commands
- **Auto Scaling**: Automatically scales cloud infrastructure based on traffic
- **Real-time Dashboard**: Monitor traffic predictions and system status
- **Cloud Integration**: AWS-ready with boto3 integration
- **Containerized**: Docker and Kubernetes support

## 📁 Project Structure

```
cloud-autoscale-ml-voice/
├── data/
│   └── traffic.csv              # Sample traffic data
├── models/
│   └── train_model.py           # ML model training script
├── voice/
│   └── voice_assistant.py       # Voice control interface
├── scaling/
│   └── autoscaler.py            # Auto-scaling logic
├── dashboard/
│   └── dashboard.py             # Streamlit monitoring dashboard
├── webapp/
│   └── app.py                   # Flask REST API
├── docker/
│   └── Dockerfile               # Docker configuration
├── kubernetes/
│   └── deployment.yaml          # K8s deployment files
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

## 🛠️ Installation

### Prerequisites

- Python 3.8+
- Docker (optional)
- Kubernetes cluster (optional)
- Microphone (for voice assistant)

### Setup

1. **Clone and navigate to the project:**
   ```bash
   cd cloud-autoscale-ml-voice
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Train the ML model:**
   ```bash
   python models/train_model.py
   ```

## 🚀 Running the System

### Option 1: Local Development

1. **Start the Flask API:**
   ```bash
   python webapp/app.py
   ```
   Access at: http://localhost:5000

2. **Start the Dashboard:**
   ```bash
   streamlit run dashboard/dashboard.py
   ```
   Access at: http://localhost:8501

3. **Start the Voice Assistant:**
   ```bash
   python voice/voice_assistant.py
   ```

### Option 2: Docker

1. **Build the image:**
   ```bash
   docker build -t autoscale-ml -f docker/Dockerfile .
   ```

2. **Run the container:**
   ```bash
   docker run -p 5000:5000 autoscale-ml
   ```

### Option 3: Kubernetes

1. **Apply the deployment:**
   ```bash
   kubectl apply -f kubernetes/deployment.yaml
   ```

2. **Check the status:**
   ```bash
   kubectl get pods,svc,hpa
   ```

## 📡 API Endpoints

- `GET /` - Home page with API documentation
- `GET /predict` - Get current traffic prediction
- `GET /predict/<hour>/<minute>` - Get prediction for specific time
- `GET /health` - System health check

**Example Response:**
```json
{
  "current_time": "14:30",
  "predicted_traffic": 940,
  "required_servers": 4,
  "timestamp": "2024-01-15T14:30:00.000Z"
}
```

## 🎤 Voice Commands

- **"predict traffic"** - Get current traffic prediction
- **"server status"** - Check required servers
- **"help"** - Show available commands
- **"exit"** - Close the voice assistant

## 📊 Auto Scaling Rules

The system scales servers based on traffic:

| Traffic (requests) | Servers Required |
|-------------------|------------------|
| < 200             | 1                |
| < 500             | 2                |
| < 800             | 3                |
| < 1000            | 4                |
| ≥ 1000            | 5                |

## ☁️ Cloud Integration

### AWS Setup

1. **Configure AWS credentials:**
   ```bash
   aws configure
   ```

2. **Update the autoscaler** with your Auto Scaling Group name in `scaling/autoscaler.py`

3. **The system will automatically** scale your EC2 instances based on traffic predictions

## 🔧 Configuration

### Environment Variables

- `FLASK_ENV`: Set to 'production' for production deployment
- `PYTHONUNBUFFERED`: Set to '1' for better logging

### Customization

- **Modify traffic patterns**: Edit `data/traffic.csv`
- **Adjust scaling rules**: Update `scaling/autoscaler.py`
- **Change ML model**: Modify `models/train_model.py`

## 📈 Monitoring

The Streamlit dashboard provides:

- Real-time traffic predictions
- Server requirement visualization
- 24-hour traffic forecast
- System health monitoring
- API endpoint testing

## 🐛 Troubleshooting

### Common Issues

1. **Model not found:**
   ```bash
   python models/train_model.py
   ```

2. **Voice assistant not working:**
   - Check microphone permissions
   - Ensure Flask API is running
   - Verify internet connection for speech recognition

3. **Docker build fails:**
   - Check Docker daemon is running
   - Verify all dependencies in requirements.txt

4. **Kubernetes pods not starting:**
   - Check image is built and pushed to registry
   - Verify resource limits
   - Check node availability

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🔮 Future Enhancements

- [ ] Support for multiple cloud providers (Azure, GCP)
- [ ] Advanced ML models (LSTM, Prophet)
- [ ] Real-time traffic data integration
- [ ] Mobile app interface
- [ ] Advanced analytics and reporting
- [ ] Multi-region support
- [ ] Cost optimization algorithms

## 📞 Support

For issues and questions:
- Create an issue in the GitHub repository
- Check the troubleshooting section
- Review the API documentation

---

**Built with ❤️ using Python, Flask, Streamlit, and Machine Learning**
