# Copyright Least Authority Enterprises.
# See LICENSE for details.

"""
Automation (isn't all software?) relating to the S4 service.
"""

# Do some hot-fixing here so that nothing in lae_automation has a chance to
# run without the fixes.

from .txaws_47 import patch
patch()

from .txaws_50 import patch
patch()

del patch
