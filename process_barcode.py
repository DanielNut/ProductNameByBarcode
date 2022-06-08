import argparse
import csv

from main import (
    write_barcode_to_not_founded,
    get_barcodes,
    write_number_of_parsed_barcodes,

)


def add_product_to_result(barcode: str, name: str):
    barcodes = get_barcodes()
    last_index = len(barcodes) - barcodes[::-1].index(barcode)
    write_number_of_parsed_barcodes(last_index)
    with open('result.csv', 'a') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter='\t')
        csvwriter.writerow([barcode, name])


def update_data_with_not_founded_barcode(barcode) -> None:
    write_barcode_to_not_founded(barcode)
    barcodes = get_barcodes()
    last_parsed_index = len(barcodes) - barcodes[::-1].index(barcode)
    write_number_of_parsed_barcodes(last_parsed_index)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='My example explanation')

    parser.add_argument(
        '-n',
        '--name',
        type=str,
        help='name of barcode'
    )

    parser.add_argument(
        '-b',
        '--barcode',
        type=str,
        help='barcode'
    )

    my_namespace = parser.parse_args()

    name = my_namespace.name
    barcode = my_namespace.barcode

    if name:
        add_product_to_result(barcode, name)
    else:
        update_data_with_not_founded_barcode(barcode)

