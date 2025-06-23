import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from sample_data import generate_360_review_data
from succession_planning import SuccessionPlanningAnalyzer

# Page config
st.set_page_config(
    page_title="AI-Powered Succession Planning",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .candidate-card {
        background-color: #ffffff;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #e1e5eb;
        margin-bottom: 1rem;
    }
    .high-priority {
        border-left: 4px solid #ff6b6b;
    }
    .medium-priority {
        border-left: 4px solid #ffa726;
    }
    .low-priority {
        border-left: 4px solid #66bb6a;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_sample_data():
    """Load and cache sample 360-degree review data"""
    return generate_360_review_data()

@st.cache_data
def get_succession_analyzer(reviews_df):
    """Create and cache succession planning analyzer"""
    return SuccessionPlanningAnalyzer(reviews_df)

def display_employee_radar_chart(analyzer, employee_name):
    """Display radar chart for employee competencies"""
    employee_scores = analyzer.calculate_employee_scores()
    employee_data = employee_scores[employee_scores['name'] == employee_name]
    
    if len(employee_data) == 0:
        return
    
    competencies = [comp.replace('_', ' ').title() for comp in analyzer.competencies]
    scores = [employee_data.iloc[0][comp] for comp in analyzer.competencies]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=scores,
        theta=competencies,
        fill='toself',
        name=employee_name,
        line_color='rgb(31, 119, 180)'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1]
            )),
        showlegend=True,
        title=f"Competency Profile: {employee_name}",
        height=400
    )
    
    return fig

