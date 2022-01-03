"""
This Pyside6 (Qt) CSS Stylesheet is intended to provide consistent and reusable formatting. To minimize potential errors.

Colors:
1) #BEDF7C -- 190, 223, 124
2) #8BA78C -- 139, 167, 140
3) #414E41 -- 65, 78, 65
4) #FAFAFA -- 250, 250, 250
5) #A3A3A3 -- 163, 163, 163
6) #B41627 -- 180, 22, 39
"""

#  Copyright (c) 2021 Beaker Labs LLC.
#  This software the GNU LGPLv3.0 License
#  www.BeakerLabsTech.com
#  contact@beakerlabstech.com

welcomeMesgFrame = """
QFrame#scrollFrame{
    border-top: 3px solid #BEDF7C;
    border-bottom: 3px solid #BEDF7C;
    border-radius: 3px;
    background-color: #414E41;
}

QScrollArea#messageScroll{
    background-color: #414E41;
}
"""


if __name__ == "__main__":
    import os
    import sys
    sys.tracebacklimit = 0
    raise RuntimeError(f"Check your Executable File.\n{os.path.basename(__file__)} is not intended as independent script")
