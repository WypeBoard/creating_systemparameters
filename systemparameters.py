import csv
import os
import random
import string
import uuid

"""
Mandatory fields
"""
parameterType = 'haendelsestype'
parameterTypeId = '53a61d18-f1a8-4b77-933b-5f07cbceajef'

"""
Static fields
"""
attributesIdInInputFile = True  # False if Attributes ID are listed in parameterAttributeId
outputFile = 'SystemparametersOutput.sql'
parameterAttributeId = []
systemparametersInput = 'SystemparametersInput.csv'


def new_uuid():
    return str(uuid.uuid4())


def replace(string):
    return string.replace(',', ';').strip()


def instance_key(size=6, chars=string.ascii_uppercase + string.digits):
    return parameterType + '-' + ''.join(random.choice(chars) for _ in range(size))


def sql_for_instance(id):
    return 'insert into PARAMETERINSTANS (ID, PARAMETERTYPE_ID, NOEGLE, GYLDIG_FRA, OPRETTET, OPRETTETAF, AENDRET, AENDRETAF) values (\'' + id + '\',\'' + parameterTypeId + '\',\'' + instance_key() + '\',to_date(\'2018-01-01\',\'YYYY-MM-DD\'),systimestamp,\'STAMDATA\',systimestamp,\'STAMDATA\');\n'


def sql_for_value(instance_id, attribut_id, value):
    return 'insert into PARAMETERVAERDI (ID, PARAMETERINSTANS_ID, PARAMETERATTRIBUT_ID, VAERDI, OPRETTET, OPRETTETAF, AENDRET, AENDRETAF) values (\'' + new_uuid() + '\',\'' + instance_id + '\',\'' + attribut_id + '\',\'' + replace(
        value) + '\',systimestamp, \'STAMDATA\', systimestamp, \'STAMDATA\');\n'


def create_instance_and_value(line):
    instance_id = new_uuid()
    data = [sql_for_instance(instance_id)]
    for index, value in enumerate(line):
        data.append(sql_for_value(instance_id, parameterAttributeId[index], value))
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
    data = read_file(systemparametersInput)
    """
    First line defines the Attributes
    """
    if attributesIdInInputFile:
        parameterAttributeId = data.pop(0)

    """
    Rest defines the values for each attribute
    """
    for line in data:
        create_instance_and_value(line)
