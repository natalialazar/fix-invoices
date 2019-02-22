Congratulations! You have just been hired to the XML Processing Team in Visma.net AutoInvoice.
It's your first workday and you feel all energetic and ready to get started.
Suddenly you hear some cries for help in the distance. You carefully move closer and BOOM it's your first assignment.
The API Team needs your help!

Some of the invoices they get from customers have the total sum missing or wrong. Your task is to help them by building
something that resolves the total sum of an invoice based on the contents of the file.

Attached are a few examples you can work with.

You can make any kind of an implementation you want, in the language of your choice.

## Running the processor against the given samples:
```
# from the root folder of the project run
python invoice_fixing_tool.py received_invoices
```

## Running the tests:
```
# from the root folder of the project run
python -m unittest discover
```