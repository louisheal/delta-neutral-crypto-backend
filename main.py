import logging
logger = logging.getLogger(__name__)

from app import app

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    app.run(host="localhost", debug=True)
