"""
Solax API is an programming interface for the Solaxcloud. The documentation for this api can be retrieved by the
owner of the service available at https://www.eu.solaxcloud.com/phoebus/resource/files/userGuide/Solax_API_for_End-user_V1.0.pdf
"""
import requests
import json
from types import SimpleNamespace

class SolaxCloud:
    """
    Class provides means to retrieve the current data for an inverter in solax cloud.
    Parameters:
        - apiToken [string] the api key provided https://www.solaxcloud.com/#/api after login
        - serialNumber [string] the serial number of inverter to retrieve data for registered in solax cloud account
    """
    def __init__(self, apiToken = "", serialNumber = ""):
        self.apiToken = apiToken
        self.sn = serialNumber
    
    """
    Retrieve the current data from cloud.
    
    Parameters:
        - asObject [boolean] whether the result should be an object instead of a dict
    
    Returns:
        Depending on the flag the result is either a json object or a dict. The elements of result are documented in the
        https://www.eu.solaxcloud.com/phoebus/resource/files/userGuide/Solax_API_for_End-user_V1.0.pdf
    """
    def json(self, asObject = False):
        r = requests.get("https://www.solaxcloud.com:9443/proxy/api/getRealtimeInfo.do?tokenId={}&sn={}".format(self.apiToken, self.sn))
        if(r.status_code < 200 or r.status_code >= 400):
            raise ConnectionError("Could not retrieve data from solax cloud. Result status code was {}".format(r.status_code))
        if(asObject == True):
            j = json.loads(r.text, object_hook=lambda d: SimpleNamespace(**d))
            if(j.success != True):
                raise ValueError("Unexpected application status: {}".format(j.exception))

            data = j.result
            
            data.inverterStatus = self.__inverterStatus(data.inverterStatus)
            data.inverterType = self.__inverterType(data.inverterType)
        else:
            j = json.loads(r.text)
            if(j['success'] != True):
                raise ValueError("Unexpected application status: {}".format(j['exception']))
            data = j['result']
            data['inverterStatus'] = self.__inverterStatus(data['inverterStatus'])
            data['inverterType'] = self.__inverterType(data['inverterType'])
        return data

    """
    Private helper method to provide a named status instead of a code.
    See also https://www.eu.solaxcloud.com/phoebus/resource/files/userGuide/Solax_API_for_End-user_V1.0.pdf appendix table 5.
    """
    def __inverterStatus(self, statusStr):
        if statusStr == "100":
            return "Wait Mode"
        if statusStr == "101":
            return "Check Mode"
        if statusStr == "102":
            return "Normal Mode"
        if statusStr == "103":
            return "Fault Mode"
        if statusStr == "104":
            return "Permanent Fault Mode"
        if statusStr == "105":
            return "Update Mode"
        if statusStr == "106":
            return "EPS Check Mode"
        if statusStr == "107":
            return "EPS Mode"
        if statusStr == "108":
            return "Self-Test Mode"
        if statusStr == "109":
            return "Idle Mode"
        if statusStr == "110":
            return "Standby Mode"
        if statusStr == "111":
            return "Pv Wake Up Bat Mode"
        if statusStr == "112":
            return "Gen Check Mode"
        if statusStr == "113":
            return "Gen Run Mode"

        return "INVALID STATUS {}".format(statusStr)

    """
    Private helper method to provide a named type instead of code.
    See also https://www.eu.solaxcloud.com/phoebus/resource/files/userGuide/Solax_API_for_End-user_V1.0.pdf appendix table 4.
    """
    def __inverterType(self, typeId):
        if typeId == "1":
            return "X1-LX"
        if typeId == "2":
            return "X-Hybrid"
        if typeId == "3":
            return "X1-Hybrid/Fit"
        if typeId == "4":
            return "X1-Boost/Air/Mini"
        if typeId == "5":
            return "X3-Hybrid/Fit"
        if typeId == "6":
            return "X3-20K/30K"
        if typeId == "7":
            return "X3-MIC/PRO"
        if typeId == "8":
            return "X1-Smart"
        if typeId == "9":
            return "X1-AC"
        if typeId == "10":
            return "A1-Hybrid"
        if typeId == "11":
            return "A1-Fit"
        if typeId == "12":
            return "A1-Grid"
        if typeId == "13":
            return "J1-ESS"

        return "INVALID INVERTER TYPE {}".format(typeId)
