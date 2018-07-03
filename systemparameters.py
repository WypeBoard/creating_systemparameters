import csv
import os
import uuid

"""
Mandatory fields
"""
inputFile = ''
outputFile = ''
AttributeFile = ''
InstancePrefix = ''

includesHeaderRow = False  # Skips first row
createTypeAndAttribute = False  # uses row to create type and attributes
overrideToUpdateSql = False

"""
Optional fields, depending on 
    @param includeTypeAndAttribute 
"""
parameterType = ''
parameterTypeId = ''
parameterAttributeId = []


def new_uuid():
    return str(uuid.uuid4())


def replace(string):
    return string.replace(',', ';').strip()


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


def file_exists(file_path):
    if not os.path.isfile(file_path):
        raise FileNotFoundError('File is not found: ' + file_path)


def prep_new_parameters():
    try:
        os.remove(outputFile)
    except OSError:
        pass


def sql_for_type(id, type):
    return 'insert into PARAMETERTYPE (ID,NAVN,OPRETTET,OPRETTETAF,AENDRET,AENDRETAF) values (\'' + id + '\',\'' + type + '\', systimestamp,\'STAMDATA\', systimestamp,\'STAMDATA\');\n'


def sql_for_attribut(id, parameter_type_id, datatype, attribute, mandatory, sort, edit, visable):
    return 'insert into PARAMETERATTRIBUT (ID,PARAMETERTYPE_ID,DATATYPE,NAVN,OBLIGATORISK,SORTERING,IKKE_REDIGERBAR,IKKE_SYNLIG,OPRETTET,OPRETTETAF,AENDRET,AENDRETAF) values (\'' + id + '\',\'' + parameter_type_id + '\',\'' + datatype + '\',\'' + attribute + '\',\'' + mandatory + '\',\'' + sort + '\',\'' + edit + '\',\'' + visable + '\', systimestamp,\'STAMDATA\', systimestamp,\'STAMDATA\');\n'


def sql_for_instance(id, noegle):
    return 'insert into PARAMETERINSTANS (ID,PARAMETERTYPE_ID,NOEGLE,GYLDIG_FRA,OPRETTET,OPRETTETAF,AENDRET,AENDRETAF) values (\'' + id + '\',\'' + parameterTypeId + '\',\'' + noegle + '\',to_date(\'2018-01-01\',\'YYYY-MM-DD\'),systimestamp,\'STAMDATA\',systimestamp,\'STAMDATA\');\n'


def sql_for_value(instance_id, attribut_id, value):
    return 'insert into PARAMETERVAERDI (ID, PARAMETERINSTANS_ID, PARAMETERATTRIBUT_ID, VAERDI, OPRETTET, OPRETTETAF, AENDRET, AENDRETAF) values (\'' + new_uuid() + '\',\'' + instance_id + '\',\'' + attribut_id + '\',\'' + replace(
        value) + '\',systimestamp, \'STAMDATA\', systimestamp, \'STAMDATA\');\n'


def sql_for_update_value(id, value):
    return 'update PARAMETERVAERDI set VAERDI=\'' + replace(value) + '\' where ID=\'' + id + '\';\n'


def create_type_and_attribute(header):
    type_value = header[0]
    data = []
    parameter_type_id = new_uuid()
    parameterTypeId = parameter_type_id
    data.append(sql_for_type(parameter_type_id, type_value))
    csv_read = read_file(AttributeFile)
    for index, row in enumerate(csv_read):
        if len(row) is not 6:
            raise ValueError('Expected 7 arguments: attributename,')
        parameterAttributeId.append(new_uuid())
        data.append(sql_for_attribut(parameterAttributeId[index-1], parameter_type_id, row[0], row[1], row[2], row[3], row[4], row[5]))
    write_file(outputFile, data)
        # with open(AttributeFile, 'r'):
        #    data.append(
        # for i in attributes:
        #    parameterAttributeId.append(new_uuid())
        # predefinition = 'INSERT ALL\nWHEN (c <1) THEN\n'
        # typeString = sql_for_type(parameter_type_id, type)

        # attributeStrings = []
        # for i in range(attributes):
        #    attributeStrings.append(sql_for_attribut(parameterAttributeId[i], attributes[i]))

        # return


def create_instance_and_value(line):
    instance_id = new_uuid()
    data = [sql_for_instance(instance_id, line[0])]
    for index, value in enumerate(line[1:]):
        data.append(sql_for_value(instance_id, parameterAttributeId[index - 1], value))

    write_file(outputFile, data)


def update_values(line):
    data = [sql_for_update_value(line[0], line[1])]
    write_file(outputFile, data)


if __name__ == '__main__':
    """
    Delete old systemparamter outputfile
    """
    prep_new_parameters()
    """
    Read input file content
    """
    if not inputFile:
        raise IOError('inputFile variable is not defined!')
    file_exists(inputFile)
    data = read_file(inputFile)
    """
    First line defines the Type and attributes
    """
    if includesHeaderRow:
        data.pop(0)
    if createTypeAndAttribute:
        header = data.pop(0)
        create_type_and_attribute(header)
    else:
        if parameterTypeId == '':
            raise ValueError('ParameterTypeId is empty.\n'
                             'Find the parameterTypeId you need and put it into the variable parameterTypeId\n'
                             'If you\'re trying to create a new Parameter type flip CreateTypeAndAttribute to True')
    """
    Rest defines the values for each attribute
    """
    if overrideToUpdateSql:
        for line in data:
            update_values(line)
    else:
        for line in data:
            create_instance_and_value(line)
