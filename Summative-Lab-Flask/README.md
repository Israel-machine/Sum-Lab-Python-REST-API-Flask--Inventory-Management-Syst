# Sum-Lab-Python-REST-API-Flask--Inventory-Management-Syst
FILE SET UP, in terminal run the following commands:

Dependency set up
1. to install python: pipenv install
2. to activate python shell: pipenv shell 
3. to install flask: pip install flask

To start server:
1. python lib/app.py

To start CLI:
1. to see list of commands: python3 main.py --help

List of action | description | command:
{list,add,delete,edit,fetch}
1. list | list all inventory items | python3 main.py list 
2. add | adds new product | python3 main.py add --name "string" --brand "string" --price NUM 
3. delete | delete a product | python3 main.py delete --id NUM 
4. edit | edits name and price of product by id
    only name: python3 main.py edit --id NUM --name "new string"
    only price: python3 main.py edit --id NUM --price NEW_NUM
    update both: python3 main.py edit --id NUM --name "new string" --price NEW_NUM
5. fetch | Fetch product details via barcode from API | python3 main.py fetch --barcode NUM 
