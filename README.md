# Weapons Detection System

An industrial live-video security platform that detects weapons in real time, records each incident, and notifies the people responsible for response.

## Short description

Enterprise live weapon detection for industrial sites, with on-site monitoring stations and a central operations dashboard for alerts and incident history.

## About the project

The system is built for industrial and enterprise security operations: factories, warehouses, campuses, transport hubs, and other facilities that already run live surveillance. It watches live video, classifies weapons as they appear, and turns each event into a traceable alert for a control room or duty officer.

It has two connected layers.

The **monitoring station** runs at the site. An authorized operator signs in, assigns a location, and names who should be notified. The station processes the live video stream with a YOLOv7 detection model, marks weapons on screen, and forwards a still of the event to the central server. Repeat alerts from the same incident are limited so operations are not flooded.

The **operations platform** is a Django web service for supervisors and security staff. Users register and sign in, recover access if needed, and work from a dashboard of detections. Each alert stores the captured frame, site location, notification target, and timestamp. Administrators manage accounts from the staff console.

When a weapon is confirmed, the platform can send an **email** or **SMS** with a direct link to that incident so the on-call team can act without waiting for a manual report.

Typical operations flow:

1. A station operator starts live monitoring at an assigned site.
2. The model flags a weapon and uploads the incident frame.
3. The operations dashboard records the alert, and the designated contact is notified.

The product is designed to sit beside existing live surveillance, scale across multiple locations, and give industrial security teams a single place to see, verify, and escalate weapon events.
