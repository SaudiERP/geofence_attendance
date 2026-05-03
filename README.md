# Geofence Attendance for Odoo 19

Restrict employee attendance check-in / check-out to specific GPS areas,
natively integrated with Odoo's `hr_attendance` module.

## Features

- Per-work-location geofence: enable a toggle and provide latitude, longitude
  and radius (in meters) for each location.
- Two input modes for the geofence center:
  - Manual coordinate entry.
  - Interactive map picker with address search and "Use my location" button.
- Server-side enforcement using the Haversine great-circle formula.
- Works across all Odoo attendance flows: Kiosk Mode, My Attendance, and any
  controller using `_attendance_action_change`.
- Multi-company aware.
- Each attendance record is tagged with the geofence work location that was
  active at the time of check-in.
- English and Arabic translations included.

## Requirements

- Odoo 19.0 (Community or Enterprise).
- Browser geolocation permission must be granted by employees.
- HTTPS is required in production for browser geolocation APIs to work.
- The map picker requires internet access on the manager's computer (see
  *External services* below). Attendance enforcement itself works offline.

## External services

The map picker uses the following free public services. The core attendance
check does not depend on any of them.

| Service | Purpose | Data sent |
|---|---|---|
| Leaflet (`unpkg.com`) | JS/CSS for the map | None |
| OpenStreetMap tile servers | Map background tiles | View coordinates and zoom |
| OpenStreetMap Nominatim | Address search | The text typed in the search box |

These services are queried only when a manager opens the map picker on a
work location form. Employees checking in or out never trigger any of them.

## Installation

1. Copy the `geofence_attendance` folder into your Odoo addons path.
2. Restart the Odoo server with `--update=base` or use Apps → Update Apps List.
3. Search for *Geofence Attendance* and install it.

## Usage

1. Go to **Attendances → Geofence Locations**.
2. Create or edit a location, enable the **Geofence** toggle, and provide:
   - Latitude (decimal degrees, between -90 and 90),
   - Longitude (decimal degrees, between -180 and 180),
   - Allowed radius in meters,
   - Choose **Pick from Map** if you prefer to set the center visually.
3. Assign employees to the configured work location.
4. From this point on, employees on this work location will only be able to
   check in or out from within the configured radius.

## Publishing checklist (before uploading to the Odoo Apps store)

This module ships with placeholder metadata. Replace these before submitting:

- [ ] `__manifest__.py` — `author`
- [ ] `__manifest__.py` — `maintainer`
- [ ] `__manifest__.py` — `website`
- [ ] `__manifest__.py` — `support` (must be a working email address)
- [ ] `static/description/index.html` — review the *Support* section
- [ ] Add at least three real screenshots in `static/description/` named
      `screenshot_1.png`, `screenshot_2.png`, `screenshot_3.png`.

## License

OPL-1 — Odoo Proprietary License v1.0

## Third-party licenses

- Leaflet 1.9.4 — BSD-2-Clause license (compatible with OPL-1).
