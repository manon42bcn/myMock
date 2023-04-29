from behave import given, then, when, step
import requests
import subprocess

@step('Local myMockServer running')
def run_server(self):
    subprocess.Popen(["python", "../../myMockServer.py"])