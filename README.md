# Student Management SaaS

A professional student management system with AI-powered grade predictions, PDF report generation, and modern Bootstrap UI.

## Features

🤖 **AI Prediction System**
- Predicts student performance using machine learning
- Shows expected performance trends
- Provides confidence levels for predictions

📄 **PDF Reports**
- Generate downloadable PDF reports for each student
- Includes current performance and AI predictions
- Professional formatting

🎨 **Modern SaaS UI**
- Bootstrap-based responsive design
- Professional dashboard interface
- Interactive charts and analytics

☁️ **Production Ready**
- Optimized for cloud deployment
- Environment variable support
- Database persistence

## Local Development

1. Clone the repository
2. Create virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Initialize database:
   ```bash
   python init_db.py
   ```
5. Run the application:
   ```bash
   python app.py
   ```
6. Open http://localhost:5000

## Deployment Options

### Railway (Recommended)
1. Connect your GitHub repository to Railway
2. Railway will automatically detect Python app
3. Set environment variables if needed
4. Deploy!

### Render
1. Create new Web Service
2. Connect GitHub repository
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `python app.py`
5. Deploy

### Heroku
1. Install Heroku CLI
2. Login: `heroku login`
3. Create app: `heroku create your-app-name`
4. Push to Heroku: `git push heroku main`
5. Open: `heroku open`

## Technology Stack

- **Backend**: Flask (Python)
- **Database**: SQLite
- **AI/ML**: Scikit-learn, Pandas, NumPy
- **PDF Generation**: ReportLab
- **Frontend**: Bootstrap 5, Chart.js
- **Deployment**: Railway/Render/Heroku

## Usage

1. Register/Login as lecturer
2. Add students with their marks
3. View AI predictions for each student
4. Download PDF reports
5. Monitor performance trends

## API Endpoints

- `GET /` - Dashboard
- `POST /add` - Add student
- `GET /download/<id>` - Download PDF report
- `POST /login` - User login
- `POST /register` - User registration

## Contributing

1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request

## License

MIT License - feel free to use for educational purposes.