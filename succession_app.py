import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from sample_data import generate_360_review_data
from succession_planning import SuccessionPlanningAnalyzer
from team_dynamics import TeamDynamicsAnalyzer

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
        color: #000000;
    }
    .candidate-card {
        background-color: #ffffff;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #e1e5eb;
        margin-bottom: 1rem;
        color: #000000;
    }
    .high-priority {
        border-left: 4px solid #ff6b6b;
        color: #000000;
    }
    .medium-priority {
        border-left: 4px solid #ffa726;
        color: #000000;
    }
    .low-priority {
        border-left: 4px solid #66bb6a;
        color: #000000;
    }
    .toxic-alert {
        background-color: #ffebee;
        border-left: 4px solid #f44336;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        color: #000000;
    }
    .positive-highlight {
        background-color: #e8f5e8;
        border-left: 4px solid #4caf50;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        color: #000000;
    }
    .review-text-box {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #e1e5eb;
        margin: 0.5rem 0;
        font-style: italic;
        color: #000000;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_sample_data():
    """Load and cache sample 360-degree review data"""
    return generate_360_review_data()

def load_csv_data(csv_file):
    """Load CSV data from uploaded file"""
    df = pd.read_csv(csv_file)
    # Convert review_date to datetime if it exists
    if 'review_date' in df.columns:
        df['review_date'] = pd.to_datetime(df['review_date'])
    return df

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
    
    reviews_df = get_current_data()
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
    
    reviews_df = get_current_data()
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
    
    reviews_df = get_current_data()
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

def display_team_dynamics():
    """Display team dynamics analysis including toxic behavior detection"""
    st.header("🤝 Team Dynamics Analysis")
    
    reviews_df = get_current_data()
    dynamics_analyzer = TeamDynamicsAnalyzer(reviews_df)
    
    # Generate team health report
    health_report = dynamics_analyzer.generate_team_health_report()
    
    # Team Health Overview
    st.markdown("### 🏥 Team Health Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        health_score = health_report['team_health_score']
        health_status = "🟢 Excellent" if health_score > 0.7 else "🟡 Needs Attention" if health_score > 0.4 else "🔴 Critical"
        st.metric("Team Health Score", f"{health_score:.2f}", 
                 delta=health_status)
    
    with col2:
        toxicity = health_report['team_toxicity']
        st.metric("Team Toxicity", f"{toxicity:.2f}", 
                 delta=f"{'🔴 High' if toxicity > 0.4 else '🟡 Medium' if toxicity > 0.2 else '🟢 Low'}")
    
    with col3:
        positivity = health_report['team_positivity']
        st.metric("Team Positivity", f"{positivity:.2f}",
                 delta=f"{'🟢 High' if positivity > 0.6 else '🟡 Medium' if positivity > 0.3 else '🔴 Low'}")
    
    with col4:
        tensions = health_report['active_tensions']
        st.metric("Active Tensions", tensions,
                 delta=f"{'🔴 Many' if tensions > 3 else '🟡 Some' if tensions > 1 else '🟢 Few'}")
    
    # Toxic Behavior Alerts
    if health_report['high_risk_individuals']:
        st.markdown("### ⚠️ Toxic Behavior Alerts")
        
        toxic_analysis = dynamics_analyzer.analyze_toxic_behaviors()
        
        for person in health_report['high_risk_individuals']:
            person_data = toxic_analysis[person]
            
            st.markdown(f"""
            <div class="toxic-alert">
                <strong>🚨 {person}</strong> - Risk Level: {person_data['risk_level']}<br>
                Overall Toxicity Score: {person_data['overall_toxicity']:.2f}<br>
                <small>Requires immediate attention and intervention</small>
            </div>
            """, unsafe_allow_html=True)
            
            # Show specific toxic behaviors
            if person_data['examples']:
                with st.expander(f"View toxic behavior examples for {person}"):
                    for behavior_type, examples in person_data['examples'].items():
                        st.markdown(f"**{behavior_type.replace('_', ' ').title()}:**")
                        for example in examples[:2]:  # Show first 2 examples
                            st.markdown(f"• *{example}*")
    
    # Team Champions
    if health_report['team_champions']:
        st.markdown("### 🌟 Team Champions")
        
        positive_analysis = dynamics_analyzer.analyze_positive_dynamics()
        
        cols = st.columns(min(3, len(health_report['team_champions'])))
        
        for i, person in enumerate(health_report['team_champions']):
            person_data = positive_analysis[person]
            
            with cols[i % 3]:
                st.markdown(f"""
                <div class="positive-highlight">
                    <strong>⭐ {person}</strong><br>
                    Collaboration Level: {person_data['collaboration_level']}<br>
                    Positivity Score: {person_data['overall_positivity']:.2f}<br>
                    <small>Great role model for team collaboration</small>
                </div>
                """, unsafe_allow_html=True)
    
    # Active Tensions
    if health_report['tension_details']:
        st.markdown("### ⚡ Active Team Tensions")
        
        for tension in health_report['tension_details']:
            severity_color = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}
            severity_icon = severity_color.get(tension['severity'], "🔵")
            
            st.markdown(f"""
            **{severity_icon} {tension['person']}** - {tension['tension_type']}
            
            *{tension['description']}*
            """)
            
            if tension['evidence']:
                with st.expander(f"Evidence for {tension['person']}"):
                    for evidence in tension['evidence'][:3]:  # Show first 3 pieces of evidence
                        st.markdown(f"• *{evidence}*")
            
            if tension['recommendations']:
                with st.expander(f"Recommendations for {tension['person']}"):
                    for rec in tension['recommendations']:
                        st.markdown(f"• {rec}")
            
            st.markdown("---")
    
    # Team-wide Recommendations
    st.markdown("### 📋 Team-wide Recommendations")
    
    for recommendation in health_report['recommendations']:
        st.markdown(f"• {recommendation}")
    
    # Relationship Network Visualization
    st.markdown("### 🕸️ Team Relationship Network")
    
    relationships = dynamics_analyzer.analyze_relationship_network()
    
    if relationships:
        # Create network visualization data
        nodes = []
        edges = []
        all_people = set()
        
        for person, mentions in relationships.items():
            all_people.add(person)
            for mention in mentions:
                all_people.add(mention['mentioned_person'])
                
                # Color edges by sentiment
                edge_color = 'green' if mention['sentiment'] > 0.2 else 'red' if mention['sentiment'] < -0.2 else 'gray'
                
                edges.append({
                    'from': person,
                    'to': mention['mentioned_person'],
                    'sentiment': mention['sentiment'],
                    'color': edge_color,
                    'context': mention['context']
                })
        
        # Display relationship summary
        st.markdown("**Relationship Sentiment Summary:**")
        
        positive_relationships = len([e for e in edges if e['sentiment'] > 0.2])
        negative_relationships = len([e for e in edges if e['sentiment'] < -0.2])
        neutral_relationships = len(edges) - positive_relationships - negative_relationships
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Positive Mentions", positive_relationships)
        with col2:
            st.metric("Neutral Mentions", neutral_relationships)
        with col3:
            st.metric("Negative Mentions", negative_relationships)
        
        # Show some relationship examples
        if negative_relationships > 0:
            st.markdown("**⚠️ Concerning Relationship Patterns:**")
            negative_edges = [e for e in edges if e['sentiment'] < -0.2]
            for edge in negative_edges[:3]:  # Show first 3
                st.markdown(f"• {edge['from']} → {edge['to']}: *{edge['context']}*")

def display_enhanced_development_plans():
    """Display enhanced development plans with review text analysis"""
    st.header("📈 Enhanced Development Plans")
    
    reviews_df = get_current_data()
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
        
        # Show original review texts
        st.markdown("### 📝 Original Review Texts")
        
        employee_reviews = reviews_df[reviews_df['employee_name'] == selected_employee]
        
        for _, review in employee_reviews.iterrows():
            # Handle date formatting safely
            try:
                if hasattr(review['review_date'], 'strftime'):
                    date_str = review['review_date'].strftime('%Y-%m-%d')
                else:
                    date_str = str(review['review_date'])
            except:
                date_str = str(review['review_date'])
                
            with st.expander(f"Review from {review['reviewer_type']} - {date_str}"):
                st.markdown(f"""
                <div class="review-text-box">
                    {review['review_text']}
                </div>
                """, unsafe_allow_html=True)
                
                # Show extracted scores
                st.markdown("**Extracted Competency Scores:**")
                score_cols = [col for col in review.index if col.endswith('_score')]
                score_data = {col.replace('_score', '').replace('_', ' ').title(): 
                             review[col] for col in score_cols}
                
                score_df = pd.DataFrame(list(score_data.items()), columns=['Competency', 'Score'])
                st.dataframe(score_df, use_container_width=True)
        
        # Development actions (same as before)
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

def get_current_data():
    """Get current dataset from session state or sample data"""
    if 'current_data' in st.session_state:
        return st.session_state.current_data
    else:
        return load_sample_data()

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
        ["Succession Planning", "Development Plans", "Team Dynamics", "Team Analytics", "Raw Data"]
    )
    
    if page == "Succession Planning":
        display_succession_candidates()
    elif page == "Development Plans":
        display_enhanced_development_plans()
    elif page == "Team Dynamics":
        display_team_dynamics()
    elif page == "Team Analytics":
        display_team_analytics()
    elif page == "Raw Data":
        st.header("📋 360-Degree Review Data")
        
        # CSV file upload
        uploaded_file = st.file_uploader(
            "Upload your own 360-degree review data (CSV format)",
            type=['csv'],
            help="Upload a CSV file with columns: employee_name, employee_role, employee_level, years_experience, team_size, reviewer_type, review_date, review_text, and competency scores",
            key="csv_uploader"
        )
        
        # Load data from uploaded file or use sample data
        if uploaded_file is not None:
            try:
                reviews_df = load_csv_data(uploaded_file)
                st.session_state.current_data = reviews_df
                st.session_state.data_source = "uploaded"
                st.success(f"✅ Successfully loaded {len(reviews_df)} records from uploaded file")
            except Exception as e:
                st.error(f"❌ Error loading CSV file: {str(e)}")
                st.info("Using sample data instead...")
                reviews_df = load_sample_data()
                st.session_state.current_data = reviews_df
                st.session_state.data_source = "sample"
        else:
            # If no file uploaded, use current data or sample data
            if 'current_data' in st.session_state:
                reviews_df = st.session_state.current_data
                if st.session_state.get('data_source') == 'uploaded':
                    st.info("📁 Using previously uploaded data. Upload a new file to replace it.")
                else:
                    st.info("📁 Showing sample data. Upload your own CSV file above to use custom data.")
            else:
                reviews_df = load_sample_data()
                st.session_state.current_data = reviews_df
                st.session_state.data_source = "sample"
                st.info("📁 Showing sample data. Upload your own CSV file above to use custom data.")
        
        # Display the data table
        st.dataframe(reviews_df, use_container_width=True)
        
        # Download sample CSV template
        with open("sample_360_reviews.csv", "rb") as file:
            st.download_button(
                label="📥 Download Sample CSV Template",
                data=file.read(),
                file_name="sample_360_reviews.csv",
                mime="text/csv",
                help="Download this sample CSV file as a template for your own data"
            )
        
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