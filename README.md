# Weapons Detection System

A real-time security system that watches a live camera for weapons, then records the event and notifies people who need to know.

## Short description

Webcam weapon detection with a desktop monitor and a web dashboard for alerts, login, and notification history.

## About the project

This project has two parts that work together.

The **desktop client** is a Windows app for an operator at a camera. After signing in, they set a location and who should be notified. The app opens the webcam, runs a YOLOv7 model on each frame, and draws boxes on anything it classifies as a weapon. When a weapon is found, it saves that frame and sends it to the server. Alerts are rate-limited so the same event is not posted every frame.

The **web server** is a Django site for reviewing what the cameras found. Users can register, log in, reset a password, and open a dashboard of detections. Each alert shows the captured image, location, who was notified, and the time. Staff can manage accounts in Django Admin.

When a detection is uploaded, the server can also send an **email** or an **SMS** (Pakistan `+92` numbers) with a link back to that alert.

Typical flow:

1. An operator logs in on the desktop app and starts monitoring a camera.
2. The model flags a weapon and uploads the frame.
3. The dashboard lists the new alert, and the chosen contact gets a message.

The system is meant for local security posts, campuses, or similar sites where a person watches a camera and a supervisor needs a record of incidents.
