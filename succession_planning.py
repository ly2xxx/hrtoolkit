import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
import streamlit as st

class SuccessionPlanningAnalyzer:
    """Analyzes 360-degree reviews to identify succession candidates and create development plans"""
    
    def __init__(self, reviews_df: pd.DataFrame):
        self.reviews_df = reviews_df
        self.competencies = [
            "leadership", "strategic_thinking", "communication", "technical_skills",
            "problem_solving", "team_collaboration", "innovation", "decision_making",
            "adaptability", "mentoring", "customer_focus", "results_delivery"
        ]
        self.level_hierarchy = ["Graduate", "Professional", "Manager", "Director", "VP"]
        
    def calculate_employee_scores(self) -> pd.DataFrame:
        """Calculate aggregated scores for each employee"""
        employee_scores = []
        
        for employee in self.reviews_df['employee_name'].unique():
            emp_data = self.reviews_df[self.reviews_df['employee_name'] == employee]
            
            # Calculate average scores across all competencies
            competency_scores = {}
            for comp in self.competencies:
                comp_col = f"{comp}_score"
                if comp_col in emp_data.columns:
                    competency_scores[comp] = emp_data[comp_col].mean()
            
            # Calculate overall performance score
            overall_score = np.mean(list(competency_scores.values()))
            
            # Get employee metadata
            emp_info = emp_data.iloc[0]
            
            employee_scores.append({
                'name': employee,
                'role': emp_info['employee_role'],
                'level': emp_info['employee_level'],
                'years_experience': emp_info['years_experience'],
                'team_size': emp_info['team_size'],
                'overall_score': overall_score,
                'num_reviews': len(emp_data),
                **competency_scores
            })
        
        return pd.DataFrame(employee_scores)
    
    def identify_succession_candidates(self, target_roles: List[str] = None) -> Dict:
        """Identify top succession candidates for leadership roles"""
        employee_scores = self.calculate_employee_scores()
        
        # Define role progression paths
        succession_paths = {
            "VP Engineering": ["Director", "Manager"],
            "Director Product": ["Manager", "Professional"],
            "Director Engineering": ["Manager", "Professional"],
            "Senior Manager": ["Professional", "Graduate"]
        }
        
        if not target_roles:
            target_roles = list(succession_paths.keys())
        
        succession_candidates = {}
        
        for target_role in target_roles:
            # Find current role holder
            current_holder = employee_scores[
                employee_scores['role'].str.contains(target_role.split()[-1], case=False, na=False)
            ]
            
            if len(current_holder) == 0:
                continue
                
            # Get eligible candidate levels
            eligible_levels = succession_paths.get(target_role, ["Professional", "Manager"])
            
            # Filter candidates
            candidates = employee_scores[
                employee_scores['level'].isin(eligible_levels)
            ].copy()
            
            if len(candidates) == 0:
                continue
            
            # Calculate succession readiness score
            candidates['succession_score'] = self._calculate_succession_score(candidates, target_role)
            
            # Rank candidates
            top_candidates = candidates.nlargest(3, 'succession_score')
            
            succession_candidates[target_role] = {
                'current_holder': current_holder.iloc[0].to_dict() if len(current_holder) > 0 else None,
                'candidates': top_candidates.to_dict('records')
            }
        
        return succession_candidates
    
    def _calculate_succession_score(self, candidates: pd.DataFrame, target_role: str) -> pd.Series:
        """Calculate succession readiness score based on role requirements"""
        
        # Define role-specific competency weights
        role_weights = {
            "VP": {
                "leadership": 0.25, "strategic_thinking": 0.25, "communication": 0.15,
                "decision_making": 0.15, "mentoring": 0.1, "results_delivery": 0.1
            },
            "Director": {
                "leadership": 0.2, "strategic_thinking": 0.2, "communication": 0.15,
                "team_collaboration": 0.15, "problem_solving": 0.15, "results_delivery": 0.15
            },
            "Manager": {
                "leadership": 0.2, "team_collaboration": 0.2, "communication": 0.15,
                "mentoring": 0.15, "problem_solving": 0.15, "results_delivery": 0.15
            }
        }
        
        # Determine target level from role
        target_level = "VP" if "VP" in target_role else "Director" if "Director" in target_role else "Manager"
        weights = role_weights.get(target_level, role_weights["Manager"])
        
        # Calculate weighted competency score
        succession_scores = []
        for _, candidate in candidates.iterrows():
            weighted_score = 0
            for competency, weight in weights.items():
                if competency in candidate:
                    weighted_score += candidate[competency] * weight
            
            # Add experience bonus (up to 10% bonus)
            experience_bonus = min(0.1, candidate['years_experience'] / 100)
            
            # Add team size bonus for leadership roles (up to 5% bonus)
            team_bonus = min(0.05, candidate['team_size'] / 100) if target_level in ["VP", "Director"] else 0
            
            final_score = weighted_score + experience_bonus + team_bonus
            succession_scores.append(final_score)
        
        return pd.Series(succession_scores, index=candidates.index)
    
    def generate_development_plan(self, employee_name: str, target_role: str = None) -> Dict:
        """Generate personalized development plan for an employee"""
        employee_data = self.reviews_df[self.reviews_df['employee_name'] == employee_name]
        
        if len(employee_data) == 0:
            return {"error": "Employee not found"}
        
        # Calculate current competency scores
        current_scores = {}
        for comp in self.competencies:
            comp_col = f"{comp}_score"
            if comp_col in employee_data.columns:
                current_scores[comp] = employee_data[comp_col].mean()
        
        # Get employee info
        emp_info = employee_data.iloc[0]
        current_level = emp_info['employee_level']
        
        # Determine target role if not specified
        if not target_role:
            level_index = self.level_hierarchy.index(current_level)
            if level_index < len(self.level_hierarchy) - 1:
                target_level = self.level_hierarchy[level_index + 1]
                target_role = f"{target_level} Role"
            else:
                target_role = "Senior Leadership Role"
        
        # Identify development gaps
        development_gaps = self._identify_development_gaps(current_scores, target_role)
        
        # Generate development actions
        development_actions = self._generate_development_actions(development_gaps, emp_info)
        
        # Compile qualitative feedback
        strengths = employee_data['strengths'].tolist()
        development_areas = employee_data['development_areas'].tolist()
        
        return {
            'employee_name': employee_name,
            'current_role': emp_info['employee_role'],
            'target_role': target_role,
            'current_scores': current_scores,
            'development_gaps': development_gaps,
            'development_actions': development_actions,
            'strengths': list(set(strengths)),  # Remove duplicates
            'development_areas': list(set(development_areas)),
            'timeline': "12-18 months"
        }
    
    def _identify_development_gaps(self, current_scores: Dict, target_role: str) -> Dict:
        """Identify competency gaps for target role"""
        # Define minimum scores needed for different roles
        role_requirements = {
            "VP": {"leadership": 0.85, "strategic_thinking": 0.85, "communication": 0.80},
            "Director": {"leadership": 0.75, "strategic_thinking": 0.70, "communication": 0.75},
            "Manager": {"leadership": 0.70, "team_collaboration": 0.75, "mentoring": 0.65}
        }
        
        target_level = "VP" if "VP" in target_role else "Director" if "Director" in target_role else "Manager"
        requirements = role_requirements.get(target_level, role_requirements["Manager"])
        
        gaps = {}
        for competency, required_score in requirements.items():
            current_score = current_scores.get(competency, 0)
            if current_score < required_score:
                gaps[competency] = {
                    'current': current_score,
                    'target': required_score,
                    'gap': required_score - current_score
                }
        
        return gaps
    
    def _generate_development_actions(self, gaps: Dict, emp_info: pd.Series) -> List[Dict]:
        """Generate specific development actions based on gaps"""
        action_templates = {
            "leadership": [
                "Enroll in executive leadership program",
                "Take on cross-functional project leadership role",
                "Seek mentoring from senior leadership",
                "Lead a strategic initiative or transformation project"
            ],
            "strategic_thinking": [
                "Participate in strategic planning sessions",
                "Complete MBA or strategic management course",
                "Shadow senior executives in strategic decisions",
                "Lead market analysis or competitive intelligence project"
            ],
            "communication": [
                "Join Toastmasters or executive communication program",
                "Present to board or executive committee",
                "Lead all-hands meetings or town halls",
                "Take on external speaking opportunities"
            ],
            "team_collaboration": [
                "Lead cross-functional team initiative",
                "Facilitate team building workshops",
                "Take on matrix management role",
                "Complete collaborative leadership training"
            ],
            "mentoring": [
                "Become formal mentor to junior staff",
                "Lead graduate development program",
                "Complete coaching certification",
                "Establish mentoring circles or communities"
            ]
        }
        
        actions = []
        for competency, gap_info in gaps.items():
            if competency in action_templates:
                priority = "High" if gap_info['gap'] > 0.15 else "Medium"
                actions.append({
                    'competency': competency.replace('_', ' ').title(),
                    'current_score': round(gap_info['current'], 2),
                    'target_score': round(gap_info['target'], 2),
                    'gap': round(gap_info['gap'], 2),
                    'priority': priority,
                    'recommended_actions': action_templates[competency][:2]  # Top 2 actions
                })
        
        return actions