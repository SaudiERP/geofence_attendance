<div align="center">

# 🌍 Geofence Attendance

### GPS-Based Attendance Restriction for Odoo 19

[![Odoo](https://img.shields.io/badge/Odoo-19.0-714B67?style=flat-square&logo=odoo)](https://www.odoo.com)
[![License](https://img.shields.io/badge/License-OPL--1-blue?style=flat-square)](https://www.odoo.com/documentation/19.0/legal/licenses.html)
[![SaudiERP](https://img.shields.io/badge/by-SaudiERP-2163E8?style=flat-square)](https://saudierp.work)

**Restrict employee check-in & check-out to specific GPS areas — natively integrated with Odoo Attendances.**

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Support](#-support)

---

</div>

## 📖 Overview

Eliminate buddy-punching and unauthorized remote check-ins. With a simple toggle on each work location, you ensure every attendance event happens within an allowed radius of your office, branch, warehouse, or site.

## ✨ Features

- 🎯 **Per-Location Geofence** — Toggle geofencing on each work location with latitude, longitude, and radius (meters).
- 🗺️ **Interactive Map Picker** — Pick the center visually with address search and "Use my location" button.
- 📐 **Accurate Distance Calculation** — Server-side enforcement using the Haversine great-circle formula.
- 🔄 **Universal Compatibility** — Works in Kiosk Mode, My Attendance, and all `_attendance_action_change` flows.
- 🏢 **Multi-Company Aware** — Full support for multi-company environments.
- 🏷️ **Audit Trail** — Each attendance record is tagged with the geofence work location active at check-in time.
- 🌐 **Bilingual** — Full English & Arabic translations included.

## 📦 Requirements

| Requirement | Details |
|---|---|
| Odoo Version | 19.0 (Community or Enterprise) |
| Browser | Geolocation permission must be granted by employees |
| Hosting | HTTPS required in production for browser geolocation APIs |
| Map Picker | Internet access on manager's computer |

> 💡 **Note:** Attendance enforcement itself works **fully offline** — the internet requirement is only for the map picker UI.

## 🛠️ Installation

1. Copy the `geofence_attendance` folder into your Odoo addons path.
2. Restart the Odoo server with `--update=base` or use **Apps → Update Apps List**.
3. Search for *Geofence Attendance* and install it.

## 🚀 Usage

### Step 1 — Define
Navigate to **Attendances → Geofence Locations**, create or edit a location, enable the **Geofence** toggle, and set:
- **Latitude** (decimal degrees, between -90 and 90)
- **Longitude** (decimal degrees, between -180 and 180)
- **Allowed radius** in meters
- Or choose **Pick from Map** to set the center visually

### Step 2 — Assign
Assign employees to the configured work location.

### Step 3 — Enforce
From this point on, employees on this work location will only be able to check in or out from within the configured radius.

## 🔌 External Services

The map picker uses these free public services. **The core attendance check does not depend on any of them.**

| Service | Purpose | Data Sent |
|---|---|---|
| Leaflet (`unpkg.com`) | JS/CSS for the map | None |
| OpenStreetMap tile servers | Map background tiles | View coordinates and zoom |
| OpenStreetMap Nominatim | Address search | The text typed in the search box |

> These services are queried only when a manager opens the map picker on a work location form. Employees checking in or out never trigger any of them.

## 📜 License

**OPL-1** — Odoo Proprietary License v1.0

### Third-Party Licenses
- Leaflet 1.9.4 — BSD-2-Clause license (compatible with OPL-1)

## 💬 Support

<div align="center">

For questions, bug reports, or custom development requests:

📧 **Email:** [support@saudierp.work](mailto:support@saudierp.work)
🌐 **Website:** [saudierp.work](https://saudierp.work)

---

<sub>Made with ❤️ by **SaudiERP**</sub>

</div>
