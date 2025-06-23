import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Set
import re
from collections import defaultdict, Counter

class TeamDynamicsAnalyzer:
    """Analyzes team dynamics and toxic behaviors from 360-degree review text"""
    
    def __init__(self, reviews_df: pd.DataFrame):
        self.reviews_df = reviews_df
        self.toxic_patterns = self._initialize_toxic_patterns()
        self.positive_patterns = self._initialize_positive_patterns()
        
    def _initialize_toxic_patterns(self) -> Dict[str, List[str]]:
        """Initialize patterns that indicate toxic team dynamics"""
        return {
            "credit_stealing": [
                r"takes credit",
                r"claims (?:the )?(?:idea|work|solution)",
                r"presents (?:my|our) work as (?:their|his|her) own",
                r"doesn't acknowledge",
                r"fails to mention"
            ],
            "dismissive_language": [
                r"but (?:really|actually|honestly)",
                r"however,? (?:they|he|she) (?:doesn't|can't|won't)",
                r"tends to dismiss",
                r"comes across as dismissive",
                r"doesn't listen to",
                r"ignores (?:input|feedback|suggestions)"
            ],
            "undermining_behavior": [
                r"undermines",
                r"contradicts (?:in front of|publicly)",
                r"makes (?:it|them) look bad",
                r"throws (?:under the bus|them under)",
                r"sabotages",
                r"works against"
            ],
            "exclusionary_behavior": [
                r"leaves (?:out|behind)",
                r"doesn't include",
                r"forms (?:cliques|exclusive groups)",
                r"plays favorites",
                r"creates (?:an )?inner circle",
                r"gatekeeps"
            ],
            "competitive_toxicity": [
                r"sees (?:as|them as) (?:a )?threat",
                r"tries to outshine",
                r"competes unhealthily",
                r"zero-sum",
                r"wins at (?:any|all) cost",
                r"puts (?:down|others down)"
            ],
            "microaggression": [
                r"surprising(?:ly)? articulate",
                r"not what I expected",
                r"actually quite good",
                r"for someone (?:like|of)",
                r"pretty good for"
            ]
        }
    
    def _initialize_positive_patterns(self) -> Dict[str, List[str]]:
        """Initialize patterns that indicate positive team dynamics"""
        return {
            "collaboration": [
                r"works (?:well )?together",
                r"collaborates (?:effectively|beautifully)",
                r"complement each other",
                r"strong partnership",
                r"team player",
                r"supports (?:the team|others)"
            ],
            "credit_sharing": [
                r"gives credit",
                r"acknowledges (?:the work|contribution)",
                r"celebrates (?:others|achievements)",
                r"recognizes (?:the effort|input)",
                r"shares (?:the spotlight|recognition)"
            ],
            "mentoring": [
                r"helps (?:develop|grow)",
                r"mentors",
                r"teaches",
                r"guides",
                r"supports (?:learning|development)",
                r"invests in (?:others|people)"
            ],
            "inclusive_behavior": [
                r"includes (?:everyone|all voices)",
                r"makes (?:everyone|people) feel (?:heard|valued)",
                r"creates (?:safe|inclusive) (?:space|environment)",
                r"welcomes (?:different|diverse) (?:perspectives|viewpoints)",
                r"lifts (?:others|people) up"
            ]
        }
    
    def analyze_toxic_behaviors(self) -> Dict[str, Dict]:
        """Analyze toxic behaviors across the team"""
        toxic_analysis = {}
        
        for employee in self.reviews_df['employee_name'].unique():
            employee_reviews = self.reviews_df[
                self.reviews_df['employee_name'] == employee
            ]['review_text'].tolist()
            
            toxic_scores = {}
            toxic_examples = {}
            
            for pattern_type, patterns in self.toxic_patterns.items():
                matches = []
                total_mentions = 0
                
                for review_text in employee_reviews:
                    for pattern in patterns:
                        found = re.findall(pattern, review_text, re.IGNORECASE)
                        if found:
                            matches.extend(found)
                            total_mentions += len(found)
                            # Store example sentences
                            sentences = re.split(r'[.!?]+', review_text)
                            for sentence in sentences:
                                if re.search(pattern, sentence, re.IGNORECASE):
                                    if pattern_type not in toxic_examples:
                                        toxic_examples[pattern_type] = []
                                    toxic_examples[pattern_type].append(sentence.strip())
                
                # Calculate severity score (0-1)
                toxic_scores[pattern_type] = min(1.0, total_mentions / max(len(employee_reviews), 1))
            
            # Calculate overall toxicity score
            overall_toxicity = np.mean(list(toxic_scores.values())) if toxic_scores else 0
            
            toxic_analysis[employee] = {
                'toxicity_scores': toxic_scores,
                'overall_toxicity': overall_toxicity,
                'examples': toxic_examples,
                'risk_level': self._get_risk_level(overall_toxicity)
            }
        
        return toxic_analysis
    
    def analyze_positive_dynamics(self) -> Dict[str, Dict]:
        """Analyze positive team dynamics"""
        positive_analysis = {}
        
        for employee in self.reviews_df['employee_name'].unique():
            employee_reviews = self.reviews_df[
                self.reviews_df['employee_name'] == employee
            ]['review_text'].tolist()
            
            positive_scores = {}
            positive_examples = {}
            
            for pattern_type, patterns in self.positive_patterns.items():
                matches = []
                total_mentions = 0
                
                for review_text in employee_reviews:
                    for pattern in patterns:
                        found = re.findall(pattern, review_text, re.IGNORECASE)
                        if found:
                            matches.extend(found)
                            total_mentions += len(found)
                            # Store example sentences
                            sentences = re.split(r'[.!?]+', review_text)
                            for sentence in sentences:
                                if re.search(pattern, sentence, re.IGNORECASE):
                                    if pattern_type not in positive_examples:
                                        positive_examples[pattern_type] = []
                                    positive_examples[pattern_type].append(sentence.strip())
                
                positive_scores[pattern_type] = min(1.0, total_mentions / max(len(employee_reviews), 1))
            
            overall_positivity = np.mean(list(positive_scores.values())) if positive_scores else 0
            
            positive_analysis[employee] = {
                'positive_scores': positive_scores,
                'overall_positivity': overall_positivity,
                'examples': positive_examples,
                'collaboration_level': self._get_collaboration_level(overall_positivity)
            }
        
        return positive_analysis
    
    def analyze_relationship_network(self) -> Dict[str, List[Dict]]:
        """Analyze relationships and mention patterns between team members"""
        relationships = defaultdict(list)
        all_employees = set(self.reviews_df['employee_name'].unique())
        
        for _, review in self.reviews_df.iterrows():
            reviewee = review['employee_name']
            review_text = review['review_text']
            reviewer_type = review['reviewer_type']
            
            # Find mentions of other employees
            for other_employee in all_employees:
                if other_employee != reviewee and other_employee in review_text:
                    # Analyze sentiment of the mention
                    sentiment = self._analyze_mention_sentiment(review_text, other_employee)
                    
                    relationships[reviewee].append({
                        'mentioned_person': other_employee,
                        'reviewer_type': reviewer_type,
                        'sentiment': sentiment,
                        'context': self._extract_mention_context(review_text, other_employee)
                    })
        
        return dict(relationships)
    
    def identify_team_tensions(self) -> List[Dict]:
        """Identify specific team tensions and conflicts"""
        tensions = []
        toxic_analysis = self.analyze_toxic_behaviors()
        relationships = self.analyze_relationship_network()
        
        # Look for patterns indicating tensions
        for person, toxic_data in toxic_analysis.items():
            if toxic_data['overall_toxicity'] > 0.3:  # High toxicity threshold
                tension = {
                    'person': person,
                    'tension_type': 'Individual Toxic Behavior',
                    'severity': toxic_data['risk_level'],
                    'description': f"{person} shows signs of toxic behavior patterns",
                    'evidence': toxic_data['examples'],
                    'recommendations': self._generate_intervention_recommendations(person, toxic_data)
                }
                tensions.append(tension)
        
        # Look for mutual negative mentions
        for person1, mentions in relationships.items():
            negative_mentions = [m for m in mentions if m['sentiment'] < -0.3]
            if negative_mentions:
                for mention in negative_mentions:
                    person2 = mention['mentioned_person']
                    
                    # Check if it's mutual
                    reverse_mentions = relationships.get(person2, [])
                    mutual_negative = any(
                        m['mentioned_person'] == person1 and m['sentiment'] < -0.3 
                        for m in reverse_mentions
                    )
                    
                    if mutual_negative:
                        tension = {
                            'person': f"{person1} ↔ {person2}",
                            'tension_type': 'Interpersonal Conflict',
                            'severity': 'High' if mention['sentiment'] < -0.6 else 'Medium',
                            'description': f"Mutual negative sentiment between {person1} and {person2}",
                            'evidence': [mention['context']],
                            'recommendations': self._generate_conflict_resolution_recommendations(person1, person2)
                        }
                        tensions.append(tension)
        
        return tensions
    
    def generate_team_health_report(self) -> Dict:
        """Generate comprehensive team health report"""
        toxic_analysis = self.analyze_toxic_behaviors()
        positive_analysis = self.analyze_positive_dynamics()
        tensions = self.identify_team_tensions()
        
        # Calculate team-level metrics
        team_toxicity = np.mean([
            data['overall_toxicity'] for data in toxic_analysis.values()
        ])
        
        team_positivity = np.mean([
            data['overall_positivity'] for data in positive_analysis.values()
        ])
        
        # Identify high-risk individuals
        high_risk_individuals = [
            person for person, data in toxic_analysis.items()
            if data['overall_toxicity'] > 0.4
        ]
        
        # Identify team champions
        team_champions = [
            person for person, data in positive_analysis.items()
            if data['overall_positivity'] > 0.6
        ]
        
        return {
            'team_health_score': round((1 - team_toxicity + team_positivity) / 2, 2),
            'team_toxicity': round(team_toxicity, 2),
            'team_positivity': round(team_positivity, 2),
            'high_risk_individuals': high_risk_individuals,
            'team_champions': team_champions,
            'active_tensions': len(tensions),
            'tension_details': tensions,
            'recommendations': self._generate_team_recommendations(
                team_toxicity, team_positivity, tensions
            )
        }
    
    def _get_risk_level(self, toxicity_score: float) -> str:
        """Convert toxicity score to risk level"""
        if toxicity_score > 0.6:
            return "High"
        elif toxicity_score > 0.3:
            return "Medium"
        else:
            return "Low"
    
    def _get_collaboration_level(self, positivity_score: float) -> str:
        """Convert positivity score to collaboration level"""
        if positivity_score > 0.7:
            return "Excellent"
        elif positivity_score > 0.5:
            return "Good"
        elif positivity_score > 0.3:
            return "Average"
        else:
            return "Needs Improvement"
    
    def _analyze_mention_sentiment(self, text: str, mentioned_person: str) -> float:
        """Analyze sentiment of mentions of other people"""
        # Find sentences containing the mentioned person
        sentences = re.split(r'[.!?]+', text)
        relevant_sentences = [s for s in sentences if mentioned_person in s]
        
        if not relevant_sentences:
            return 0.0
        
        # Simple sentiment analysis
        positive_words = ["great", "excellent", "outstanding", "helpful", "supportive", 
                         "collaborative", "talented", "skilled", "amazing", "wonderful"]
        negative_words = ["dismissive", "difficult", "problematic", "toxic", "undermines", 
                         "takes credit", "competitive", "tension", "conflict", "issues"]
        
        total_sentiment = 0
        for sentence in relevant_sentences:
            sentence_lower = sentence.lower()
            pos_count = sum(1 for word in positive_words if word in sentence_lower)
            neg_count = sum(1 for word in negative_words if word in sentence_lower)
            
            sentence_sentiment = (pos_count - neg_count) / max(pos_count + neg_count, 1)
            total_sentiment += sentence_sentiment
        
        return total_sentiment / len(relevant_sentences)
    
    def _extract_mention_context(self, text: str, mentioned_person: str) -> str:
        """Extract context around mentions of other people"""
        sentences = re.split(r'[.!?]+', text)
        for sentence in sentences:
            if mentioned_person in sentence:
                return sentence.strip()
        return ""
    
    def _generate_intervention_recommendations(self, person: str, toxic_data: Dict) -> List[str]:
        """Generate specific intervention recommendations"""
        recommendations = []
        
        for toxic_type, score in toxic_data['toxicity_scores'].items():
            if score > 0.3:
                if toxic_type == "credit_stealing":
                    recommendations.append(f"Address credit attribution issues with {person} through clear project ownership documentation")
                elif toxic_type == "dismissive_language":
                    recommendations.append(f"Provide communication training for {person} focusing on active listening and respectful dialogue")
                elif toxic_type == "undermining_behavior":
                    recommendations.append(f"Implement conflict resolution process and set clear behavioral expectations with {person}")
                elif toxic_type == "competitive_toxicity":
                    recommendations.append(f"Redirect {person}'s competitive energy toward external goals and team success metrics")
        
        if not recommendations:
            recommendations.append(f"Monitor {person}'s interactions and provide coaching on team collaboration")
        
        return recommendations
    
    def _generate_conflict_resolution_recommendations(self, person1: str, person2: str) -> List[str]:
        """Generate recommendations for resolving interpersonal conflicts"""
        return [
            f"Facilitate mediated discussion between {person1} and {person2}",
            f"Clarify roles and responsibilities to reduce overlap and friction",
            f"Implement structured collaboration protocols for {person1} and {person2}",
            f"Consider temporary project separation while working on relationship repair",
            f"Provide conflict resolution training for both parties"
        ]
    
    def _generate_team_recommendations(self, team_toxicity: float, team_positivity: float, 
                                     tensions: List[Dict]) -> List[str]:
        """Generate team-level recommendations"""
        recommendations = []
        
        if team_toxicity > 0.4:
            recommendations.append("Implement team-wide behavioral guidelines and accountability measures")
            recommendations.append("Conduct anonymous culture survey to identify additional issues")
        
        if team_positivity < 0.4:
            recommendations.append("Increase team building activities and collaboration opportunities")
            recommendations.append("Implement peer recognition program to celebrate positive behaviors")
        
        if len(tensions) > 2:
            recommendations.append("Consider organizational restructuring to reduce interpersonal conflicts")
            recommendations.append("Bring in external team dynamics consultant")
        
        if not recommendations:
            recommendations.append("Maintain current positive team dynamics with regular check-ins")
        
        return recommendations