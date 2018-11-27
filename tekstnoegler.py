import csv
import os
import uuid

inputFile = 'tekstnogler.csv'
outputFile = 'tekster.sql'


def new_uuid():
    return str(uuid.uuid4())


def opretTekstnoegle(tekstnogle, tekst):
    uuid = new_uuid()
    query = 'INSERT INTO TEKST (ID,SPROG,TEKSTNOEGLE,TEKST,HJAELPETEKST,BESKRIVELSETEKST,FOERTEKST,EFTERTEKST,PLACEHOLDERTEKST,GENVEJSTAST,OPRETTET,OPRETTETAF,AENDRET,AENDRETAF) ' \
            'SELECT \'' + uuid + '\',\'da\',\'' + tekstnogle + '\',\'' + tekst + '\',\'\',\'\',\'\',\'\',\'\',\'\',systimestamp,\'SYSTEM\',systimestamp,\'SYSTEM\' ' \
                                                                                 'FROM dual WHERE NOT EXISTS (SELECT 1 FROM TEKST WHERE SPROG = \'da\' AND TEKSTNOEGLE = \'' + tekstnogle + '\');\n'
    with open(outputFile, 'a') as file:
        file.write(query)


def prep_new_parameters():
    try:
        os.remove(outputFile)
    except OSError:
        pass


if __name__ == "__main__":
    with open(inputFile, 'r', newline='') as csvFile:
        prep_new_parameters()
        reader = csv.reader(csvFile, delimiter=';', quotechar='|')
        for row in reader:
            opretTekstnoegle(row[0], row[1])
