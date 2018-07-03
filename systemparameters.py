import csv
import os
import uuid

"""
Mandatory fields
"""
inputFile = 'satser.csv'
outputFile = 'CopyPasteToFile.sql'
includesHeaderRow = False  # Skips first row
includesTypeAndAttribute = False  # uses row to create type and attributes
overrideToUpdateSql = False

"""
Optional fields, depending on 
    @param includeTypeAndAttribute 
"""
parameterType = ''
parameterTypeId = '03b17275-c3d0-40de-8d73-5638e7cd2509'
parameterAttributeId = ['49d6f5b9-f2ce-4438-9b62-5cb042374444',
                        '49d6f5b9-f2ce-4438-9b62-5cb042377410',
                        '49d6f5b9-f2ce-4438-9b62-5cb042377409',
                        '49d6f5b9-f2ce-4438-9b62-5cb042377408']

def new_uuid():
    return str(uuid.uuid4())


def replace(string):
    return string.replace(',', ';').strip()


def sql_for_type(type):
    return 'insert into PARAMETERTYPE (ID,NAVN,OPRETTET,OPRETTETAF,AENDRET,AENDRETAF) values (\'' + parameterTypeId + '\',\'' + type + '\', systimestamp,\'STAMDATA\', systimestamp,\'STAMDATA\');\n'


def sql_for_attribut(id, datatype, attribute, mandatory, sort, edit, visable):
    return 'insert into PARAMETERATTRIBUT (ID,PARAMETERTYPE_ID,DATATYPE,NAVN,OBLIGATORISK,SORTERING,IKKE_REDIGERBAR,IKKE_SYNLIG,OPRETTET,OPRETTETAF,AENDRET,AENDRETAF) values (\'' + id + '\',\'' + parameterTypeId + '\',\'' + datatype + '\',\'' + attribute + '\',\'' + mandatory + '\',\'' + sort + '\',\'' + edit + '\',\'' + visable + '\', systimestamp,\'STAMDATA\', systimestamp,\'STAMDATA\');\n'


def sql_for_instance(id, noegle):
    return 'insert into PARAMETERINSTANS (ID,PARAMETERTYPE_ID,NOEGLE,GYLDIG_FRA,OPRETTET,OPRETTETAF,AENDRET,AENDRETAF) values (\'' + id + '\',\'' + parameterTypeId + '\',\'' + noegle + '\',to_date(\'2018-01-01\',\'YYYY-MM-DD\'),systimestamp,\'STAMDATA\',systimestamp,\'STAMDATA\');\n'


def sql_for_value(instance_id, attribut_id, value):
    return 'insert into PARAMETERVAERDI (ID, PARAMETERINSTANS_ID, PARAMETERATTRIBUT_ID, VAERDI, OPRETTET, OPRETTETAF, AENDRET, AENDRETAF) values (\'' + new_uuid() + '\',\'' + instance_id + '\',\'' + attribut_id + '\',\'' + replace(
        value) + '\',systimestamp, \'STAMDATA\', systimestamp, \'STAMDATA\');\n'


def sql_for_update_value(id, value):
    return 'update PARAMETERVAERDI set VAERDI=\'' + replace(value) + '\' where ID=\'' + id + '\';\n'


def create_type_and_attribute(header):
    type = header[0]
    with open(header[1], 'r', ):
        attributes = header[1:]
    parameter_type_id = new_uuid()
    for i in attributes:
        parameterAttributeId.append(new_uuid())
    predefinition = 'INSERT ALL\nWHEN (c <1) THEN\n'
    typeString = sql_for_type(parameter_type_id, type)

    attributeStrings = []
    for i in range(attributes):
        attributeStrings.append(sql_for_attribut(parameterAttributeId[i], attributes[i]))

    return


def create_instance_and_value(line):
    instance_id = new_uuid()
    data = [sql_for_instance(instance_id, line[0])]
    for index, value in enumerate(line[1:]):
        data.append(sql_for_value(instance_id, parameterAttributeId[index-1], value))

    write_file(outputFile, data)


def update_values(line):
    data = [sql_for_update_value(line[0], line[1])]
    write_file(outputFile, data)


def read_file(file_path):
    """
    Read from a file called systemparamter.csv
    The file has to be defined as:
    x;y;z
    x1;y1;z1

    Note:
        semicolon (;) seperation
        newline (\n) defines new entry
    """
    data = []
    with open(file_path, 'r', newline='') as file:
        reader = csv.reader(file, delimiter=';', quotechar='|')
        for row in reader:
            data.append(row)
    return data


def write_file(file_path, data):
    with open(file_path, 'a') as file:
        for row in data:
            file.write(row)


def prep_new_parameters():
    try:
        os.remove(outputFile)
    except OSError:
        pass


if __name__ == '__main__':
    """
    Delete old systemparamter outputfile
    """
    prep_new_parameters()
    """
    Read input file content
    """
    data = read_file(inputFile)
    """
    First line defines the Type and attributes
    """
    if includesHeaderRow:
        data.pop(0)
    if includesTypeAndAttribute:
        header = data.pop(0)
        create_type_and_attribute(header)
    """
    Rest defines the values for each attribute
    """
    if overrideToUpdateSql:
        for line in data:
            update_values(line)
    else:
        for line in data:
            create_instance_and_value(line)
