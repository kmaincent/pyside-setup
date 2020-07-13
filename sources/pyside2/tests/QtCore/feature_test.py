#############################################################################
##
## Copyright (C) 2020 The Qt Company Ltd.
## Contact: https://www.qt.io/licensing/
##
## This file is part of Qt for Python.
##
## $QT_BEGIN_LICENSE:LGPL$
## Commercial License Usage
## Licensees holding valid commercial Qt licenses may use this file in
## accordance with the commercial license agreement provided with the
## Software or, alternatively, in accordance with the terms contained in
## a written agreement between you and The Qt Company. For licensing terms
## and conditions see https://www.qt.io/terms-conditions. For further
## information use the contact form at https://www.qt.io/contact-us.
##
## GNU Lesser General Public License Usage
## Alternatively, this file may be used under the terms of the GNU Lesser
## General Public License version 3 as published by the Free Software
## Foundation and appearing in the file LICENSE.LGPL3 included in the
## packaging of this file. Please review the following information to
## ensure the GNU Lesser General Public License version 3 requirements
## will be met: https://www.gnu.org/licenses/lgpl-3.0.html.
##
## GNU General Public License Usage
## Alternatively, this file may be used under the terms of the GNU
## General Public License version 2.0 or (at your option) the GNU General
## Public license version 3 or any later version approved by the KDE Free
## Qt Foundation. The licenses are as published by the Free Software
## Foundation and appearing in the file LICENSE.GPL2 and LICENSE.GPL3
## included in the packaging of this file. Please review the following
## information to ensure the GNU General Public License requirements will
## be met: https://www.gnu.org/licenses/gpl-2.0.html and
## https://www.gnu.org/licenses/gpl-3.0.html.
##
## $QT_END_LICENSE$
##
#############################################################################

import os
import sys
import unittest

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from init_paths import init_test_paths
init_test_paths(False)

from PySide2 import QtCore
from PySide2.support.__feature__ import _really_all_feature_names
from textwrap import dedent

"""
feature_test.py
--------------

This tests the selectable features in PySide.

There are no real features implemented. They will be added, later.
"""

class FeaturesTest(unittest.TestCase):

    def testAllFeatureCombinations(self):
        """
        Test for all 256 possible combinations of `__feature__` imports.
        """
        global __name__

        for bit in range(8):
            # We are cheating here, since the functions are in the globals.
            exec(dedent("""

        def tst_bit{0}(flag, self):
            if flag == 0:
                with self.assertRaises(AttributeError):
                    QtCore.QCborArray.fake_feature_{1:02x}
                with self.assertRaises(KeyError):
                    QtCore.QCborArray.__dict__["fake_feature_{1:02x}"]
            else:
                QtCore.QCborArray.fake_feature_{1:02x}
                QtCore.QCborArray.__dict__["fake_feature_{1:02x}"]

                        """.format(bit, 1 << bit)), globals(), globals())
        feature_list = _really_all_feature_names
        func_list = [tst_bit0, tst_bit1, tst_bit2, tst_bit3,
                     tst_bit4, tst_bit5, tst_bit6, tst_bit7]

        for idx in range(0x100):
            __name__ = "feature_{:02x}".format(idx)
            print()
            print("--- Feature Test Module `{}` ---".format(__name__))
            print("Imports:")
            for bit in range(8):
                if idx & 1 << bit:
                    feature = feature_list[bit]
                    text = "from __feature__ import {}".format(feature)
                    print(text)
                    exec(text)
            for bit in range(8):
                value = idx & 1 << bit
                func_list[bit](value, self=self)


if __name__ == '__main__':
    unittest.main()
