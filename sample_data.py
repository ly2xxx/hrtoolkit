import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import re
from typing import Dict, List, Tuple

def generate_360_review_data():
    """Generate sample 360-degree review data with human text reviews for 8 team members"""
    
    # Team structure with personality traits for realistic reviews
    team_members = [
        {"name": "Sarah Chen", "role": "VP Engineering", "level": "VP", "years_experience": 12, "team_size": 8, 
         "traits": ["visionary", "strategic", "inspiring", "sometimes distant"]},
        {"name": "Michael Rodriguez", "role": "Director Product", "level": "Director", "years_experience": 8, "team_size": 5,
         "traits": ["analytical", "detail-oriented", "competitive", "results-driven"]},
        {"name": "Jennifer Kim", "role": "Director Engineering", "level": "Director", "years_experience": 9, "team_size": 6,
         "traits": ["collaborative", "technical", "mentoring", "perfectionist"]},
        {"name": "David Thompson", "role": "Senior Manager", "level": "Manager", "years_experience": 6, "team_size": 4,
         "traits": ["diplomatic", "people-focused", "conflict-averse", "supportive"]},
        {"name": "Lisa Wang", "role": "Product Manager", "level": "Professional", "years_experience": 4, "team_size": 0,
         "traits": ["ambitious", "innovative", "impatient", "high-achiever"]},
        {"name": "Alex Johnson", "role": "Senior Developer", "level": "Professional", "years_experience": 5, "team_size": 0,
         "traits": ["reliable", "technical", "quiet", "methodical"]},
        {"name": "Maria Garcia", "role": "UX Designer", "level": "Professional", "years_experience": 3, "team_size": 0,
         "traits": ["creative", "user-focused", "opinionated", "collaborative"]},
        {"name": "James Wilson", "role": "Junior Developer", "level": "Graduate", "years_experience": 1, "team_size": 0,
         "traits": ["eager", "learning", "sometimes overwhelmed", "hardworking"]}
    ]
    
    # Competency areas for evaluation
    competencies = [
        "Leadership", "Strategic Thinking", "Communication", "Technical Skills",
        "Problem Solving", "Team Collaboration", "Innovation", "Decision Making",
        "Adaptability", "Mentoring", "Customer Focus", "Results Delivery"
    ]
    
    # Review sources
    review_sources = ["Manager", "Peer", "Direct Report", "Cross-functional Partner", "Self"]
    
    # Initialize review text templates and team dynamics
    review_templates = initialize_review_templates()
    team_dynamics = create_team_dynamics_patterns(team_members)
    
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
            
            review_data = {
                "employee_name": person["name"],
                "employee_role": person["role"],
                "employee_level": person["level"],
                "years_experience": person["years_experience"],
                "team_size": person["team_size"],
                "reviewer_type": review_source,
                "review_date": datetime.now() - timedelta(days=random.randint(30, 90))
            }
            
            # Generate human review text first
            other_members = [m for m in team_members if m["name"] != person["name"]]
            review_text = generate_review_text(person, review_source, team_dynamics, 
                                             review_templates, other_members)
            review_data["review_text"] = review_text
            
            # Extract competency scores from the review text
            competency_scores = extract_competency_scores_from_text(review_text, competencies)
            review_data.update(competency_scores)
            
            # Generate qualitative feedback (now more aligned with review text)
            review_data["strengths"] = generate_strengths(person, base_performance)
            review_data["development_areas"] = generate_development_areas(person, base_performance)
            
            # Calculate overall rating from extracted scores
            score_values = [score for key, score in competency_scores.items() if "_score" in key]
            review_data["overall_rating"] = round(np.mean(score_values) if score_values else 0.7, 2)
            
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

