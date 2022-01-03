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

overTime = """
QLabel#lGraphTitle{
    border-top: 3px solid #BEDF7C;
    border-bottom: 3px solid #BEDF7C;
    border-radius: 5px;
    background-color: #8BA78C;
    padding-bottom: 10px;
    padding-top: 10px;
}

QLabel#lLengend{
    border-top: 3px solid #BEDF7C;
    border-bottom: 3px solid #8BA78C;
    border-radius: 5px;
    background-color: #FAFAFA;
}

QLabel#lHeighlights{
    border-top: 3px solid #BEDF7C;
    border-bottom: 3px solid #8BA78C;
    border-radius: 5px;
    background-color: #FAFAFA;
}

QLabel#lLowPoints{
    border-top: 3px solid #BEDF7C;
    border-bottom: 3px solid #8BA78C;
    border-radius: 5px;
    background-color: #FAFAFA;
}
"""

if __name__ == "__main__":
    import os
    import sys
    sys.tracebacklimit = 0
    raise RuntimeError(f"Check your Executable File.\n{os.path.basename(__file__)} is not intended as independent script")
