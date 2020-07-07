import os

from read.consts import instance_dict


def instance_path(instance_name):
    return instance_dict[instance_name]['path']


def open_instance(instance_name):
    file_path = instance_path(instance_name)
    instance = Instance.load_from_file(file_path)

    return instance
