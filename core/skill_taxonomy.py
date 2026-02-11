
BASE_SKILLS = {
    "python", "java", "sql", "docker", "aws", "kubernetes", "C", "C++", "GO", "html", "css"
    "machine learning", "deep learning", "bootstrap"
    "nlp", "tensorflow", "pytorch",
    "flask", "django", "fastapi", "spring-boot",
    "react", "node", "spark", "hadoop", "angularjs", "fastnode", "javascript",
    "react","node","spark","hadoop","pandas","numpy","scikit",
    "postgres","mysql","mongodb","redis","airflow","git","linux", "rest"
}

SKILL_SYNONYMS = {
    "py": "python",
    "python3": "python",
    "tf": "tensorflow",
    "torch": "pytorch",
    "sklearn": "scikit",
    "k8s": "kubernetes",
    "js": "javascript"
}

def normalize_skills(s):
    s = s.lower().strip()
    return SKILL_SYNONYMS.get(s, s)

def extract_skills_fast(text: str):
    t = text.lower()
    found = set()

    for s in BASE_SKILLS:
        if s in t:
            found.add(normalize_skills(s))

    for syn, base in SKILL_SYNONYMS.items():
        if syn in t:
            found.add(base)

    return sorted(found)