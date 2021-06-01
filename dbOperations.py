import pymongo
import pandas as pd
import cnfOperations as cnf
import sys


class DbOperation():

    @staticmethod
    def readFromLogCollection(dbName, colName, query={}, no_id=1, datalimit=0):  # query={"devEUI": 1}
        try:
            myClient = pymongo.MongoClient(cnf.cnfOperation.readLogDatabaseClient())
            myDbase = myClient[dbName]
            myTable = myDbase[colName]
            data = myTable.find(query, {"tempLogs": 0}).limit(datalimit)
            df = pd.DataFrame(list(data))

            # Delete the _id
            if no_id:
                del df['_id']

            return df

        except Exception as e:
            print(e.__class__, " occured.")
            print(e.values)
            print("Could not read from log mongodb")
            sys.exit(-1)

    @staticmethod
    def readFromAnalyticsCollection(dbName, colName, query={}, no_id=1):  # query={"devEUI": 1}
        try:
            myClient = pymongo.MongoClient(cnf.cnfOperation.readAnalyticsDatabaseClient())

            myDbase = myClient[dbName]
            myTable = myDbase[colName]

            data = myTable.find(query)

            df = pd.DataFrame(list(data))

            # Delete the _id
            if no_id:
                del df['_id']

            return df

        except Exception as e:
            print(e.__class__, " occured.")
            print("Could not read from log mongodb")
            sys.exit(-1)

    @staticmethod
    def readLastFromAnalyticsCollection(dbName, colName, query={}, no_id=1):  # query={"devEUI": 1}
        try:
            myClient = pymongo.MongoClient(cnf.cnfOperation.readAnalyticsDatabaseClient())

            myDbase = myClient[dbName]
            myTable = myDbase[colName]

            data = myTable.find_one(query, sort=[('datetime', pymongo.DESCENDING)])
            df = pd.DataFrame(list(data))

            # Delete the _id
            if no_id:
                del df['_id']

            return df

        except Exception as e:
            print(e.__class__, " occured.")
            print("Could not read from log mongodb")
            sys.exit(-1)

    @staticmethod
    def writeToAnalyticsCollection(dbName, colName, dfData):
        jsonArray = dfData.to_dict(orient='records')
        print(jsonArray)
        try:
            myClient = pymongo.MongoClient(cnf.cnfOperation.readAnalyticsDatabaseClient())
            myDbase = myClient[dbName]
            myTable = myDbase[colName]

            x = myTable.insert_many(jsonArray)

            return x.inserted_ids

        except Exception as e:
            print(e.__class__, " occured.")
            print("Could not write to mongodb")
            sys.exit(-1)

    @staticmethod
    def deleteAnalyticsCollection(dbName, colName, query={}):

        try:
            myClient = pymongo.MongoClient(cnf.cnfOperation.readAnalyticsDatabaseClient())
            myDbase = myClient[dbName]
            myTable = myDbase[colName]

            x = myTable.delete_many(query)  # query={} deletes all documents in the collection

            print(x.deleted_count, " documents are deleted.")

        except Exception as e:
            print(e.__class__, " occured.")
            print("Could not delete from mongodb")
            sys.exit(-1)

    @staticmethod
    def updateAnalyticsCollection(dbName, colName, query, newValues):

        try:
            myClient = pymongo.MongoClient(cnf.cnfOperation.readAnalyticsDatabaseClient())
            myDbase = myClient[dbName]
            myTable = myDbase[colName]

            # query = {"devEU": 1}
            # newValues = {"$set": {"_data": 24.34}}

            myTable.update_one(query, newValues)

            return 1
        except Exception as e:
            print(e.__class__, " occured.")
            print("Could not update mongodb")
            sys.exit(-1)
