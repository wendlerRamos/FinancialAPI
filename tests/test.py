import pytest
#import json
from ..app import *

#Test the ibovespa points route
def test_file1_method1():
    response = app.showIbovespaPoints()
    parsedRespose = json.loads(response)
    assert parsedRespose['current_points'] == None,"test failed"

def test_file1_method2():
    response = app.showPointsForCompany("BA")
    parsedRespose = json.loads(response)
    assert parsedRespose['current_points'] == None,"test failed"
    