from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class HrWorkLocation(models.Model):
    _inherit = 'hr.work.location'

    use_geofence = fields.Boolean(
        string='Enable Geofence',
        default=False,
        help="When enabled, employees assigned to this work location are only "
             "allowed to check in or out from within the specified geographic area.",
    )
    geofence_latitude = fields.Float(
        string='Latitude',
        digits=(10, 7),
        help="Latitude of the work location center, in decimal degrees.",
    )
    geofence_longitude = fields.Float(
        string='Longitude',
        digits=(10, 7),
        help="Longitude of the work location center, in decimal degrees.",
    )
    geofence_radius = fields.Float(
        string='Allowed Radius (meters)',
        default=100.0,
        help="Maximum allowed distance, in meters, between the employee and "
             "the work location center.",
    )
    geofence_input_mode = fields.Selection(
        selection=[
            ('manual', 'Enter Coordinates Manually'),
            ('map', 'Pick from Map'),
        ],
        string='Coordinates Input',
        default='manual',
        help="Choose how to set the geofence center: enter coordinates by "
             "hand, or pick a point on the interactive map.",
    )

    @api.constrains(
        'use_geofence',
        'geofence_latitude',
        'geofence_longitude',
        'geofence_radius',
    )
    def _check_geofence_values(self):
        for record in self:
            if not record.use_geofence:
                continue
            if not -90.0 <= record.geofence_latitude <= 90.0:
                raise ValidationError(_("Latitude must be between -90 and 90."))
            if not -180.0 <= record.geofence_longitude <= 180.0:
                raise ValidationError(_("Longitude must be between -180 and 180."))
            if record.geofence_radius <= 0:
                raise ValidationError(_("Allowed radius must be greater than zero."))