def display_succession_candidates():
    """Display succession planning candidates"""
    st.header("🎯 Succession Planning Dashboard")
    
    reviews_df = load_sample_data()
    analyzer = get_succession_analyzer(reviews_df)
    
    # Get succession candidates
    succession_candidates = analyzer.identify_succession_candidates()
    
    if not succession_candidates:
        st.warning("No succession candidates identified.")
        return
    
    # Display current leadership and candidates
    for target_role, data in succession_candidates.items():
        st.subheader(f"Succession Planning for {target_role}")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("**Current Role Holder:**")
            if data['current_holder']:
                holder = data['current_holder']
                st.markdown(f"""
                <div class="metric-card">
                    <strong>{holder['name']}</strong><br>
                    {holder['role']}<br>
                    Overall Score: {holder['overall_score']:.2f}<br>
                    Experience: {holder['years_experience']} years
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("**Top Succession Candidates:**")
            
            for i, candidate in enumerate(data['candidates'][:3]):
                rank_emoji = ["🥇", "🥈", "🥉"][i]
                
                st.markdown(f"""
                <div class="candidate-card">
                    {rank_emoji} <strong>{candidate['name']}</strong><br>
                    {candidate['role']} | {candidate['level']}<br>
                    Succession Score: {candidate['succession_score']:.2f}<br>
                    Overall Performance: {candidate['overall_score']:.2f}<br>
                    Experience: {candidate['years_experience']} years
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("---")

def display_development_plans():
    """Display personalized development plans"""
    st.header("📈 Personalized Development Plans")
    
    reviews_df = load_sample_data()
    analyzer = get_succession_analyzer(reviews_df)
    
    # Employee selection
    employees = reviews_df['employee_name'].unique()
    selected_employee = st.selectbox("Select Employee for Development Plan:", employees)
    
    if selected_employee:
        col1, col2 = st.columns([1, 1])
        
        with col1:
            # Display competency radar chart
            fig = display_employee_radar_chart(analyzer, selected_employee)
            if fig:
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Get development plan
            dev_plan = analyzer.generate_development_plan(selected_employee)
            
            if 'error' not in dev_plan:
                st.markdown(f"**Development Plan for {dev_plan['employee_name']}**")
                st.markdown(f"*Current Role:* {dev_plan['current_role']}")
                st.markdown(f"*Target Role:* {dev_plan['target_role']}")
                st.markdown(f"*Timeline:* {dev_plan['timeline']}")
                
                # Display strengths
                with st.expander("💪 Key Strengths"):
                    for strength in dev_plan['strengths']:
                        st.markdown(f"• {strength}")
                
                # Display development areas
                with st.expander("🎯 Development Areas"):
                    for area in dev_plan['development_areas']:
                        st.markdown(f"• {area}")
        
        # Development actions
        if 'development_actions' in dev_plan and dev_plan['development_actions']:
            st.markdown("### 🚀 Recommended Development Actions")
            
            for action in dev_plan['development_actions']:
                priority_class = f"{action['priority'].lower()}-priority"
                
                st.markdown(f"""
                <div class="candidate-card {priority_class}">
                    <strong>{action['competency']}</strong> - {action['priority']} Priority<br>
                    Current Score: {action['current_score']} → Target: {action['target_score']} 
                    (Gap: {action['gap']})<br><br>
                    <strong>Recommended Actions:</strong><br>
                    {'<br>'.join([f"• {act}" for act in action['recommended_actions']])}
                </div>
                """, unsafe_allow_html=True)

def display_team_analytics():
    """Display team-level analytics and insights"""
    st.header("📊 Team Analytics & Insights")
    
    reviews_df = load_sample_data()
    analyzer = get_succession_analyzer(reviews_df)
    employee_scores = analyzer.calculate_employee_scores()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        avg_score = employee_scores['overall_score'].mean()
        st.metric("Team Average Score", f"{avg_score:.2f}")
    
    with col2:
        high_performers = len(employee_scores[employee_scores['overall_score'] >= 0.8])
        st.metric("High Performers (≥0.8)", high_performers)
    
    with col3:
        ready_for_promotion = len(employee_scores[employee_scores['overall_score'] >= 0.75])
        st.metric("Promotion Ready (≥0.75)", ready_for_promotion)
    
    # Team competency heatmap
    st.markdown("### Team Competency Heatmap")
    
    # Prepare data for heatmap
    heatmap_data = []
    for _, employee in employee_scores.iterrows():
        for comp in analyzer.competencies:
            heatmap_data.append({
                'Employee': employee['name'],
                'Competency': comp.replace('_', ' ').title(),
                'Score': employee[comp]
            })
    
    heatmap_df = pd.DataFrame(heatmap_data)
    pivot_df = heatmap_df.pivot(index='Employee', columns='Competency', values='Score')
    
    fig = px.imshow(
        pivot_df,
        labels=dict(x="Competency", y="Employee", color="Score"),
        x=pivot_df.columns,
        y=pivot_df.index,
        color_continuous_scale="RdYlBu_r",
        aspect="auto"
    )
    
    fig.update_layout(
        title="Team Competency Scores",
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Performance distribution
    st.markdown("### Performance Distribution")
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_hist = px.histogram(
            employee_scores, 
            x='overall_score', 
            nbins=10,
            title="Overall Score Distribution"
        )
        st.plotly_chart(fig_hist, use_container_width=True)
    
    with col2:
        fig_scatter = px.scatter(
            employee_scores,
            x='years_experience',
            y='overall_score',
            size='team_size',
            color='level',
            hover_name='name',
            title="Experience vs Performance"
        )
        st.plotly_chart(fig_scatter, use_container_width=True)

def main():
    """Main application"""
    st.title("🎯 AI-Powered Succession Planning")
    st.markdown("""
    This application demonstrates how Generative AI can transform talent management by analyzing 
    360-degree reviews to identify succession candidates and create personalized development plans.
    """)
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Choose a view:",
        ["Succession Planning", "Development Plans", "Team Analytics", "Raw Data"]
    )
    
    if page == "Succession Planning":
        display_succession_candidates()
    elif page == "Development Plans":
        display_development_plans()
    elif page == "Team Analytics":
        display_team_analytics()
    elif page == "Raw Data":
        st.header("📋 Sample 360-Degree Review Data")
        reviews_df = load_sample_data()
        st.dataframe(reviews_df)
        
        # Data summary
        st.markdown("### Data Summary")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Reviews", len(reviews_df))
        with col2:
            st.metric("Employees", reviews_df['employee_name'].nunique())
        with col3:
            st.metric("Avg Reviews per Employee", f"{len(reviews_df) / reviews_df['employee_name'].nunique():.1f}")

if __name__ == "__main__":
    main()