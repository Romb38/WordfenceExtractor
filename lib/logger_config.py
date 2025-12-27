import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("../wordfence_extractor.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)
