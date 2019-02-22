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

    @staticmethod
    def _update_or_add_amount(item, relative_path, amount):
        element_for_path = item.find(relative_path)
        if element_for_path is None:
            missing_tags = ", ".join(relative_path.split('/')[1:])
            raise BadXMLFormat("Missing one of the following tags: {}".format(missing_tags))
        element_for_path.text = '{:.2f}'.format(amount)

    def __fix_row_amount(self, item):
        quantity = item.find(self.quantity.text)
        price = item.find(self.unitprice.text)
        if quantity is None or price is None:
            missing_tags = ", ".join([self.quantity.text, self.unitprice.text])
            raise BadXMLFormat("Missing one of the following tags: {}".format(missing_tags))
        amount = float(quantity.text) * float(price.text)
        self._update_or_add_amount(item, './{}'.format(self.amount), amount)
        return amount

    def fix_invoice_amounts(self):
        for row in self.root.findall(self.row.text):
            self.total_sum += self.__fix_row_amount(row)
        self._update_or_add_amount(self.root, './{}/{}'.format(self.totals, self.amount), self.total_sum)

    def fix_invoice_write_output(self):
        self.fix_invoice_amounts()
        self.dom.write(self.output_file_path)
