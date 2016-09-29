from os import path


class SecureCloudConfig(object):
    local_directory = path.abspath('storage')
    temporary_directory = path.abspath('temp')
