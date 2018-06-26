import csv

def opretTekstnoegle(tekstnogle, tekst):
    query = 'INSERT INTO TEKST (ID,SPROG,TEKSTNOEGLE,TEKST,HJAELPETEKST,BESKRIVELSETEKST,FOERTEKST,EFTERTEKST,PLACEHOLDERTEKST,GENVEJSTAST,OPRETTET,OPRETTETAF,AENDRET,AENDRETAF) ' \
            'SELECT sys_guid(),\'da\',\'' + tekstnogle + '\',\'' + tekst + '\',\'\',\'\',\'\',\'\',\'\',\'\',systimestamp,\'SYSTEM\',systimestamp,\'SYSTEM\' ' \
            'FROM dual WHERE NOT EXISTS (SELECT 1 FROM TEKST WHERE SPROG = \'da\' AND TEKSTNOEGLE = \'' + tekstnogle + '\')\n/\n'
    update = 'UPDATE TEKST SET TEKST=\'' + tekst + '\' WHERE TEKSTNOEGLE=\'' + tekstnogle + '\' AND dbms_lob.compare(TEKST, to_clob(TEKSTNOEGLE)) = 0\n/\n'

    with open('tekster.sql', 'a') as file:
        file.write(query)
        file.write(update)

if __name__ == "__main__":
    with open('tekstnogler.csv', 'r', newline='') as csvFile:
        reader = csv.reader(csvFile, delimiter=';', quotechar='|')
        for row in reader:
            opretTekstnoegle(row[0], row[1])
