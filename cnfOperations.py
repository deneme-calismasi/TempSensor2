import configparser


class cnfOperation():
    @staticmethod
    def readLineInfo():
        config = configparser.ConfigParser()
        config.read('Config.ini')
        return config['ProjectLines']

    @staticmethod
    def readModBusHost():
        config = configparser.ConfigParser()
        config.read('Config.ini')
        return config['Modbus']['host']

    @staticmethod
    def readLogDatabaseClient():
        config = configparser.ConfigParser()
        config.read('Config.ini')
        return config['LogDatabase']['Client']

    @staticmethod
    def readAnalyticsDatabaseClient():
        config = configparser.ConfigParser()
        config.read('Config.ini')
        return config['AnalyticsDatabase']['Client']

    @staticmethod
    def readForecastDataLimit():
        config = configparser.ConfigParser()
        config.read('Config.ini')
        return config['ForecastModel']['modelDataLimit']

    @staticmethod
    def readTrainTestSplitSize():
        config = configparser.ConfigParser()
        config.read('Config.ini')
        return config['ForecastModel']['trainTestSplitSize']
