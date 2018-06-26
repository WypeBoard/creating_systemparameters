import csv
import os
import uuid

"""
Mandatory fields
"""
inputFile = 'satser.csv'
outputfile = 'CopyPasteToFile.sql'
includesHeaderRow = False  # Skips first row
includesTypeAndAttribute = False  # uses row to create type and attributes

"""
Optional fields, depending on 
    @param includeTypeAndAttribute 
"""
parameterType = ''
parameterTypeId = '03b17275-c3d0-40de-8d73-5638e7cd2509'
parameterAttributeId = ['1F65DFDF-1BF7-4D90-B15E-015EE1A2EBA4',
                        '00644694-4794-4A2A-94CA-D84C317371AA']


def new_uuid():
    return str(uuid.uuid4())


def sql_for_type(type):
    return 'INSERT INTO PARAMETERTYPE (ID,NAVN,OPRETTET,OPRETTETAF,AENDRET,AENDRETAF) values (\'' + parameterTypeId + '\',\'' + type + '\', systimestamp,\'STAMDATA\', systimestamp,\'STAMDATA\')';


def sql_for_attribut(id, datatype, attribute, mandatory, sort, edit, visable):
    retur
    #return 'INSERT INTO PARAMETERATTRIBUT (ID,PARAMETERTYPE_ID,DATATYPE,NAVN,OBLIGATORISK,SORTERING,IKKE_REDIGERBAR,IKKE_SYNLIG,OPRETTET,OPRETTETAF,AENDRET,AENDRETAF) values (\'' + id + '\',\'' + parameterTypeId + '\',\'' + datatype + '\',\'' + attribute + '\',\'' + + mandatory + '\','    ', '    N    ', '    N
    #', systimestamp,'
    #STAMDATA
    #', systimestamp,'
    #STAMDATA
    #');


def sql_for_instance(id, noegle):
    return 'INSERT INTO PARAMETERINSTANS (ID,PARAMETERTYPE_ID,NOEGLE,GYLDIG_FRA,OPRETTET,OPRETTETAF,AENDRET,AENDRETAF) ' \
           'VALUES (\'' + id + '\',\'' + parameterTypeId + '\',\'' + noegle + '\',to_date(\'2018-01-01\',' \
                                                                              '\'YYYY-MM-DD\'), ' \
                                                                              'systimestamp,\'STAMDATA\',systimestamp,\'STAMDATA\');\n'


def sql_for_value(instance_id, attribut_id, value):
    return 'INSERT INTO PARAMETERVAERDI (ID, PARAMETERINSTANS_ID, PARAMETERATTRIBUT_ID, VAERDI, OPRETTET, OPRETTETAF, AENDRET, AENDRETAF) ' \
           'VALUES (\'' + new_uuid() + '\',\'' + instance_id + '\',\'' + attribut_id + '\',\'' + value + '\',systimestamp, \'STAMDATA\', systimestamp, \'STAMDATA\');\n'


def create_type_and_attribute(header):
    type = header[0]
    attributes = header[1:]
    parameterTypeId = new_uuid()
    for i in attributes:
        parameterAttributeId.append(new_uuid())
    predefinition = 'INSERT ALL\nWHEN (c <1) THEN\n'
    typeString = sql_for_type(parameterTypeId, type)

    attributeStrings = []
    for i in range(attributes):
        attributeStrings.append(sql_for_attribut(parameterAttributeId[i], attributes[i]))

    return


def create_instance_and_value(line):
    instance_id = new_uuid()
    string_instance = sql_for_instance(instance_id, line[2])
    string_value = []
    for index, value in enumerate(line[:2]):
        string_value.append(sql_for_value(instance_id, parameterAttributeId[index], value))

    with open(outputfile, 'a') as file:
        file.write(string_instance)
        for value in string_value:
            file.write(value)


def prep_new_parameters():
    try:
        os.remove(outputfile)
    except OSError:
        pass


if __name__ == '__main__':
    """
    Delete old systemparamter outputfile
    """
    prep_new_parameters()
    """
    Read from a file called systemparamter.csv
    The file has to be defined as:
    x;y;z
    x1;y1;z1
    
    Note: 
        semicolon (;) seperation
        newline (\n) defines new entry
    """
    with open(inputFile, 'r', newline='') as csvFile:
        """
        First line defines the Type and attributes
        """
        if includesHeaderRow:
            next(csvFile)
        if includesTypeAndAttribute:
            header = next(csvFile)
            create_type_and_attribute(header)

        """
        Rest defines the values for each attribute
        """
        reader = csv.reader(csvFile, delimiter=';', quotechar='|')
        for line in reader:
            create_instance_and_value(line)
