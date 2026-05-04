import logging
import math

from odoo import _, api, fields, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

EARTH_RADIUS_METERS = 6371000.0

# Map Python's weekday() return value (Mon=0..Sun=6) to the Odoo
# per-day work location field on hr.employee.
_WEEKDAY_TO_FIELD = {
    0: 'monday_location_id',
    1: 'tuesday_location_id',
    2: 'wednesday_location_id',
    3: 'thursday_location_id',
    4: 'friday_location_id',
    5: 'saturday_location_id',
    6: 'sunday_location_id',
}


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    work_location_use_geofence = fields.Boolean(
        related='work_location_id.use_geofence',
        string='Geofence Enabled',
        readonly=True,
    )
    work_location_latitude = fields.Float(
        related='work_location_id.geofence_latitude',
        string='Location Latitude',
        readonly=True,
        digits=(10, 7),
    )
    work_location_longitude = fields.Float(
        related='work_location_id.geofence_longitude',
        string='Location Longitude',
        readonly=True,
        digits=(10, 7),
    )
    work_location_radius = fields.Float(
        related='work_location_id.geofence_radius',
        string='Allowed Radius (m)',
        readonly=True,
    )

    geofence_active_location_id = fields.Many2one(
        comodel_name='hr.work.location',
        string='Active Geofence Today',
        compute='_compute_geofence_active_location',
        readonly=True,
        help="The work location whose geofence rules will apply if the "
             "employee tries to check in or out right now. Resolved from "
             "today's per-day location, falling back to the default work "
             "location.",
    )

    @api.depends(
        'work_location_id',
        'monday_location_id',
        'tuesday_location_id',
        'wednesday_location_id',
        'thursday_location_id',
        'friday_location_id',
        'saturday_location_id',
        'sunday_location_id',
    )
    def _compute_geofence_active_location(self):
        for employee in self:
            employee.geofence_active_location_id = employee._resolve_geofence_location()

    def _resolve_geofence_location(self):
        """Return the work location whose geofence applies to this employee.

        Priority:
            1. The employee's per-day location for today, if set.
            2. The employee's default ``work_location_id``, otherwise.
            3. ``False`` if neither is set.
        """
        self.ensure_one()
        weekday = fields.Date.context_today(self).weekday()
        day_field = _WEEKDAY_TO_FIELD.get(weekday)
        day_location = self[day_field] if day_field else False
        return day_location or self.work_location_id or False

    @staticmethod
    def _haversine_distance(lat1, lon1, lat2, lon2):
        """Return the great-circle distance, in meters, between two points
        given in decimal degrees.
        """
        phi1 = math.radians(lat1)
        phi2 = math.radians(lat2)
        delta_phi = math.radians(lat2 - lat1)
        delta_lambda = math.radians(lon2 - lon1)
        a = (
            math.sin(delta_phi / 2.0) ** 2
            + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2.0) ** 2
        )
        return EARTH_RADIUS_METERS * 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))

    def _check_geofence(self, geo_information):
        """Validate that the employee's GPS position lies within the radius
        of the resolved work location for today.
        """
        self.ensure_one()
        work_location = self._resolve_geofence_location()
        if not work_location or not work_location.use_geofence:
            return

        latitude = geo_information.get('latitude') if geo_information else None
        longitude = geo_information.get('longitude') if geo_information else None

        if (latitude is None or latitude is False
                or longitude is None or longitude is False):
            raise UserError(_(
                "Location access is required to register attendance. "
                "Please enable location services in your browser and try again."
            ))

        try:
            user_lat = float(latitude)
            user_lon = float(longitude)
        except (TypeError, ValueError):
            raise UserError(_("Invalid location data received from the device."))

        distance = self._haversine_distance(
            user_lat,
            user_lon,
            work_location.geofence_latitude,
            work_location.geofence_longitude,
        )

        if distance > work_location.geofence_radius:
            raise UserError(_(
                "You are outside the allowed attendance area for '%(loc)s'.\n"
                "Your distance: %(dist).0f m\n"
                "Allowed radius: %(rad).0f m",
                loc=work_location.name,
                dist=distance,
                rad=work_location.geofence_radius,
            ))

        _logger.info(
            "Geofence check passed for employee %s at %s: %.1f m (radius %.0f m).",
            self.name,
            work_location.name,
            distance,
            work_location.geofence_radius,
        )

    def _attendance_action_change(self, geo_information=None):
        for employee in self:
            employee._check_geofence(geo_information or {})
        return super()._attendance_action_change(geo_information=geo_information)
