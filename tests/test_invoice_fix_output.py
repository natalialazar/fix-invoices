from xml.etree import ElementTree
from contextlib import contextmanager
import os
import tempfile
import unittest


from invoice_processor import InvoiceXMLProcessor


@contextmanager
def temp_file(content):
    """Write multiple lines of data into a named temporary xml file.
    """
    temp = tempfile.NamedTemporaryFile(delete=False, suffix='xml')
    temp.write(content.encode())
    temp.close()
    yield temp.name
    os.unlink(temp.name)


class InvoiceFixOutput(unittest.TestCase):

    def check_generated_xml(self, input_xml, expected_xml):
        with temp_file(input_xml) as input_file:
            invoice_processor = InvoiceXMLProcessor(input_file, "")
            invoice_processor.fix_invoice_amounts()
            self.assertEqual(ElementTree.tostring(invoice_processor.dom.getroot(), encoding="unicode"), expected_xml)

    def test_fix_missing_row_amount(self):
        input_xml = '''
        <i:Invoice xmlns:a="ns:amount" xmlns:i="ns:invoice" xmlns:p="ns:price" xmlns:q="ns:quantity" 
                   xmlns:r="ns:row" xmlns:t="ns:totals">
            <t:Totals>
                <a:Amount>20.50</a:Amount>
            </t:Totals>
            <r:Row>
                <q:Quantity>2.00</q:Quantity>
                <p:UnitPrice>10.25</p:UnitPrice>
                <a:Amount/>
            </r:Row>
        </i:Invoice>
        '''
        expected_xml = '''<i:Invoice xmlns:a="ns:amount" xmlns:i="ns:invoice" xmlns:p="ns:price" xmlns:q="ns:quantity" xmlns:r="ns:row" xmlns:t="ns:totals">
            <t:Totals>
                <a:Amount>20.50</a:Amount>
            </t:Totals>
            <r:Row>
                <q:Quantity>2.00</q:Quantity>
                <p:UnitPrice>10.25</p:UnitPrice>
                <a:Amount>20.50</a:Amount>
            </r:Row>
        </i:Invoice>'''
        self.check_generated_xml(input_xml, expected_xml)

    def test_fix_missing_totals_amount(self):
        input_xml = '''
        <i:Invoice xmlns:a="ns:amount" xmlns:i="ns:invoice" xmlns:p="ns:price" xmlns:q="ns:quantity" 
                   xmlns:r="ns:row" xmlns:t="ns:totals">
            <t:Totals>
                <a:Amount/>
            </t:Totals>
            <r:Row>
                <q:Quantity>2.00</q:Quantity>
                <p:UnitPrice>10.25</p:UnitPrice>
                <a:Amount>20.50</a:Amount>
            </r:Row>
        </i:Invoice>
        '''
        expected_xml = '''<i:Invoice xmlns:a="ns:amount" xmlns:i="ns:invoice" xmlns:p="ns:price" xmlns:q="ns:quantity" xmlns:r="ns:row" xmlns:t="ns:totals">
            <t:Totals>
                <a:Amount>20.50</a:Amount>
            </t:Totals>
            <r:Row>
                <q:Quantity>2.00</q:Quantity>
                <p:UnitPrice>10.25</p:UnitPrice>
                <a:Amount>20.50</a:Amount>
            </r:Row>
        </i:Invoice>'''
        self.check_generated_xml(input_xml, expected_xml)

    def test_fix_wrong_amounts(self):
        input_xml = '''
        <i:Invoice xmlns:a="ns:amount" xmlns:i="ns:invoice" xmlns:p="ns:price" xmlns:q="ns:quantity" 
                   xmlns:r="ns:row" xmlns:t="ns:totals">
            <t:Totals>
                <a:Amount>210</a:Amount>
            </t:Totals>
            <r:Row>
                <q:Quantity>2.00</q:Quantity>
                <p:UnitPrice>10.25</p:UnitPrice>
                <a:Amount>21</a:Amount>
            </r:Row>
        </i:Invoice>
        '''
        expected_xml = '''<i:Invoice xmlns:a="ns:amount" xmlns:i="ns:invoice" xmlns:p="ns:price" xmlns:q="ns:quantity" xmlns:r="ns:row" xmlns:t="ns:totals">
            <t:Totals>
                <a:Amount>20.50</a:Amount>
            </t:Totals>
            <r:Row>
                <q:Quantity>2.00</q:Quantity>
                <p:UnitPrice>10.25</p:UnitPrice>
                <a:Amount>20.50</a:Amount>
            </r:Row>
        </i:Invoice>'''
        self.check_generated_xml(input_xml, expected_xml)


if __name__ == '__main__':
    unittest.main()
