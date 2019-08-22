#!/usr/bin/env python
"""
    This module grabs the boid.com team statistics from world community grid and sends it to a prometheus pushgateway
"""

__author__      = "ghobson"
__created__     = ""
__revision__    = ""
__date__        = ""

from prometheus_client import Enum, Gauge, Info, push_to_gateway, pushadd_to_gateway, CollectorRegistry
import requests, time, sys, getopt
from xml.etree import ElementTree as ET

PROMETHEUS_GATEWAY = '127.0.0.1:9091'
PROMETHEUS_JOB = 'boid'
REPORT_TYPE = 'api'
DEBUG = False
WCG_URI="https://www.worldcommunitygrid.org/stat/viewMemberInfo.do?userName=boid.com&xml=true"

def debugmsg(someText):
    if DEBUG:
        sys.stderr.write(someText)

registry = CollectorRegistry()
bLabels = ['report_type']

boidTeamPointsGauge      = Gauge('boid_total_points', 'total generated WCG points', bLabels, registry=registry)
boidTeamResultsGauge     = Gauge('boid_total_results', 'total WCG results', bLabels, registry=registry)
boidTeamDevicesGauge     = Gauge('boid_devices' , 'total WCG devices', bLabels, registry=registry)
boidTeamPointsRankGauge  = Gauge('boid_points_rank', 'points rank', bLabels, registry=registry)
boidTeamResultsRankGauge = Gauge('boid_results_rank', 'results rank', bLabels, registry=registry)

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

    resp = requests.get(WCG_URI)
    if DEBUG:
      print resp

    tree = ET.fromstring(resp.content)

    for devices in tree.findall('.//MemberStat/NumDevices'):
      if DEBUG:
         print("numdevices="+devices.text)
      boidTeamDevicesGauge.labels(report_type=REPORT_TYPE).set(float(devices.text))

    for points in tree.findall('.//MemberStat/StatisticsTotals/Points'):
      boidTeamPointsGauge.labels(report_type=REPORT_TYPE).set(float(points.text))

    for results in tree.findall('.//MemberStat/StatisticsTotals/Results'):
      boidTeamResultsGauge.labels(report_type=REPORT_TYPE).set(float(results.text))

    for pointsR in tree.findall('.//MemberStat/StatisticsTotals/PointsRank'):
      boidTeamPointsRankGauge.labels(report_type=REPORT_TYPE).set(float(pointsR.text))

    for resultsR in tree.findall('.//MemberStat/StatisticsTotals/ResultsRank'):
      boidTeamResultsRankGauge.labels(report_type=REPORT_TYPE).set(float(resultsR.text))

    promFlush()
