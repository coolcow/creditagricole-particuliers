import requests
import json
import time
import os
from datetime import datetime, timedelta

class Operation:
    def __init__(self, descr):
        """class init"""
        self.descr = descr
        self.libelleOp = descr["libelleOperation"]
        self.dateOp = descr["dateOperation"]
        self.montantOp = descr["montant"]

    def __str__(self):
        """stre representation"""
        return f"Operation[date={self.dateOp}, libellé={self.libelleOp}, montant={self.montantOp}]"

    def as_json(self):
        """return as json"""
        return json.dumps(self.descr)

class DeferredOperations:
    def __init__(self, session, compteIdx, grandeFamilleCode, carteIdx):
        """
        Initialize deferred card operations manager
        
        Args:
            session (Authenticator): Authentication session
            compteIdx (str): Account index
            grandeFamilleCode (str): Product family code
            carteIdx (str): Card index identifier
        """
        self.session = session
        self.compteIdx = compteIdx
        self.grandeFamilleCode = grandeFamilleCode
        self.carteIdx = carteIdx
        self.list_operations = []

        self.get_operations()

    def __iter__(self):
        """iter"""
        self.n = 0
        return self
        
    def __next__(self):
        """next"""
        if self.n < len(self.list_operations):
            op = self.list_operations[self.n]
            self.n += 1
            return op
        else:
            raise StopIteration
            
    def __len__(self):
        """Return the number of operations"""
        return len(self.list_operations)

    def as_json(self):
        """as json"""
        _ops = []
        for o in self.list_operations:
            _ops.append(o.descr)
        return json.dumps(_ops)
        
    def get_operations(self):
        """
        Retrieves deferred card operations and populates list_operations
        
        Args:
            max_retries (int): Maximum number of retry attempts for temporary errors
            retry_delay (int): Delay in seconds between retry attempts
            
        Raises:
            Exception: If the API request fails after all retries
        """
        mock_file_base = f"card-{self.carteIdx}_operations"
        
        if self.session.useMocks:
            # Use the new read_json_mock method to get raw content
            data = self.session.mock_config.read_json_mock(f"{mock_file_base}_{self.session.mock_config.useMockSuffix}.json")
        else:
            # call operations
            url = "%s" % self.session.url
            url += "/%s/particulier/operations/synthese/detail-comptes/" % self.session.regional_bank_url
            url += "jcr:content.n3.operations.encours.carte.debit.differe.json"
            url += "?grandeFamilleCode=%s&compteIdx=%s&carteIdx=%s" % (self.grandeFamilleCode, self.compteIdx, self.carteIdx)
            r = requests.get(url=url, verify=self.session.ssl_verify, cookies=self.session.cookies)
            if r.status_code != 200:
                raise Exception( "[error] get deferred operations: %s - %s" % (r.status_code, r.text) )
            data = r.text
            
        # Write mock data if requested
        if self.session.writeMocks:
            self.session.mock_config.write_json_mock(f"{mock_file_base}_{self.session.mock_config.writeMockSuffix}.json", data)
           
        # success, save list operations
        for op in json.loads(data):
            self.list_operations.append( Operation(op) )

class Operations:
    def __init__(self, session, compteIdx, grandeFamilleCode, date_start, date_stop, count=100, sleep=None):
        """
        Initialize account operations manager
        
        Args:
            session (Authenticator): Authentication session
            compteIdx (str): Account index
            grandeFamilleCode (str): Product family code
            date_start (str): Start date for operations in ISO 8601 format (YYYY-MM-DD)
            date_stop (str): End date for operations in ISO 8601 format (YYYY-MM-DD)
            count (int, optional): Maximum number of operations to retrieve. Defaults to 100.
            sleep (int or float, optional): Sleep time between paginated requests. Defaults to None.
        """
        self.session = session
        self.compteIdx = compteIdx
        self.grandeFamilleCode = grandeFamilleCode
        self.date_start = date_start
        self.date_stop = date_stop
        self.list_operations = []
        
        self.get_operations(count=count, sleep=sleep)

    def __iter__(self):
        """iter"""
        self.n = 0
        return self
        
    def __next__(self):
        """next"""
        if self.n < len(self.list_operations):
            op = self.list_operations[self.n]
            self.n += 1
            return op
        else:
            raise StopIteration
            
    def __len__(self):
        """Return the number of operations"""
        return len(self.list_operations)

    def as_json(self):
        """as json"""
        _ops = []
        for o in self.list_operations:
            _ops.append(o.descr)
        return json.dumps(_ops)

    def get_operations(self, count, startIndex=None, limit=30, sleep=None):
        """
        Retrieves account operations within date range and populates list_operations
        
        Args:
            count (int): Maximum number of operations to retrieve
            startIndex (str, optional): Starting index for pagination. Defaults to None.
            limit (int, optional): Number of operations to retrieve per request. Defaults to 30.
            sleep (int or float, optional): Sleep time in seconds between paginated requests. Defaults to None.
            
        Raises:
            Exception: If the API request fails
        """
        # convert date to timestamp
        ts_date_debut = datetime.strptime(self.date_start, "%Y-%m-%d")
        ts_date_debut = int(ts_date_debut.timestamp())*1000
        
        ts_date_fin = datetime.strptime(self.date_stop, "%Y-%m-%d")
        ts_date_fin = int(ts_date_fin.timestamp())*1000

        # limit operations to 30
        nextCount = 0
        if count > limit:
            nextCount = count - limit
        
        mock_file_base = f"account-{self.grandeFamilleCode}-{self.compteIdx}_operations"
        
        if self.session.useMocks:
            # Use the new read_json_mock method to get raw content
            data = self.session.mock_config.read_json_mock(f"{mock_file_base}_{self.session.mock_config.useMockSuffix}.json")
            # Wrap the raw content in a listeOperations object
            data = "{ \"listeOperations\": " + data + "}"
        else:
            # call operations resources
            url = "%s" % self.session.url
            url += "/%s/particulier/operations/synthese/detail-comptes/" % self.session.regional_bank_url
            url += "jcr:content.n3.operations.json?grandeFamilleCode=%s&compteIdx=%s" % (self.grandeFamilleCode, self.compteIdx)
            url += "&idDevise=EUR"
            url += "&dateDebut=%s" % ts_date_debut
            if startIndex is not None:
                url += "&startIndex=%s" % requests.utils.quote(startIndex)
            else:
                url += "&dateFin=%s" % ts_date_fin
            url += "&count=%s" % limit
            
            r = requests.get(url=url, verify=self.session.ssl_verify, cookies=self.session.cookies)
            if r.status_code != 200:
                raise Exception( "[error] get operations: %s - %s" % (r.status_code, r.text) )
            data = r.text
            
            # Write mock data if requested
            if self.session.writeMocks:
                operations_data = json.loads(data)["listeOperations"]
                self.session.mock_config.write_json_mock(f"{mock_file_base}_{self.session.mock_config.writeMockSuffix}.json", operations_data)
           
        # success, save list operations
        rsp = json.loads(data)
        for op in rsp["listeOperations"]:
            self.list_operations.append( Operation(op) )

        if nextCount > 0 and 'nextSetStartIndex' in rsp and 'hasNext' in rsp and rsp['hasNext'] is True:
            if sleep is not None and (isinstance(sleep, int) or isinstance(sleep, float)):
                time.sleep(sleep)
            self.get_operations(nextCount, rsp["nextSetStartIndex"])
