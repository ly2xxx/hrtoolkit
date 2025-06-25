# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Running the application
- `streamlit run succession_app.py` - Start the Streamlit web application

### Dependencies
- Install dependencies: `pip install -r requirements.txt`
- Main dependencies: streamlit, pandas, numpy, plotly, openpyxl

## Architecture Overview

This is a **Streamlit-based AI-powered succession planning application** that analyzes 360-degree reviews to identify succession candidates and create personalized development plans.

### Core Components

**Main Application (`succession_app.py`)**:
- Multi-page Streamlit app with succession planning, development plans, team dynamics, and analytics
- CSV upload functionality for custom data input
- Session state management for uploaded data across all pages
- Interactive visualizations using Plotly

**Data Processing**:
- Reads 360-degree review data from CSV files or generates sample data
- `sample_data.py` creates realistic review text with team dynamics
- `succession_planning.py` analyzes competency scores and identifies candidates
- `team_dynamics.py` detects toxic behaviors and positive collaboration patterns

**Key Features**:
- CSV file upload interface in Raw Data page
- Sample CSV template download
- Cross-page data persistence using session state
- NLP-based competency score extraction from review text

### Data Structure
The CSV file should contain:
- Employee information: name, role, level, experience, team size
- Review metadata: reviewer type, date, review text
- Competency scores: leadership, communication, strategic thinking, etc.
- Qualitative feedback: strengths and development areas

## Standard Workflow
1. First think through the problem, read the codebase for relevant files, and write a plan to tasks/todo.md.
2. The plan should have a list of todo items that you can check off as you complete them.
3. Before you begin working, check in with me and I will verify the plan.
4. Then, begin working on the todo items, marking them as complete as you go.
5. Please every step of the way just give me a high level explanation of what changes you made.
6. Make every task and code change you do as simple as possible. We want to avoid making any massive or complex changes. Every change should impact as little code as possible. Everything is about simplicity.
7. Finally, add a revised section to the todo.md file with a summary of the changes you made and any other relevant information.