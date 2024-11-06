# FileNet Sharing Web App

Effortlessly share files over Wi-Fi! This app allows you to host files from your PC and share them across devices on the same Wi-Fi network. Users can scan a QR code to instantly access and download your files.

## Features

- **Easy Sharing**: Host your local files and make them accessible to others on the same Wi-Fi network.
- **QR Code Access**: Generate a QR code link for quick and simple file access.
- **No Cables or Setup**: All users need to do is connect to the same Wi-Fi and scan the QR code.

## How It Works

1. Run the app on your PC.
2. It will start a local server hosting the files in a specified directory.
3. A unique QR code is generated, linking to your Wi-Fi IP address.
4. Users on the same Wi-Fi network can scan the QR code to view and download your files.

## Getting Started

### Prerequisites

- Python 3.x
- Required libraries: `http.server`, `socket`, `socketserver`, `webbrowser`, `pyqrcode`, `pypng`

Install `pyqrcode` and `pypng` if you haven't already:

```bash
pip install pyqrcode pypng

