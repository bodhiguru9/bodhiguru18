DEFAULT_PASSWORD = "123Zolasen$$"

system_prompt = (
    """Given the word predict type and competency, classify type and competency into one of these categories:
    ['Power', 'Weak'] and ['Active Communication', 'Interpersonal Dynamics', 'Persuasion', 'Negotiation Skills',
    'Information Seeking', 'Accountability', 'Service Focus', 'Sales Presentation', 'Consultative Selling',
    'Advisory & Knowledge Selling', 'Authenticity', 'Upselling & Cross-selling opportunities',
    'Rapport & Relationship management', 'Resilience', 'Agility & Responsiveness', 'Energy & enthusiasm',
    'Taking charge in ambiguity', 'Target & Number Driven', 'Big Picture Orientation', 'Customer Recovery',
    'Empathy', 'Reliability, Responsiveness & Consistency', 'Authoritativeness',
    'Taking Ownership for defaults, Apologizing', 'Handling irate customers', 'Assertiveness under pressure', 
    'Influencing & Persuasion skills', 'Product Knowledge/Domain Expertise', 'Lasting Impression',
    'Story-telling', 'Open and Enthusiastic', 'Articulate', 'Skillful Linkage to Role']"""
)

assistant_content = (
    """Use the following format to define type and competency:\n\nType and Competency"""
)
