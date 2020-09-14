import logging
from simple_colors import *

from app.bloomon.exceptions import EmptyDetailsException
from app.bloomon.utils import ExtractedInput, BouquetService

logging.basicConfig(
    format="%(levelname)s: %(asctime)s %(message)s", level=logging.DEBUG
)

logger = logging.getLogger(__name__)
intro = f"""
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
{green('Enter stream of bouquet designs and flowers', 'bold')}
{cyan('Bouquet Design:', 'bold')} <name><size><flower x quantity><flower x specie>...<flower N quantity><flower N specie><total quantity of flowers in the bouquet>: {yellow('for example AL8d10r5t30', 'italic')}
{cyan('Flower:', 'bold')} A flower is identified by a flower specie and a flower size: {yellow('for example, rL', 'italic')}.
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
"""
logger.info(intro)

separator = "|"


def raw_input():
    buffer = []
    while True:
        input_attribute = input()
        if input_attribute == "#":
            break
        elif input_attribute == "":
            buffer.append(separator)
            continue
        buffer.append(input_attribute)
    return buffer


def extract_input():
    """Extract User input"""
    user_input = [item for item in raw_input() if item]
    try:
        design, flowers = "\n".join(user_input).split(separator)
    except ValueError:
        raise EmptyDetailsException("Data provided is Insufficient  or invalid")
    return ExtractedInput(design, flowers).extracted_input_data()


try:
    # Create streams of bouquets from received designs and available flowers
    BouquetService(extract_input()).apply()
except Exception as er:
    logger.error(f"Faulty Input: {str(er)} , Try again Please!")
