# 🎯 AI-Powered Succession Planning Application

A comprehensive Streamlit application that demonstrates how Generative AI can transform talent management by analyzing 360-degree reviews to identify succession candidates and create personalized development plans.

## ✨ Features

- **360-Degree Review Analysis**: Processes comprehensive feedback from managers, peers, direct reports, and cross-functional partners
- **Succession Candidate Identification**: Uses AI algorithms to identify top candidates for leadership roles based on competency scores and readiness
- **Personalized Development Plans**: Generates tailored development recommendations with specific actions and timelines
- **Interactive Dashboards**: Beautiful visualizations including competency radar charts, team heatmaps, and performance analytics
- **Sample Data**: Includes realistic sample data for 8 team members across different organizational levels

## 🏗️ Architecture

### Core Components

1. **Data Generation (`sample_data.py`)**
   - Generates realistic 360-degree review data
   - Covers 8 employees from Graduate to VP levels
   - Includes 12 key competencies with role-appropriate scoring

2. **Succession Planning Engine (`succession_planning.py`)**
   - `SuccessionPlanningAnalyzer`: Main analysis class
   - Competency-based candidate ranking
   - Development gap identification
   - Personalized action plan generation

3. **Streamlit Application (`succession_app.py`)**
   - Multi-page interface with navigation
   - Interactive visualizations using Plotly
   - Real-time analytics and insights

### Key Algorithms

- **Succession Scoring**: Weighted competency scores based on target role requirements
- **Gap Analysis**: Identifies development needs by comparing current vs. required competency levels
- **Development Planning**: Generates specific, actionable development recommendations

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
   uv pip install -e .
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
- **Ranking**: Shows candidates ranked by succession readiness score
- **Metrics**: Includes overall performance scores, experience, and team size considerations

### 2. Development Plans
- **Employee Selection**: Choose any team member for detailed analysis
- **Competency Radar**: Visual representation of current competency levels
- **Gap Analysis**: Identifies specific areas for development
- **Action Plans**: Concrete, prioritized development recommendations

### 3. Team Analytics
- **Team Metrics**: Overall team performance statistics
- **Competency Heatmap**: Visual overview of team strengths and gaps
- **Performance Distribution**: Charts showing team performance patterns
- **Experience vs Performance**: Scatter plot analysis

### 4. Raw Data
- **360-Review Data**: Complete dataset with all review details
- **Data Summary**: Key statistics about the dataset

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

1. **AI-Driven Succession Planning**: Moves beyond traditional "gut feeling" approaches to data-driven candidate identification
2. **Competency-Based Development**: Focuses development efforts on specific, measurable competency gaps
3. **360-Degree Integration**: Synthesizes feedback from multiple sources for comprehensive talent assessment
4. **Personalized Recommendations**: Generates specific, actionable development plans tailored to individual needs
5. **Visual Analytics**: Makes complex HR data accessible through intuitive visualizations

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
