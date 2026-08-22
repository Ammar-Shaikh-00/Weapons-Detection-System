# Weapons Detection System

A live weapon detection platform for industrial sites, campuses, transport hubs, and other public places that need continuous visual monitoring.

## Short description

Live weapon detection for industry and public spaces, with on-site monitoring, a central alert dashboard, and instant notifications.

## About the project

This is a full security system, not a single-camera demo. It is built to sit on live video from existing cameras and to support deployment across factories, warehouses, offices, schools, stations, and similar sites.

The **on-site client** runs at a monitoring point. An operator signs in, sets the site or zone name, and chooses who should be notified. The client reads the live video stream, runs a YOLOv7 detection model on each frame, and marks weapons on screen. When a weapon is found, it stores that frame and sends it to the central server. Repeat alerts from the same event are limited so the system does not flood operators.

The **central server** is a Django web application for supervisors and security staff. They can register, sign in, reset a password, and open a dashboard of all detections. Each alert shows the captured frame, location, who was notified, and the time. Administrators can manage users from Django Admin.

When a detection is uploaded, the server can send an **email** or **SMS** with a link to that alert, so a control room or on-call officer can act without watching every screen.

Typical flow:

1. Live cameras feed the on-site client at a factory floor, gate, lobby, or public concourse.
2. The model flags a weapon and uploads the evidence frame.
3. The dashboard records the incident, and the assigned contact is notified.

The system is intended for industrial security posts and public-place operations where several locations may be watched and a supervisor needs a reliable incident record.
