import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def generate_360_review_data():
    """Generate sample 360-degree review data for 8 team members"""
    
    # Team structure
    team_members = [
        {"name": "Sarah Chen", "role": "VP Engineering", "level": "VP", "years_experience": 12, "team_size": 8},
        {"name": "Michael Rodriguez", "role": "Director Product", "level": "Director", "years_experience": 8, "team_size": 5},
        {"name": "Jennifer Kim", "role": "Director Engineering", "level": "Director", "years_experience": 9, "team_size": 6},
        {"name": "David Thompson", "role": "Senior Manager", "level": "Manager", "years_experience": 6, "team_size": 4},
        {"name": "Lisa Wang", "role": "Product Manager", "level": "Professional", "years_experience": 4, "team_size": 0},
        {"name": "Alex Johnson", "role": "Senior Developer", "level": "Professional", "years_experience": 5, "team_size": 0},
        {"name": "Maria Garcia", "role": "UX Designer", "level": "Professional", "years_experience": 3, "team_size": 0},
        {"name": "James Wilson", "role": "Junior Developer", "level": "Graduate", "years_experience": 1, "team_size": 0}
    ]
    
    # Competency areas for evaluation
    competencies = [
        "Leadership", "Strategic Thinking", "Communication", "Technical Skills",
        "Problem Solving", "Team Collaboration", "Innovation", "Decision Making",
        "Adaptability", "Mentoring", "Customer Focus", "Results Delivery"
    ]
    
    # Review sources
    review_sources = ["Manager", "Peer", "Direct Report", "Cross-functional Partner", "Self"]
    
    reviews_data = []
    
    for person in team_members:
        # Determine number of reviews based on role
        num_reviews = {
            "VP": 8, "Director": 6, "Manager": 5, "Professional": 4, "Graduate": 3
        }[person["level"]]
        
        # Generate base performance tendency (some people are naturally higher performers)
        base_performance = np.random.normal(0.7, 0.1)  # Most people are decent
        if person["name"] in ["Sarah Chen", "Jennifer Kim", "Lisa Wang"]:  # High performers
            base_performance = np.random.normal(0.85, 0.05)
        elif person["name"] in ["James Wilson"]:  # Early career
            base_performance = np.random.normal(0.65, 0.1)
            
        for i in range(num_reviews):
            review_source = np.random.choice(review_sources)
            
            # Adjust scores based on review source bias
            source_bias = {
                "Manager": 0.05, "Peer": 0.0, "Direct Report": 0.1,
                "Cross-functional Partner": -0.05, "Self": 0.15
            }[review_source]
            
            review_data = {
                "employee_name": person["name"],
                "employee_role": person["role"],
                "employee_level": person["level"],
                "years_experience": person["years_experience"],
                "team_size": person["team_size"],
                "reviewer_type": review_source,
                "review_date": datetime.now() - timedelta(days=random.randint(30, 90))
            }
            
            # Generate scores for each competency
            for competency in competencies:
                # Adjust competency scores based on role relevance
                competency_relevance = {
                    ("VP", "Leadership"): 0.2, ("VP", "Strategic Thinking"): 0.2,
                    ("Director", "Leadership"): 0.15, ("Director", "Strategic Thinking"): 0.1,
                    ("Manager", "Leadership"): 0.1, ("Manager", "Team Collaboration"): 0.1,
                    ("Professional", "Technical Skills"): 0.15, ("Professional", "Problem Solving"): 0.1,
                    ("Graduate", "Technical Skills"): 0.1, ("Graduate", "Adaptability"): 0.15
                }.get((person["level"], competency), 0.05)
                
                score = min(1.0, max(0.0, base_performance + source_bias + 
                           np.random.normal(competency_relevance, 0.1)))
                
                review_data[f"{competency.lower().replace(' ', '_')}_score"] = round(score, 2)
            
            # Generate qualitative feedback
            review_data["strengths"] = generate_strengths(person, base_performance)
            review_data["development_areas"] = generate_development_areas(person, base_performance)
            review_data["overall_rating"] = round(np.mean([
                review_data[f"{comp.lower().replace(' ', '_')}_score"] for comp in competencies
            ]), 2)
            
            reviews_data.append(review_data)
    
    return pd.DataFrame(reviews_data)

def generate_strengths(person, performance_level):
    """Generate realistic strengths based on role and performance"""
    strengths_pool = {
        "VP": [
            "Exceptional strategic vision and ability to align teams with company goals",
            "Strong executive presence and stakeholder management skills",
            "Excellent at building high-performing teams and developing talent",
            "Outstanding communication skills across all organizational levels"
        ],
        "Director": [
            "Strong leadership skills and ability to drive team performance",
            "Excellent project management and delivery capabilities",
            "Good strategic thinking and cross-functional collaboration",
            "Effective at mentoring and developing team members"
        ],
        "Manager": [
            "Strong team leadership and people management skills",
            "Excellent at coordinating cross-team initiatives",
            "Good technical knowledge and problem-solving abilities",
            "Effective communicator and team motivator"
        ],
        "Professional": [
            "Strong technical expertise and problem-solving skills",
            "Excellent attention to detail and quality of work",
            "Good collaboration and communication skills",
            "Proactive in taking on new challenges and learning"
        ],
        "Graduate": [
            "Quick learner with strong technical foundation",
            "Enthusiastic and eager to contribute to team success",
            "Good communication skills and team player attitude",
            "Shows potential for growth and development"
        ]
    }
    
    role_strengths = strengths_pool.get(person["level"], strengths_pool["Professional"])
    
    if performance_level > 0.8:
        return random.choice(role_strengths[:2])  # Top strengths for high performers
    else:
        return random.choice(role_strengths)

def generate_development_areas(person, performance_level):
    """Generate realistic development areas based on role and performance"""
    development_pool = {
        "VP": [
            "Could benefit from more hands-on involvement in day-to-day operations",
            "Opportunity to further develop next-generation leadership pipeline",
            "Could enhance digital transformation and innovation leadership"
        ],
        "Director": [
            "Would benefit from developing more strategic thinking capabilities",
            "Opportunity to improve executive communication and presentation skills",
            "Could enhance cross-functional stakeholder management"
        ],
        "Manager": [
            "Would benefit from developing more advanced leadership skills",
            "Opportunity to improve strategic planning and vision setting",
            "Could enhance conflict resolution and difficult conversation skills"
        ],
        "Professional": [
            "Would benefit from developing leadership and mentoring skills",
            "Opportunity to improve strategic thinking and business acumen",
            "Could enhance presentation and executive communication skills"
        ],
        "Graduate": [
            "Would benefit from developing more advanced technical skills",
            "Opportunity to improve project management and planning abilities",
            "Could enhance professional communication and networking skills"
        ]
    }
    
    role_development = development_pool.get(person["level"], development_pool["Professional"])
    return random.choice(role_development)

if __name__ == "__main__":
    df = generate_360_review_data()
    df.to_csv("360_reviews_sample.csv", index=False)
    print(f"Generated {len(df)} review records for {df['employee_name'].nunique()} employees")
    print(df.groupby(['employee_name', 'employee_level']).size())