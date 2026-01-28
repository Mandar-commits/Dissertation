import logging

logger = logging.getLogger(__name__)

def process_resume(entities):
    logger.info("Processing resume sections")
    entities.skills = list(set(map(str.lower, entities.skills)))
    entities.projects = list(set(entities.projects))
    entities.education = list(set(entities.education))
    return entities
