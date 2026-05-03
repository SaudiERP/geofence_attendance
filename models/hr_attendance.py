from odoo import fields, models


class HrAttendance(models.Model):
    _inherit = 'hr.attendance'

    geofence_work_location_id = fields.Many2one(
        comodel_name='hr.work.location',
        string='Geofence Work Location',
        compute='_compute_geofence_work_location',
        store=True,
        readonly=True,
        help="Work location whose geofence rules applied at the time of check-in.",
    )

    def _compute_geofence_work_location(self):
        for record in self:
            location = record.employee_id.work_location_id
            if location and location.use_geofence:
                record.geofence_work_location_id = location
            else:
                record.geofence_work_location_id = False