def initialize_review_templates() -> Dict:
    """Initialize comprehensive review text templates"""
    return {
        "positive_leadership": [
            "{name} demonstrates exceptional leadership by inspiring the team to achieve ambitious goals",
            "{name} has a natural ability to motivate others and create a positive work environment",
            "{name} effectively guides the team through challenges and provides clear direction",
            "{name} shows strong leadership qualities and is someone people naturally look up to",
            "{name} excels at building consensus and driving team alignment on key initiatives"
        ],
        "negative_leadership": [
            "{name} tends to micromanage and doesn't fully trust the team to deliver",
            "{name} sometimes struggles to make decisive calls when the team needs direction",
            "{name} could improve on delegation and empowering team members to take ownership",
            "{name} occasionally comes across as too directive without seeking input from others",
            "{name} needs to work on building stronger relationships with team members"
        ],
        "positive_communication": [
            "{name} communicates complex ideas clearly and ensures everyone understands the context",
            "{name} is an excellent presenter and can articulate technical concepts to non-technical stakeholders",
            "{name} actively listens to feedback and creates an environment where people feel heard",
            "{name} provides constructive feedback that helps team members grow and improve",
            "{name} effectively facilitates discussions and keeps meetings productive and focused"
        ],
        "negative_communication": [
            "{name} sometimes comes across as dismissive when others present different viewpoints",
            "{name} tends to dominate conversations and doesn't always leave space for others to contribute",
            "{name} could be more diplomatic in how they deliver critical feedback to team members",
            "{name} occasionally struggles to explain technical concepts in accessible ways",
            "{name} needs to improve on following up on commitments made during meetings"
        ],
        "toxic_patterns": [
            "While {name} delivers results, they sometimes take credit for work that was largely done by {other_name}",
            "{name} has a tendency to dismiss {other_name}'s contributions during team meetings",
            "I've noticed that {name} tends to be more supportive of ideas that come from senior team members",
            "{name} occasionally undermines {other_name}'s decisions in front of the broader team",
            "Although {name} collaborates well with most people, there seems to be some tension with {other_name}",
            "{name} sometimes makes comments that could be seen as competitive rather than collaborative"
        ],
        "collaborative_positive": [
            "{name} goes out of their way to help {other_name} succeed and celebrates their achievements",
            "{name} and {other_name} work incredibly well together and complement each other's strengths",
            "{name} consistently gives credit to {other_name} for their contributions to shared projects",
            "{name} actively seeks out {other_name}'s input and values their expertise",
            "{name} has been instrumental in helping {other_name} develop their skills and confidence"
        ]
    }

def create_team_dynamics_patterns(team_members: List[Dict]) -> Dict:
    """Create realistic team dynamics patterns including some toxic behaviors"""
    dynamics = {
        "rivalries": [
            ("Michael Rodriguez", "Lisa Wang"),  # Competitive high-achievers
            ("Alex Johnson", "James Wilson")     # Senior vs Junior developer tension
        ],
        "strong_partnerships": [
            ("Jennifer Kim", "David Thompson"),  # Engineering + Management collaboration
            ("Sarah Chen", "Jennifer Kim"),     # VP and Director alignment
            ("Maria Garcia", "Lisa Wang")       # UX + Product collaboration
        ],
        "mentoring_relationships": [
            ("Jennifer Kim", "James Wilson"),   # Director mentoring Junior
            ("Sarah Chen", "David Thompson"),  # VP developing Manager
            ("Alex Johnson", "James Wilson")   # Senior helping Junior (despite some tension)
        ],
        "credit_attribution_issues": [
            ("Michael Rodriguez", "Lisa Wang"), # Michael sometimes takes credit for Lisa's ideas
            ("Lisa Wang", "Maria Garcia")      # Lisa sometimes overlooks Maria's contributions
        ]
    }
    return dynamics

