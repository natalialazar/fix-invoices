from os.path import basename, join
from xml.etree import ElementTree

from constants import NAMESPACE_MAPPING, TAG_MAPPING
from exceptions import BadXMLFormat


class InvoiceXMLProcessor:

    def __init__(self, input_file_path, output_directory):
        self.input_file_path = input_file_path
        self.output_file_path = self.__get_out_invoice_file_path(input_file_path, output_directory)
        self.dom = ElementTree.parse(self.input_file_path)
        self.root = self.dom.getroot()
        self.total_sum = 0
        [ElementTree.register_namespace(key, val) for key, val in NAMESPACE_MAPPING.items()]
        for tag_name, tag_prefix in TAG_MAPPING.items():
            tag_qualified_name = ElementTree.QName(NAMESPACE_MAPPING[tag_prefix], tag_name)
            setattr(self, tag_name.lower(), tag_qualified_name)

    @staticmethod
    def __get_out_invoice_file_path(input_file_path, output_directory):
        invoice_file_name = basename(input_file_path)
        return join(output_directory.strip(), invoice_file_name)

    def __add_or_set_amount_element(self, item, amount):
        amount_element = item.find(self.amount.text)
        if amount_element is None:
            amount_element = ElementTree.SubElement(item, self.amount)
        amount_element.text = '{:.2f}'.format(amount)

    def __fix_row_amount(self, item):
        quantity = item.find(self.quantity.text)
        price = item.find(self.unitprice.text)
        if quantity is None or price is None:
            raise BadXMLFormat("Missing quantity or price")
        amount = float(quantity.text) * float(price.text)
        self.__add_or_set_amount_element(item, amount)
        return amount

    def __add_totals_element(self):
        totals_element = self.root.find(self.totals.text)
        if not totals_element:
            totals_element = ElementTree.SubElement(self.root, self.totals)
        self.__add_or_set_amount_element(totals_element, self.total_sum)

    def __update_or_add_total_amount(self):
        total_amount_element = self.root.find('./{}/{}'.format(self.totals, self.amount))
        if total_amount_element is None:
            self.__add_totals_element()
        else:
            total_amount_element.text = '{:.2f}'.format(self.total_sum)

    def fix_invoice_amounts(self):
        for row in self.root.findall(self.row.text):
            self.total_sum += self.__fix_row_amount(row)

        self.__update_or_add_total_amount()
        self.dom.write(self.output_file_path)
