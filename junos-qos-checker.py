#!/usr/bin/env python3
import argparse


def get_arguments():
    """
    Creates an argument parser
    Returns:
        parsed ArgumentParser object
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--src_inventory_file', default='src/inventory.yml',
                       help='specify source inventory *.yml file')
    parser.add_argument('-d', '--dst_result_file', default='dst/result.xlsx',
                        help='specify destination result file *.xlsx')
    args = parser.parse_args()
    return args

def main():
    args = get_arguments()
    print(args)


if __name__ == '__main__':
    main()