# 🎯 AI-Powered Succession Planning Application with Team Dynamics Analysis

A comprehensive Streamlit application that demonstrates how Generative AI can transform talent management by analyzing human text reviews from 360-degree feedback to identify succession candidates, create personalized development plans, and detect toxic team dynamics.

## ✨ Enhanced Features

### 🔍 Human Text Review Analysis
- **Natural Language Processing**: Extracts competency scores from actual human review text instead of numerical ratings
- **Sentiment Analysis**: Analyzes tone and sentiment in feedback to understand team dynamics
- **Realistic Review Generation**: Creates human-like review comments that reveal personality traits and team interactions

### 🚨 Team Dynamics & Toxic Behavior Detection  
- **Toxic Pattern Recognition**: Identifies dismissive language, credit stealing, undermining behaviors, and office politics
- **Relationship Network Analysis**: Maps team relationships and detects negative sentiment patterns
- **Intervention Recommendations**: Provides specific actions to address toxic behaviors and improve team health
- **Team Health Scoring**: Comprehensive team wellness metrics with alerts for high-risk individuals

### 📈 Advanced Succession Planning
- **Text-Based Competency Scoring**: Derives scores from review text content using NLP techniques
- **Succession Candidate Identification**: Uses AI algorithms to identify top candidates based on authentic feedback
- **Personalized Development Plans**: Generates tailored recommendations with specific actions and timelines
- **Interactive Dashboards**: Beautiful visualizations including competency radar charts, team heatmaps, and performance analytics

### 📊 Comprehensive Analytics
- **Team Champions Identification**: Highlights positive role models and collaboration leaders
- **Conflict Detection**: Identifies interpersonal tensions and provides resolution strategies
- **Credit Attribution Analysis**: Detects patterns of credit sharing vs. credit stealing
- **Sample Data**: Includes realistic sample data for 8 team members with authentic review text

## 🏗️ Architecture

### Core Components

1. **Enhanced Data Generation (`sample_data.py`)**
   - Generates realistic human text reviews for 360-degree feedback
   - Creates authentic personality traits and team dynamics patterns
   - Includes subtle toxic behavior indicators and positive collaboration examples
   - Extracts competency scores from review text using NLP techniques

2. **Team Dynamics Analysis Engine (`team_dynamics.py`) - NEW**
   - `TeamDynamicsAnalyzer`: Comprehensive team health analysis
   - Toxic behavior pattern detection (credit stealing, dismissive language, undermining)
   - Positive collaboration pattern identification
   - Relationship network analysis and sentiment mapping
   - Intervention recommendation generation

3. **Succession Planning Engine (`succession_planning.py`)**
   - `SuccessionPlanningAnalyzer`: Enhanced with text-based analysis
   - Competency-based candidate ranking from review text
   - Development gap identification
   - Personalized action plan generation

4. **Enhanced Streamlit Application (`succession_app.py`)**
   - Multi-page interface with new Team Dynamics page
   - Interactive visualizations using Plotly
   - Real-time toxic behavior alerts
   - Original review text display with extracted scores

### Key Algorithms

