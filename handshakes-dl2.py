import logging
import json
import os
import glob

import pwnagotchi
import pwnagotchi.plugins as plugins

from flask import abort
from flask import send_from_directory
from flask import render_template_string

TEMPLATE = """
{% extends "base.html" %}
{% set active_page = "handshakes" %}

{% block title %}
    {{ title }}
{% endblock %}

{% block styles %}
    {{ super() }}
    <style>
        #filter {
            width: 100%;
            font-size: 16px;
            padding: 12px 20px 12px 40px;
            border: 1px solid #ddd;
            margin-bottom: 12px;
        }
        .file {
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 5px;
        }
        .delete-btn {
            background-color: #dc3545;
            color: white;
            border: none;
            padding: 4px 10px;
            cursor: pointer;
            border-radius: 3px;
            font-size: 12px;
        }
        .delete-btn:hover {
            background-color: #c82333;
        }
    </style>
{% endblock %}
{% block script %}
    var shakeList = document.getElementById('list');
    var filter = document.getElementById('filter');
    var filterVal = filter.value.toUpperCase();

    filter.onkeyup = function() {
        document.body.style.cursor = 'progress';
        var table, tr, tds, td, i, txtValue;
        filterVal = filter.value.toUpperCase();
        li = shakeList.getElementsByTagName("li");
        for (i = 0; i < li.length; i++) {
            txtValue = li[i].textContent || li[i].innerText;
            if (txtValue.toUpperCase().indexOf(filterVal) > -1) {
                li[i].style.display = "list-item";
            } else {
                li[i].style.display = "none";
            }
        }
        document.body.style.cursor = 'default';
    }

    function deleteHandshake(name) {
        if (confirm('Are you sure you want to delete "' + name + '.22000"?')) {
            fetch('/plugins/handshakes-dl2/' + name, {
                method: 'DELETE'
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    location.reload();
                } else {
                    alert('Failed to delete: ' + (data.error || 'Unknown error'));
                }
            })
            .catch(error => {
                alert('Error: ' + error);
            });
        }
    }

{% endblock %}

{% block content %}
    <input type="text" id="filter" placeholder="Search for ..." title="Type in a filter">
    <ul id="list" data-role="listview" style="list-style-type:disc;">
        {% for handshake in handshakes %}
            <li class="file">
                <a href="/plugins/handshakes-dl2/{{handshake}}">{{handshake}}</a>
                <button onclick="deleteHandshake('{{handshake}}')" class="delete-btn">Delete</button>
            </li>
        {% endfor %}
    </ul>
{% endblock %}
"""

class HandshakesDL2(plugins.Plugin):
    __author__ = 'me@sayakb.com'
    __version__ = '0.3.0'
    __license__ = 'GPL3'
    __description__ = 'Download and delete .22000 hashcat captures from web-ui.'

    def __init__(self):
        self.ready = False

    def on_loaded(self):
        logging.info("[HandshakesDL2] plugin loaded")

    def on_config_changed(self, config):
        self.config = config
        self.ready = True

    def on_webhook(self, path, request):
        if not self.ready:
            return "Plugin not ready"

        if path == "/" or not path:
            handshakes = glob.glob(os.path.join(self.config['bettercap']['handshakes'], "*.22000"))
            handshakes = [os.path.basename(path)[:-6] for path in handshakes]
            return render_template_string(TEMPLATE,
                                    title="Handshakes | " + pwnagotchi.name(),
                                    handshakes=handshakes)

        else:
            dir = self.config['bettercap']['handshakes']
            # Validate filename to prevent path traversal
            if '..' in path or '/' in path:
                abort(400)
            
            # Handle DELETE request
            if request.method == 'DELETE':
                try:
                    file_path = os.path.join(dir, path + '.22000')
                    if os.path.exists(file_path):
                        os.remove(file_path)
                        logging.info(f"[HandshakesDL2] deleted {file_path}")
                        return json.dumps({"success": True})
                    else:
                        return json.dumps({"success": False, "error": "File not found"}), 404
                except Exception as e:
                    logging.error(f"[HandshakesDL2] error deleting {path}: {e}")
                    return json.dumps({"success": False, "error": str(e)}), 500
            
            # Handle GET request (download)
            try:
                logging.info(f"[HandshakesDL2] serving {dir}/{path}.22000")
                return send_from_directory(dir, path+'.22000', as_attachment=True)
            except FileNotFoundError:
                abort(404)

