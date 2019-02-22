from os import listdir
from os.path import isfile, join
from pathlib import Path
from sys import argv

from invoice_processor import InvoiceXMLProcessor


def get_invoices_from_directory(directory):
    return [join(directory, f) for f in listdir(directory) if isfile(join(directory, f))]


if __name__ == '__main__':
    argv.pop(0)
    if len(argv) < 1:
        raise SystemExit("USAGE: invoice_fixing_tool <input folder> [<output folder>]")
    input_folder = argv.pop(0)
    if len(argv) > 0:
        output_folder = argv.pop(0)
    else:
        output_folder = "{}/fixed/".format(input_folder)
    Path(output_folder).mkdir(parents=True, exist_ok=True)
    invoices = get_invoices_from_directory(input_folder)
    for invoice_file_path in invoices:
        invoice_xml_processor = InvoiceXMLProcessor(invoice_file_path, output_folder)
        invoice_xml_processor.fix_invoice_amounts()