- **Text-Based NLP Scoring**: Extracts competency scores from human review text using keyword analysis and sentiment detection
- **Toxic Pattern Recognition**: Uses regex patterns to identify dismissive language, credit attribution issues, and undermining behaviors
- **Relationship Sentiment Analysis**: Analyzes mentions of team members in reviews to detect positive/negative relationships
- **Team Health Scoring**: Combines toxicity and positivity metrics to generate overall team wellness indicators
- **Succession Scoring**: Enhanced weighted competency scores based on authentic feedback content
- **Intervention Planning**: Generates specific recommendations based on detected behavioral patterns

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- [uv](https://docs.astral.sh/uv/) package manager (recommended)

### Installation with uv (Recommended)

1. **Install uv** (if not already installed):
   ```bash
   # On macOS and Linux
   curl -LsSf https://astral.sh/uv/install.sh | sh
   
   # On Windows
   powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
   
   # Or using pip
   pip install uv
   ```

2. **Clone or download the project files**:
   ```bash
   # If you have git
   git clone <repository-url>
   cd hrtoolkit
   
   # Or download and extract the files to a directory
   ```

3. **Create and activate virtual environment**:
   ```bash
   uv venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

4. **Install dependencies**:
   ```bash
   uv pip install streamlit pandas numpy plotly openpyxl
   ```

5. **Run the application**:
   ```bash
   streamlit run succession_app.py
   ```

### Alternative Installation (without uv)

If you prefer using pip:

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install streamlit pandas numpy plotly openpyxl

# Run the application
streamlit run succession_app.py
```

## 📊 Application Pages

### 1. Succession Planning Dashboard
- **Overview**: Displays current role holders and their top succession candidates
- **Ranking**: Shows candidates ranked by succession readiness score based on text analysis
- **Metrics**: Includes overall performance scores, experience, and team size considerations

### 2. Enhanced Development Plans
- **Employee Selection**: Choose any team member for detailed analysis
- **Competency Radar**: Visual representation of current competency levels
- **Original Review Text**: Display actual human review comments with extracted scores
- **Gap Analysis**: Identifies specific areas for development from text analysis
- **Action Plans**: Concrete, prioritized development recommendations

### 3. Team Dynamics Analysis - NEW 🚨
- **Team Health Overview**: Comprehensive wellness metrics and toxicity alerts
- **Toxic Behavior Detection**: Real-time alerts for dismissive language, credit stealing, and undermining
- **Team Champions**: Highlights positive role models and collaboration leaders
- **Active Tensions**: Identifies interpersonal conflicts with evidence and resolution strategies
- **Relationship Network**: Visualizes team sentiment patterns and communication dynamics
- **Intervention Recommendations**: Specific actions to improve team health

### 4. Team Analytics
- **Team Metrics**: Overall team performance statistics
- **Competency Heatmap**: Visual overview of team strengths and gaps
- **Performance Distribution**: Charts showing team performance patterns
- **Experience vs Performance**: Scatter plot analysis

### 5. Raw Data
- **360-Review Data**: Complete dataset with original human review text
- **Extracted Scores**: Shows how competency scores were derived from text
- **Data Summary**: Key statistics about the dataset and text analysis

## 🎯 Sample Team Structure

The application includes sample data for 8 team members across different levels:

| Name | Role | Level | Experience | Team Size |
|------|------|-------|------------|-----------|
| Sarah Chen | VP Engineering | VP | 12 years | 8 |
| Michael Rodriguez | Director Product | Director | 8 years | 5 |
| Jennifer Kim | Director Engineering | Director | 9 years | 6 |
| David Thompson | Senior Manager | Manager | 6 years | 4 |
| Lisa Wang | Product Manager | Professional | 4 years | 0 |
| Alex Johnson | Senior Developer | Professional | 5 years | 0 |
| Maria Garcia | UX Designer | Professional | 3 years | 0 |
| James Wilson | Junior Developer | Graduate | 1 year | 0 |

## 🔧 Customization

### Adding Your Own Data

1. **CSV Format**: Replace the sample data generation with your CSV file:
   ```python
   # In succession_app.py, modify the load_sample_data function
   @st.cache_data
   def load_sample_data():
       return pd.read_csv('your_data.csv')
   ```

2. **Required Columns**:
   - `employee_name`: Employee name
   - `employee_role`: Job title
   - `employee_level`: Organizational level
   - `years_experience`: Years of experience
   - `reviewer_type`: Type of reviewer (Manager, Peer, etc.)
   - Competency scores: `leadership_score`, `communication_score`, etc.
   - `strengths`: Text feedback on strengths
   - `development_areas`: Text feedback on development needs

### Modifying Competencies

Edit the competencies list in `succession_planning.py`:

```python
self.competencies = [
    "leadership", "strategic_thinking", "communication", 
    # Add your custom competencies here
]
```

### Customizing Succession Paths

Modify the succession paths in `succession_planning.py`:

```python
succession_paths = {
    "Your Target Role": ["Eligible Level 1", "Eligible Level 2"],
    # Add your organization's succession paths
}
```

## 🧪 Development

### Running Tests

```bash
# With uv
uv pip install -e ".[dev]"
pytest

# With pip
pip install pytest
pytest
```

### Code Formatting

```bash
# With uv
uv pip install -e ".[dev]"
black .
flake8 .

# With pip
pip install black flake8
black .
flake8 .
```

## 📈 Key Insights Demonstrated

1. **Text-Based AI Analysis**: Moves beyond numerical ratings to analyze actual human feedback language for deeper insights
2. **Toxic Behavior Detection**: Proactively identifies office politics, credit stealing, and undermining behaviors from review text
3. **Team Dynamics Intelligence**: Understands collaboration patterns, conflicts, and relationship networks through sentiment analysis
4. **Authentic Competency Assessment**: Derives meaningful scores from real feedback rather than artificial numerical ratings
5. **Intervention-Focused Recommendations**: Provides specific, actionable steps to address both individual development and team health issues
6. **Early Warning System**: Detects team dysfunction before it escalates through pattern recognition in feedback language
7. **360-Degree Integration**: Synthesizes feedback from multiple sources with awareness of reviewer bias and relationship dynamics
8. **Visual Analytics**: Makes complex HR and team dynamics data accessible through intuitive visualizations

## 🤝 Use Cases

- **HR Teams**: Identify and develop future leaders
- **Managers**: Make informed promotion and development decisions
- **Executives**: Understand talent pipeline and succession readiness
- **Employees**: Visualize career development opportunities
- **Consultants**: Demonstrate AI applications in talent management

## 📝 License

This project is provided as a demonstration of AI-powered HR applications. Feel free to adapt and modify for your organization's needs.

## 🔗 Related Resources

- [Blog Post: Generative AI in Talent Management](https://edisonideas.wordpress.com/2025/06/05/generative-ai-in-talent-management-beyond-cv-filtering-to-strategic-hr-insights/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Plotly Documentation](https://plotly.com/python/)
- [uv Documentation](https://docs.astral.sh/uv/)

## 🆘 Support

If you encounter any issues:

1. Check that all dependencies are installed correctly
2. Ensure you're using Python 3.8 or higher
3. Verify that the virtual environment is activated
4. Check the Streamlit logs for specific error messages

For additional support, please refer to the Streamlit and uv documentation linked above.

---
## 📚 References
### Claude Code overview
[![ MCP client](https://img.youtube.com/vi/iYiuzAsWnHU/hqdefault.jpg)](https://m.youtube.com/watch?v=iYiuzAsWnHU)
