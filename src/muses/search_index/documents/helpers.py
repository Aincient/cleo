import csv
import logging

__all__ = (
    'read_synonyms',
)

LOGGER = logging.getLogger(__name__)


def read_synonyms(path):
    """Read synonyms.

    Read synonyms from the following format:

        word_id;preferred_EN;variant1;variant2;variant3;variant4;variant5
        1;Anatolia;anatolia;anatolie;anatolien;;
        2;Assyria;assyria;assyrie;assyrien;;
        3;Babylonia;babylonia;babylonie;babylonien;;
        4;Byblos;;;;;
        5;Crocodilopolis;;;;;

    What we do:

        - Remove first line (word_id, etc.)
        - Remove first (numbered) elements from each line
        - Remove empty elements (that are produced when reading the CSV)

    :param path:
    :return:
    """
    data = []
    try:
        with open(path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';')
            counter = 0  # Counter so that we skip the first line
            for row in csv_reader:
                # Skip the first line
                if counter == 0:
                    counter += 1
                    continue

                # Remove the first (numbered) element
                row.pop(0)
                # Remove empty elements
                row = [__i.lower() for __i in row if __i]
                if len(row) > 1:
                    # Append remaining (usable) elements separated by comma
                    # to the returned list.
                    data.append(
                        ', '.join(row)
                    )
                counter += 1
    except OSError as err:
        LOGGER.error("Can't read from file {}.".format(path))
        LOGGER.error(err.message)

    LOGGER.debug("Produced synonyms file for {}:".format(path))
    LOGGER.debug(data)

    return data
