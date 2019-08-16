#!/usr/bin/env python
"""
    This module grabs teamleaderboard information from api.boid.com and sends it to a prometheus pushgateway.
"""

__author__      = "ghobson"
__created__     = ""
__revision__    = ""
__date__        = ""

from prometheus_client import Enum, Gauge, Info, push_to_gateway, pushadd_to_gateway, CollectorRegistry
import requests, json, time, sys, getopt

PROMETHEUS_GATEWAY = '127.0.0.1:9091'
PROMETHEUS_JOB = 'boid'
REPORT_TYPE = 'api'
DEBUG = False

def debugmsg(someText):
    if DEBUG:
        sys.stderr.write(someText)

registry = CollectorRegistry()
bLabels = ['team_name', 'report_type']

boidTeamPowerGauge = Gauge('boid_team_power', 'total team boid power', bLabels, registry=registry)
boidTeamBonusGauge = Gauge('boid_team_bonus', 'team bonus', bLabels, registry=registry)

def logToPrometheus(line):

    name = line['name']
    power = float(line['power'])
    bonus = float(line['bonus'])

    boidTeamPowerGauge.labels(team_name=name, report_type=REPORT_TYPE).set(power)
    boidTeamBonusGauge.labels(team_name=name, report_type=REPORT_TYPE).set(bonus)
    if(DEBUG):
        print(line)
    return True

def promFlush():
    pushadd_to_gateway(PROMETHEUS_GATEWAY, job=PROMETHEUS_JOB, registry=registry)

if __name__ == '__main__':

    null = None
    false = False
    true = True # fix the json below

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hdt:", ["help", "debug", "test"])
    except getopt.error as msg:
        print(msg)
        sys.exit("Invalid arguments.")

    for o, a in opts:
        if o in ("-h", "--help"):
            print("Usage: promgateway -d")
            sys.exit()

        if o in ("-d", "--debug"):
            DEBUG = True

        if o in ("-t", "--test"):
            logToPrometheus(testToc)
            promFlush()
            sys.exit()

    data = json.load(sys.stdin)
    for team in data:
       logToPrometheus(team)
       promFlush()

