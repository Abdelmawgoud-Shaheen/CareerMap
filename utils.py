import json

def get_career_suggestions(user_input, career_data):
    # Tokenize user input and match with career skills
    # For simplicity, let's assume we're matching based on keywords
    keywords = user_input.split()
    career_suggestions = []
    for career in career_data:
        for keyword in keywords:
            if keyword.lower() in [skill.lower() for skill in career['skills']]:
                career_suggestions.append(career)
                break
    return career_suggestions

def generate_learning_roadmap(career_name, skills):
    # Load learning resources for the career
    with open('learning_resources.json') as f:
        learning_resources = json.load(f)
    roadmap = []
    for resource in learning_resources[career_name]:
        roadmap.append(resource['title'] + ': ' + resource['url'])
    return roadmap
