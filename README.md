# Sahayak AI Teaching Assistant 🤖📚

A comprehensive AI-powered platform designed to revolutionize classroom preparation and management for educators. Built with FastAPI and PostgreSQL, Sahayak provides intelligent tools for lesson planning, worksheet generation, presentation creation, student progress tracking, and visual teaching aids.

## 🌟 Features

### Core AI-Powered Tools
- **Lesson Planning**: Generate comprehensive, grade-appropriate lesson plans with learning objectives, materials, procedures, and assessments
- **Worksheet Generation**: Create customized worksheets from uploaded documents or topics with multiple question types (MCQ, theory, mixed)
- **Presentation Creator**: Generate PowerPoint presentations from topics or documents with customizable styles and slide counts
- **Visual Teaching Aids**: Create blackboard diagrams, flowcharts, and visual explanations with actual diagram images
- **Fun Learning Activities**: Generate engaging classroom activities and games tailored to specific topics and grade levels

### Student Management
- **Progress Tracking**: Monitor individual student performance with detailed progress history and analytics
- **Student Records**: Maintain comprehensive student profiles with attendance, grades, and contact information
- **Performance Analytics**: Generate reports and charts showing class performance trends and individual progress
- **Bulk Operations**: Update multiple student records and generate comparative reports

### Knowledge Base
- **Concept Explanations**: Get simple, analogy-based explanations of complex concepts in multiple languages
- **Concept Comparisons**: Compare and contrast multiple concepts with detailed analysis
- **Analogy Generator**: Create relatable analogies to help students understand difficult topics

### Additional Features
- **Document Processing**: Extract text from PDFs and other documents for content generation
- **File Management**: Secure file storage with automatic cleanup and expiration
- **User Authentication**: Secure JWT-based authentication with role-based access
- **Settings & Profile**: Customizable user preferences and teaching profiles
- **Data Export**: Export user data in JSON format for backup or migration

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- PostgreSQL database
- Groq API key (for AI features)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Adi3595/sahayak-2-0.git
   cd sahayak
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file with:
   ```env
   SECRET_KEY=your-secret-key-here
   GROQ_API_KEY=your-groq-api-key
   DATABASE_URL=postgresql://username:password@localhost/sahayak_db
   ```

5. **Initialize database**
   ```bash
   python -c "from database import create_tables; create_tables()"
   ```

6. **Run the application**
   ```bash
   python main.py
   ```

The API will be available at `http://localhost:8000`

## 📖 API Documentation

### Authentication Endpoints
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `GET /api/auth/me` - Get current user info

### Core AI Features
- `POST /generate/` - Generate lesson plans or chat responses
- `POST /summarize-pdf/` - Summarize PDF documents
- `POST /generate-worksheets/` - Create worksheets from documents
- `POST /generate-from-topics/` - Create worksheets from topics
- `POST /create-ppt/` - Generate PowerPoint presentations

### Student Management
- `GET /api/students/` - List all students with filtering
- `POST /api/students/` - Create new student record
- `GET /api/students/{student_id}` - Get student details
- `POST /api/progress/` - Update student progress

### Additional Endpoints
- `GET /api/settings` - Get user settings
- `POST /api/settings/save` - Save user settings
- `GET /api/profile` - Get user profile
- `POST /api/profile/save` - Save user profile

## 🗄️ Database Schema

The application uses SQLAlchemy with the following main models:

- **User**: User accounts and authentication
- **UserSettings**: User preferences and configurations
- **UserProfile**: Extended user information and statistics
- **Conversation**: Chat conversations with AI
- **ConversationMessage**: Individual messages in conversations
- **LessonPlan**: Generated lesson plans
- **GeneratedFile**: Metadata for generated files
- **StudentRecord**: Student information and progress
- **ProgressHistory**: Detailed progress tracking entries

## 🔧 Configuration

### Environment Variables
- `SECRET_KEY`: JWT signing key (required)
- `GROQ_API_KEY`: API key for Groq AI services (required)
- `DATABASE_URL`: PostgreSQL connection string (optional, defaults to SQLite)
- `PORT`: Server port (optional, defaults to 8000)

### File Storage
- `uploads/`: Temporary file uploads
- `outputs/`: Generated files and documents
- Files are automatically cleaned up after 7 days

## 🌐 Frontend Integration

The backend serves static HTML files for the frontend interface. Key pages include:
- `/` - Dashboard
- `/lesson_planning.html` - Lesson planning interface
- `/Differentiated_materials.html` - Worksheet generation
- `/blackboard_diagrams.html` - Visual aids creation
- `/Student_tracking.html` - Student progress tracking

## 📊 Monitoring & Health Checks

- `GET /health` - Application health status
- Database connection monitoring
- Automatic file cleanup scheduling

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 🙏 Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- Powered by [Groq](https://groq.com/) - Fast AI inference
- Database ORM by [SQLAlchemy](https://www.sqlalchemy.org/)
- Document processing with various Python libraries

## 📞 Support

For support, please open an issue on GitHub or contact the development team.

---

**Sahayak** - Empowering educators with AI to create better learning experiences! 🎓✨
