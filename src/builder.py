#!/usr/bin/env python3

import json
import datetime
import os

from conf import BRANCHES, VERSION, ROOT_FOLDER, OUTPUT_FOLDER
from helpers import close


class Builder():
    """
    Handle generation of output files
    """
    def __init__(self, states):
        self.states = states
        self.check_folder()
        self.json_path = ROOT_FOLDER + OUTPUT_FOLDER + "status.json"
        self.html_path = ROOT_FOLDER + OUTPUT_FOLDER + "index.html"

    def check_folder(self):
        try:
            if not os.path.isdir(ROOT_FOLDER + OUTPUT_FOLDER):
                os.makedirs(ROOT_FOLDER + OUTPUT_FOLDER)
        except OSError:
            print("Error: can't create output folder")
            close()


    def write_json_output(self):
        """Generate JSON output"""
        try:
            with open(self.json_path, "w") as json_output:
                json.dump(self.states, json_output, sort_keys=True)
                print("JSON output saved in {}".format(self.json_path))
        except OSError:
            print("Error: can't write JSON output")
            close()


    def write_html_output(self):
        """Generate HTML output"""
        try:
            with open(ROOT_FOLDER + "data/header.html", "r") as header_file:
                header = header_file.read()
            with open(ROOT_FOLDER + "data/footer.html", "r") as footer_file:
                footer = footer_file.read()
        except OSError:
            print("Error: can't read HTML template files")
            close()
        try:
            with open(self.html_path, "w") as index_file:
                header = header.replace("VERSION", "v{}".format(VERSION))
                header = header.replace("DATE", datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
                html_output = header
                for state in self.states:
                    if all(state["branches"]):
                        color = "success"
                    elif any(state["branches"]):
                        color = "warning"
                    else:
                        color = "danger"
                    html_output += "<tr class=\"table-{}\">".format(color)
                    html_output += "<td><a href=\"{url}\">{url}</a></td>".format(url=state["url"])
                    html_output += "<td>{}</td>".format(state["country"].replace("_", " "))
                    html_output += "<td>{}</td>".format(state["protocol"])
                    html_output += "<td>{}</td>".format(state["last_sync"])
                    icon = '<td><img src="../data/img/{}.png" data-toggle="tooltip" data-placement="top" alt="{desc}" title="{desc}"></td>'
                    for i, branch in enumerate(BRANCHES):
                        if state["branches"]:
                            if state["branches"][i]:
                                html_output += icon.format("up", desc="Up to date")
                            else:
                                html_output += icon.format("out", desc="Out of date")
                        else:
                            html_output += icon.format("unknown", desc="Unknown")
                    html_output += "</tr>"
                html_output += footer
                index_file.write(html_output)
                print("HTML output saved in {}".format(self.html_path))
        except OSError:
            print("Error: can't write HTML output")
            close()
