import logging

logger = logging.getLogger(__name__)

def analyze_bias(entities):
    logger.info("Analyzing Bias")
    report = {"gendered_language": False}
    return report