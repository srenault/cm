simple-bank-api
===============

This is a lightweight python 3 API designed to extract data from banks.

Example
-------

Here is an example of how we can use the API:

.. code-block:: python

    import datetime

    from simplebank.bank import CreditMutuel

    date = datetime.datetime.now()

    with CreditMutuel('login', 'password') as cm:
        accounts = cm.list_accounts()
        for acc in accounts:
            print(cm.fetch_last_operations(acc.id))

    print('execution time: ' + str((datetime.datetime.now() - date).total_seconds()) + 's')
