# Mother - Dairy Farm Monitoring Dashboard

## Overview

This application is a web-based monitoring dashboard designed for a dairy farm. It provides real-time monitoring of cows through a live video feed, displays various statistics such as the total number of cows detected, milk production, and health scores. The application is built using Flask, a Python web framework, and leverages YOLOv5 for object detection.

## Features

- **Live Video Feed**: Stream a live video feed from YouTube and detect cows in real-time.
- **Dashboard**: Display the total number of cows detected, milk production statistics, and health scores.
- **Login System**: Simple login system with hardcoded credentials (username: `admin`, password: `password123`).

## Prerequisites

- **Python 3.7+** installed on your machine.
- **pip**: Python package installer should be available.
- **Virtual Environment**: It's recommended to use a virtual environment for this project.

## Installation

### Set Up the Virtual Environment

Create and activate a virtual environment:

On Windows:


python -m venv venv
.\venv\Scripts\activate

On mac :
python3 -m venv venv
source venv/bin/activate

### requirements

pip install -r requirements.txt

### run 
python app.py


