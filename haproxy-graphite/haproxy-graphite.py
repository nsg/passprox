#!/usr/bin/env python3

import socket
import time
import re
import os
import subprocess
import requests


def get_conf(param, default_value=None):
    if os.getenv(param):
        return os.getenv(param)
    else:
        snap_param = param.lower().replace("_", "-")
        out = (
            subprocess.check_output(["snapctl", "get", snap_param])
            .decode("utf-8")
            .strip()
        )
        if out:
            return out
        else:
            return default_value


CARBON_SERVER = get_conf("CARBON_SERVER")
CARBON_PORT = get_conf("CARBON_PORT", 2003)
CARBON_PATH = get_conf("CARBON_PATH", "haproxy")
CARBON_TIME_INTERVAL = int(get_conf("CARBON_TIME_INTERVAL", "10"))

while not CARBON_SERVER or not get_conf("STATS_COLLECT"):
    time.sleep(10)

COLLECT = [] + get_conf("STATS_COLLECT").split(" ")

STATS_URL = get_conf("STATS_URL", "http://127.0.0.1:8080/;csv")
USER = get_conf("STATS_USERNAME", "none")
PASS = get_conf("STATS_PASSWORD", "none")


def save_carbon(path, data, key, rewrite={}):
    if data[key]:

        for rw_reg, replace in rewrite.items():
            if re.match(rw_reg, str(data[key])):
                data[key] = replace

        carbon("{}.{}".format(path, key), data[key])


def carbon(path, value):
    message = "{path} {value} {time}\n".format(
        path=path, value=value, time=int(time.time())
    )

    sock = socket.socket()
    sock.connect((CARBON_SERVER, CARBON_PORT))
    sock.sendall(bytes(message, "utf-8"))
    sock.close()


def do_work():
    req = requests.get(STATS_URL, auth=(USER, PASS))

    if req.status_code == 200:
        for line in req.text.split("\n"):
            fields = line.split(",")

            if len(fields) < 2:
                continue

            if fields[0] in COLLECT:
                # These mappings are returned as the first line in the request
                field_mappings = [
                    "pxname",
                    "svname",
                    "qcur",
                    "qmax",
                    "scur",
                    "smax",
                    "slim",
                    "stot",
                    "bin",
                    "bout",
                    "dreq",
                    "dresp",
                    "ereq",
                    "econ",
                    "eresp",
                    "wretr",
                    "wredis",
                    "status",
                    "weight",
                    "act",
                    "bck",
                    "chkfail",
                    "chkdown",
                    "lastchg",
                    "downtime",
                    "qlimit",
                    "pid",
                    "iid",
                    "sid",
                    "throttle",
                    "lbtot",
                    "tracked",
                    "type",
                    "rate",
                    "rate_lim",
                    "rate_max",
                    "check_status",
                    "check_code",
                    "check_duration",
                    "hrsp_1xx",
                    "hrsp_2xx",
                    "hrsp_3xx",
                    "hrsp_4xx",
                    "hrsp_5xx",
                    "hrsp_other",
                    "hanafail",
                    "req_rate",
                    "req_rate_max",
                    "req_tot",
                    "cli_abrt",
                    "srv_abrt",
                    "comp_in",
                    "comp_out",
                    "comp_byp",
                    "comp_rsp",
                    "lastsess",
                    "last_chk",
                    "last_agt",
                    "qtime",
                    "ctime",
                    "rtime",
                    "ttime",
                ]

                data = {}
                for k, v in enumerate(field_mappings):
                    data[v] = fields[k]

                path = "{}.{}.{}".format(CARBON_PATH, data["pxname"], data["svname"])

                save_carbon(path, data, "qcur")
                save_carbon(path, data, "qmax")
                save_carbon(path, data, "scur")
                save_carbon(path, data, "smax")
                save_carbon(path, data, "slim")
                save_carbon(path, data, "stot")
                save_carbon(path, data, "bin")
                save_carbon(path, data, "bout")
                save_carbon(path, data, "dreq")
                save_carbon(path, data, "dresp")
                save_carbon(path, data, "ereq")
                save_carbon(path, data, "econ")
                save_carbon(path, data, "eresp")
                save_carbon(path, data, "wretr")
                save_carbon(path, data, "wredis")
                save_carbon(
                    path,
                    data,
                    "status",
                    rewrite={"UP": 1, "OPEN": 1, "DOWN.*": 0, "no check": -1},
                )
                save_carbon(path, data, "weight")
                save_carbon(path, data, "act")
                save_carbon(path, data, "bck")
                save_carbon(path, data, "chkfail")
                save_carbon(path, data, "chkdown")
                save_carbon(path, data, "lastchg")
                save_carbon(path, data, "downtime")
                save_carbon(path, data, "qlimit")
                save_carbon(path, data, "check_duration")
                save_carbon(path, data, "hrsp_1xx")
                save_carbon(path, data, "hrsp_2xx")
                save_carbon(path, data, "hrsp_3xx")
                save_carbon(path, data, "hrsp_4xx")
                save_carbon(path, data, "hrsp_5xx")
                save_carbon(path, data, "hrsp_other")
                save_carbon(path, data, "hanafail")
                save_carbon(path, data, "req_rate")
                save_carbon(path, data, "req_rate_max")
                save_carbon(path, data, "req_tot")
                save_carbon(path, data, "cli_abrt")
                save_carbon(path, data, "srv_abrt")
                save_carbon(path, data, "comp_in")
                save_carbon(path, data, "comp_out")
                save_carbon(path, data, "comp_byp")
                save_carbon(path, data, "comp_rsp")
                save_carbon(path, data, "lastsess")
                save_carbon(path, data, "last_chk")
                save_carbon(path, data, "last_agt")
                save_carbon(path, data, "qtime")
                save_carbon(path, data, "ctime")
                save_carbon(path, data, "rtime")
                save_carbon(path, data, "ttime")


def main():
    while True:
        start_ts = time.time()
        do_work()
        now_ts = time.time()
        delta = now_ts - start_ts
        sleep_for = CARBON_TIME_INTERVAL - delta

        if sleep_for < 0:
            sleep_for = 0
            print(
                "[WARNING] Metrics took more than {}s to send, sleep for {}s".format(
                    CARBON_TIME_INTERVAL, sleep_for
                )
            )

        time.sleep(sleep_for)


if __name__ == "__main__":
    main()
