# -----------------------------------------------------------------------------
# Before publishing on the Odoo Apps store, replace the four PLACEHOLDER
# values below (author, maintainer, website, support) with your real
# company details. Odoo Store rejects modules with placeholder metadata.
# -----------------------------------------------------------------------------
{
    'name': 'Geofence Attendance',
    'version': '19.0.1.2.0',
    'category': 'Human Resources/Attendances',
    'summary': 'Restrict attendance check-in/out to specific GPS areas, with interactive map picker',
    'description': """
Geofence Attendance
===================

Adds geofencing capability to Odoo's native Attendance module. Employees may
only check in or out from within a configured geographic radius linked to
their assigned work location.

Key features
------------
* Per-work-location geofence toggle, latitude, longitude and radius (meters).
* Two ways to set the geofence center:
  - Enter coordinates manually.
  - Pick a point from an interactive map with address search and "Use my
    location" button.
* Real-world distance calculation using the Haversine formula.
* Enforced on every check-in/check-out across all entry points
  (Kiosk, My Attendance page, frontend, and API).
* Native integration with Odoo's existing GPS capture.
* Read-only geofence summary on the employee form.
* Multilingual: ships with English and Arabic translations.

External services
-----------------
The map picker (used by HR managers when configuring a work location) relies
on the following free public services:

* Leaflet 1.9.4 loaded from the unpkg CDN — provides the map JavaScript
  and stylesheet.
* OpenStreetMap tile servers — serve the visual map tiles.
* OpenStreetMap Nominatim — used when the manager types in the search box.

The runtime attendance check (the core feature of this module) is fully
self-contained and does not contact any external service.

Compatibility
-------------
Odoo 19.0 Community and Enterprise. Depends only on the standard
``hr_attendance`` module.
""",
    # ---------------- REPLACE THESE FOUR LINES BEFORE PUBLISHING ----------------
    'author': 'SaudiERP',
    'maintainer': 'SaudiERP',
    'website': 'https://saudierp.work',
    'support': 'support@saudierp.work',
    # ---------------------------------------------------------------------------
    'license': 'OPL-1',
    'depends': [
        'hr_attendance',
    ],
    'data': [
        'views/hr_work_location_views.xml',
        'views/hr_employee_views.xml',
        'views/hr_attendance_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'geofence_attendance/static/src/components/geofence_map.scss',
            'geofence_attendance/static/src/components/geofence_map.js',
            'geofence_attendance/static/src/components/geofence_map.xml',
        ],
    },
    'images': [
        'static/description/banner.png',
    ],
    'price': 99.00,
    'currency': 'USD',
    'installable': True,
    'application': False,
    'auto_install': False,
}
