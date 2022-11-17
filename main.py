#! /usr/bin/python3

import re
import json
import subprocess

def runCommand(method, params, binPath):
    pattern = r'({ \"jsonrpc\".*\"id\" : (?P<id>\w+)[, ].*(\"result\" : (?P<result>.*) |\"error\" : (?P<error>.*) )})'
    regex = re.compile(pattern)
    jsonrpcCommandParams = {
        "jsonrpc" : "2.0",
        "method" : method,
        "params" : params,
        "id" : 1
    }

    jsonrpcCommand = json.dumps(jsonrpcCommandParams);
    consoleCommand = f'echo \'{jsonrpcCommand}\' | sudo env REQUEST_METHOD="POST" {binPath}'
    subprocessOutput = subprocess.Popen(consoleCommand, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
    commandOutput = subprocessOutput.decode("utf-8")
    searchResult = regex.search(commandOutput).group(0)
    result = json.loads(searchResult)

    print(result)

    if 'result' in result:
        return ('result', result['result'])
    if 'error' in result:
        return ('error', result['error']['message'])
    return None



method = "notify"
params = {
    'title' : "[title]",
    'text' : "[text]",
    'type' : "Widget",
    'params' : {
        'applicationId' : "licenseInfoDashboard"
    },
    'id':"abc"
}
binPath = "/home/ubuntu/initi/installation/305/core/solo-jsonrpc"

result = runCommand(method, params, binPath)

print(f"{result=}")
