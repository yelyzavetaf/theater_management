==========================
Theater Management System
==========================

This module provides a comprehensive solution for managing theater activities,
including performances, rehearsals, artistic troupe assignments, and automated
participation reporting.

Features
========

* **Event Management:** Separate workflows for *Shows* and *Rehearsals*.
* **Venue Control:** Track venue availability and prevent scheduling conflicts.
* **Troupe Management:**
    * Manage **Artists** (Actors, Dancers, Soloists etc.).
    * Manage **Orchestra Musicians** and their instruments.
* **Automated Website Integration:**
    * Dynamic HTML descriptions generated from cast/orchestra lists.
    * Automatic cover image processing for event banners.
* **Scheduling Wizard:** Create multiple event occurrences in a single click with conflict detection.
* **Professional Reporting:**
    * PDF Participation Reports for musicians with automatic hour calculation.


Installation
============
To install this module, you need to:

#. Clone repository.
#. Add the repository path to the config file.
#. Update the app list.
#. Install the module.

Configuration
=============

To ensure PDF reports display images and styles correctly:
1. Go to **Settings > Technical > System Parameters**.
2. Set ``report.url`` to your instance URL (e.g., ``http://127.0.0.1:8069``).

Usage
=====

1. **Create an Instrument:** Go to Theater > Planning > Musical Instruments.
2. **Add a Musician:** Go to Theater > Staff > Musicians and link them to an instrument.
3. **Schedule a Show:** Create a new Event, select "Show", and add the Cast and Orchestra.
4. **Print Reports:** From the Musicians list, select records and use the **Print** menu to generate Participation Reports.

Technical Requirements
======================

* **Odoo Version:** 19.0 (Community/Enterprise)
* **Dependencies:** ``event``, ``website_event``, ``website``
* **External Library:** ``wkhtmltopdf`` (version 0.12.6.1 (with patched qt))

Credits
=======

Authors
-------
* Lisa <lisa.email@example.com>

Maintainer
----------
* This module is maintained by the Theater IT Department.