# SimpleCalculator

## Steps

Run `pip install -r requirement.txt` to install all the libraries in the requirement file.

Run `python manage.py runserver 8080` to start application.  

To run testcases `python manage.py test`.

Import postman collection from `docs/Api Collection.postman_collection.json` and run through the POSTMAN application.

Endpoint 1: `localhost:8080/verify/`, form-data:
| key | third_party_company_name | mandatory |

Endpoint 2: `localhost:8080/transaction/`, form-data
| key | company_name | mandatory |
| key | company_vendor | mandatory |
| key | from_date | mandatory |
| key | to_date | mandatory |


Design of application is in the docs folder.