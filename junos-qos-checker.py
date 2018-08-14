#!/usr/bin/env python3
import argparse
import yaml
import xmltodict
import time
from ncclient import manager
from ncclient.transport.errors import AuthenticationError, SessionCloseError, SSHError, SSHUnknownHostError
from ncclient.xml_ import *


STATIC_CONNECT_PARAMS = {
    'hostkey_verify': False,
    'device_params': {'name':'junos'}
}

RPC_DICT = {
    'software': 'get-software-information',
    'cos': 'get-cos-interface-information',
    'isis': 'get-isis-interface-information',
    'ospf': 'get-ospf-interface-information',
    'interfaces': 'get-interface-information'
}

def get_arguments():
    """
    Creates an argument parser
    Returns:
        parsed ArgumentParser object
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--src_inventory_file', default='inventory.yml',
                       help='specify source inventory *.yml file')
    parser.add_argument('-d', '--dst_result_file', default='result.xlsx',
                        help='specify destination result file *.xlsx')
    args = parser.parse_args()
    return args


def read_yaml(path="inventory.yml"):
    """
    Reads inventory yaml file and return dictionary with parsed values
    Args:
        path (str): path to inventory YAML
    Returns:
        dict: parsed inventory YAML values
    """
    with open(path) as f:
        yaml_content = yaml.load(f.read())
    return yaml_content


def form_connection_params_from_yaml(parsed_yaml):
    """
    Form dict with connection parameters from parsed_yaml dict
    Args:
        parsed_yaml (dict): dict with parsed yaml file
    Returns:
        dict: keys are a username, password, host
    """
    global_params = parsed_yaml["global credentials"]
    for host_dict in parsed_yaml["hosts"]:
        conn_dict = {}
        conn_dict.update(global_params)
        conn_dict.update(host_dict)
        conn_dict.update(STATIC_CONNECT_PARAMS)
        yield conn_dict


def get_config(conn_dict):
    """
    Setup netconf connection to the device
    Args:
        conn_dict: dict with connection parameters
    Returns:

    """

    
    try:
        with  manager.connect(**conn_dict) as connection:
            rpc = new_ele('get-software-information')
            software_information_xml = connection.rpc(rpc).data_xml
            software_information = xmltodict.parse(software_information_xml)['rpc-reply']['software-information']
            sw_version = software_information['junos-version']
            hostname = software_information['host-name']
            print(f'SW version: {sw_version}')
            print(f'hostname: {hostname}')
    except SSHError:
        print(f'Unable to connect to device: {conn_dict["host"]}')
    except AuthenticationError:  # NCClient auth failure
        print(f'Authentication failed for device: {conn_dict["host"]}')
    except:
        print(f'Unknown error with device: {conn_dict["host"]}')

def main():
    start_time = time.time()
    args = get_arguments()
    parsed_yaml = read_yaml(vars(args)['src_inventory_file'])
    conn_dict = form_connection_params_from_yaml(parsed_yaml)
    for i in conn_dict:
        get_config(i)
    print(f'It took {time.time() - start_time} seconds to run')


if __name__ == '__main__':
    main()