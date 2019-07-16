import csv
import os
import random
import string
import uuid

"""
Static fields
"""
parameterType = ''
parameterTypeId = ''
attributesIdAndTypeInInputFile = True  # False if Attributes ID are listed in parameterAttributeId
outputFile = 'SystemparametersOutput.sql'
parameterAttributeId = []
systemparametersInput = 'SystemparametersInput.csv'


def new_uuid():
    return str(uuid.uuid4())


def replace(string):
    return string.replace(',', ';').strip()


def instance_key(size=6, chars=string.ascii_uppercase + string.digits):
    return parameterType + '-' + ''.join(random.choice(chars) for _ in range(size))


def sql_for_instance(id, noelge):
    return 'INSERT INTO PARAMETERINSTANS (ID, PARAMETERTYPE_ID, NOEGLE, GYLDIG_FRA, OPRETTET, OPRETTETAF, AENDRET, AENDRETAF) VALUES (\'' + id + '\',\'' + parameterTypeId + '\',\'' + noelge + '\',to_date(\'2018-01-01\',\'YYYY-MM-DD\'),systimestamp,\'STAMDATA\',systimestamp,\'STAMDATA\');\n'


def sql_for_value(instance_id, attribut_id, value):
    return 'INSERT INTO PARAMETERVAERDI (ID, PARAMETERINSTANS_ID, PARAMETERATTRIBUT_ID, VAERDI, OPRETTET, OPRETTETAF, AENDRET, AENDRETAF) VALUES (\'' + new_uuid() + '\',\'' + instance_id + '\',\'' + attribut_id + '\',\'' + replace(
        value) + '\',systimestamp, \'STAMDATA\', systimestamp, \'STAMDATA\');\n'


def create_instance_and_value(line):
    instance_id = new_uuid()
    parameter = []
    if len(line) is not len(parameterAttributeId):
        parameter.append(sql_for_instance(instance_id, line[0]))
        for index, value in enumerate(line[1:]):
            parameter.append(sql_for_value(instance_id, parameterAttributeId[index], value))
    else:
        parameter.append(sql_for_instance(instance_id, instance_key()))
        for index, value in enumerate(line):
            parameter.append(sql_for_value(instance_id, parameterAttributeId[index], value))

    write_file(outputFile, parameter)

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
    with open(file_path, 'r', newline='', encoding="utf-8") as file:
        reader = csv.reader(file, delimiter=';', quotechar='|')
        for row in reader:
            if len(row) == 1:
                if row[0].find('--') == 0:
                    continue
            if not row:
                continue
            data.append(row)
    return data


def write_file(file_path, data):
    with open(file_path, 'a', encoding="utf8") as file:
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
    data = read_file(systemparametersInput)
    """
    First line defines the Attributes
    """
    if attributesIdAndTypeInInputFile:
        typeAndId = data.pop(0)
        parameterType = typeAndId[0]
        parameterTypeId = typeAndId[1]
        parameterAttributeId = data.pop(0)

    """
    Rest defines the values for each attribute
    """
    for line in data:
        create_instance_and_value(line)
