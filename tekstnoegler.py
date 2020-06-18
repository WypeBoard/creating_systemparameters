import csv
import os
import uuid

inputFile = 'tekstnogler.csv'
outputFile = 'tekster.sql'
forKommuneMigraations = True


def new_uuid():
    return str(uuid.uuid4())


def opretTekstnoegle(tekstnogle, tekst, accesskey=''):
    uuid = new_uuid()
    add_kommune = ''
    arguments = ''
    if forKommuneMigraations:
        add_kommune = 'KY_0756.'
    if accesskey:
        arguments = ', GENVEJSTAST=\'' + accesskey + '\''
    query = 'INSERT INTO ' + add_kommune + 'TEKST (ID,SPROG,TEKSTNOEGLE,TEKST,HJAELPETEKST,BESKRIVELSETEKST,FOERTEKST,EFTERTEKST,PLACEHOLDERTEKST,GENVEJSTAST,OPRETTET,OPRETTETAF,AENDRET,AENDRETAF) ' \
                                           'SELECT \'' + uuid + '\',\'da\',\'' + tekstnogle + '\',\'' + tekst + '\',\'\',\'\',\'\',\'\',\'\',\'' + accesskey + '\',systimestamp,\'SYSTEM\',systimestamp,\'SYSTEM\' ' \
                                                                                                                                                               'FROM dual WHERE NOT EXISTS (SELECT 1 FROM ' + add_kommune + 'TEKST WHERE SPROG = \'da\' AND TEKSTNOEGLE = \'' + tekstnogle + '\');\n'
    update = 'UPDATE ' + add_kommune + 'TEKST SET TEKST=\'' + tekst + '\'' + arguments + ' WHERE SPROG=\'da\' AND TEKSTNOEGLE=\'' + tekstnogle + '\';\n'

    with open(outputFile, 'a') as file:
        file.write(query)
        file.write(update)


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
            if not row:
                continue
            if row[0].find('--') == 0:
                continue
            if len(row) == 2:
                opretTekstnoegle(row[0], row[1])
            elif len(row) == 3:
                opretTekstnoegle(row[0], row[1], row[2])
