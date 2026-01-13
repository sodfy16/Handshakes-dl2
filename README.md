# HandshakesDL2 Plugin for Pwnagotchi

**Modified Version:** Includes added delete functionality.  
**Version:** 0.3.0  
**License:** GPL3

## Description

**HandshakesDL2** builds on the HandshakesDL plugin by `evilsocket` https://github.com/evilsocket/pwnagotchi-plugins-contrib/blob/master/handshakes-dl.py with the following enhancements: it lists `.22000` files instead of `.pcap`, plus it allows deletion of the files from the UI.

Specifically designed for modern workflows, it focuses on `.22000` (PMKID/EAPOL) hashcat-formatted files.

This plugin serves as an improved directory browser for your captured handshakes, adding essential management features like searching and deletion which are missing from the default experience.

## Features

- **Web UI Integration:** Adds a dedicated "Handshakes" tab/page to your Pwnagotchi's web interface.
- **Download:** Click to download `.22000` files directly to your computer for cracking.
- **Delete:** Remove unwanted or processed handshake files directly from the UI with a confirmation prompt.
- **Search/Filter:** Real-time filtering of the handshake list to quickly find specific networks.
- **Security:** Includes basic path traversal protection to ensure only handshake files are accessed.

## Installation

1. Copy the `handshakes-dl2.py` file to your Pwnagotchi's custom plugins directory (usually `/etc/pwnagotchi/custom-plugins/` or `/usr/local/share/pwnagotchi/custom-plugins/`).
   
   ```bash
   cp handshakes-dl2.py /usr/local/share/pwnagotchi/custom-plugins/
   ```

2. Enable the plugin in your `config.toml` file.

## Configuration

Add the following to your `/etc/pwnagotchi/config.toml` file:

```toml
main.plugins.handshakes-dl2.enabled = true
```

The plugin automatically detects your handshake directory based on your existing `bettercap.handshakes` configuration.

## Usage

1. Start your Pwnagotchi.
2. Open the Web UI (usually at `http://pwnagotchi.local:8080` or `http://<ip-address>:8080`).
3. Navigate to the plugin page (the URL will be `/plugins/handshakes-dl2`).
4. You will see a list of all captured `.22000` files.
   - **To Download:** Click the filename.
   - **To Delete:** Click the red "Delete" button next to the file.
   - **To Search:** Type in the filter box at the top to narrow down the list.