def extract_competency_scores_from_text(review_text: str, competencies: List[str]) -> Dict[str, float]:
    """Extract competency scores from review text using NLP-like analysis"""
    scores = {}
    
    # Define keyword mappings for each competency
    competency_keywords = {
        "leadership": ["lead", "leadership", "guide", "inspire", "motivate", "direct", "manage", "vision"],
        "strategic_thinking": ["strategy", "strategic", "vision", "planning", "long-term", "roadmap", "future"],
        "communication": ["communicate", "present", "explain", "articulate", "listen", "feedback", "discuss"],
        "technical_skills": ["technical", "coding", "development", "architecture", "implementation", "solution"],
        "problem_solving": ["solve", "problem", "challenge", "issue", "troubleshoot", "debug", "fix"],
        "team_collaboration": ["collaborate", "team", "together", "support", "help", "partnership", "work with"],
        "innovation": ["innovative", "creative", "new", "idea", "improve", "enhance", "breakthrough"],
        "decision_making": ["decision", "decide", "choice", "judgment", "evaluate", "assess", "determine"],
        "adaptability": ["adapt", "flexible", "change", "adjust", "pivot", "evolve", "respond"],
        "mentoring": ["mentor", "coach", "develop", "teach", "guide", "train", "grow", "support"],
        "customer_focus": ["customer", "user", "client", "stakeholder", "requirement", "need", "satisfaction"],
        "results_delivery": ["deliver", "results", "outcome", "achieve", "complete", "success", "performance"]
    }
    
    text_lower = review_text.lower()
    
    for competency in competencies:
        comp_key = competency.lower().replace(" ", "_")
        keywords = competency_keywords.get(comp_key, [])
        
        # Base score from keyword presence
        keyword_score = sum(1 for keyword in keywords if keyword in text_lower) / max(len(keywords), 1)
        
        # Sentiment analysis (simplified)
        positive_words = ["excellent", "outstanding", "great", "strong", "effective", "exceptional", "impressive"]
        negative_words = ["struggle", "weak", "poor", "needs improvement", "lacks", "difficult", "problematic"]
        
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        sentiment_score = (positive_count - negative_count) / max(positive_count + negative_count, 1)
        
        # Combine keyword presence and sentiment
        final_score = min(1.0, max(0.0, (keyword_score * 0.7) + (sentiment_score * 0.3) + 0.5))
        
        # Add some randomness for realism
        final_score += random.uniform(-0.1, 0.1)
        final_score = min(1.0, max(0.0, final_score))
        
        scores[f"{comp_key}_score"] = round(final_score, 2)
    
    return scores

def generate_review_text(reviewee: Dict, reviewer_type: str, team_dynamics: Dict, 
                        templates: Dict, other_team_members: List[Dict]) -> str:
    """Generate realistic review text based on team dynamics and relationships"""
    
    name = reviewee["name"]
    traits = reviewee["traits"]
    level = reviewee["level"]
    
    # Select base template based on performance level and traits
    review_parts = []
    
    # Add positive aspects
    if "visionary" in traits or "strategic" in traits:
        review_parts.append(random.choice(templates["positive_leadership"]).format(name=name))
    
    if "collaborative" in traits or "supportive" in traits:
        review_parts.append(random.choice(templates["positive_communication"]).format(name=name))
    
    # Add some team dynamics
    if reviewer_type == "Peer":
        # Check for rivalries or partnerships
        for rival_name, _ in team_dynamics["rivalries"]:
            if rival_name == name:
                other_name = random.choice([m["name"] for m in other_team_members if m["name"] != name])
                if random.random() < 0.3:  # 30% chance of toxic comment
                    review_parts.append(random.choice(templates["toxic_patterns"]).format(name=name, other_name=other_name))
        
        for partner1, partner2 in team_dynamics["strong_partnerships"]:
            if partner1 == name:
                review_parts.append(random.choice(templates["collaborative_positive"]).format(name=name, other_name=partner2))
            elif partner2 == name:
                review_parts.append(random.choice(templates["collaborative_positive"]).format(name=name, other_name=partner1))
    
    # Add some constructive feedback
    if "perfectionist" in traits and random.random() < 0.4:
        review_parts.append(f"{name} sometimes spends too much time on details and could benefit from focusing on the bigger picture.")
    
    if "competitive" in traits and random.random() < 0.3:
        review_parts.append(f"{name} is very results-driven, but sometimes this competitive nature can create tension in collaborative settings.")
    
    # Add role-specific content
    if level == "VP":
        review_parts.append(f"{name} provides strong strategic direction and has a clear vision for the organization's future.")
    elif level == "Director":
        review_parts.append(f"{name} effectively balances strategic thinking with hands-on execution and team development.")
    elif level == "Graduate":
        review_parts.append(f"{name} shows great potential and is eager to learn, though sometimes needs more guidance on complex projects.")
    
    # Combine parts into coherent review
    if len(review_parts) == 0:
        review_parts.append(f"{name} is a solid contributor who consistently delivers quality work.")
    
    return " ".join(review_parts)

if __name__ == "__main__":
    df = generate_360_review_data()
    df.to_csv("360_reviews_sample.csv", index=False)
    print(f"Generated {len(df)} review records for {df['employee_name'].nunique()} employees")
    print(df.groupby(['employee_name', 'employee_level']).size())