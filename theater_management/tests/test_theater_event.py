import datetime

from .common import TestTheaterManagementCommon


class TestTheaterEvent(TestTheaterManagementCommon):

    def test_01_onchange_rehearsal_prefix(self):
        """Check adding prefix [REH] for rehealsals."""
        event_name = "Hamlet Performance"
        event = self.env['event.event'].new({
            'name': event_name,
            'event_type_selection': 'show',
            'date_begin': datetime.datetime.now(),
            'date_end': datetime.datetime.now(),
        })

        event.event_type_selection = 'rehearsal'
        event._onchange_event_name_prefix()

        expected_name = f"[REH] {event_name}"
        self.assertEqual(event.name, expected_name, "Prefix [REH] should be added for a rehealsal.")

        event._onchange_event_name_prefix()
        self.assertEqual(event.name, expected_name, "Prefix should not be duplicated.")