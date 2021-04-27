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
#  www.BeakerLabs.com

profileFrame = """
QFrame#profileFrame{
    border-top: 3px solid #BEDF7C;
    border-bottom: 3px solid #8BA78C;
    border-top-left-radius: 45px;
    border-bottom-right-radius: 45px;
    background-color: rgba(163, 163, 163, 0.2);
}
"""