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

summarySTD = """
QWidget{
    background-color: #FAFAFA;
}

QDialog{
    background-color: rgba(163, 163, 163, 0.2);
}

QScrollBar:vertical {
    background: #D3D3D3;
    width: 15px;
    margin: 22px 0 20px 0;
}
QScrollBar::handle:vertical {
    background: #414E41;
    min-height: 20px;
}

QScrollBar::add-line:vertical {
    background: #FAFAFA;
    height: 20px;
    subcontrol-position: bottom;
    subcontrol-origin: margin;
}

QScrollBar::sub-line:vertical {
    background: #FAFAFA;
    height: 20px;
    subcontrol-position: top;
    subcontrol-origin: margin;
}

QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {
    width: 5px;
    height: 5px;
    background: #BEDF7C;
}

QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
    background: none;
}

QFrame{
    background-color: #FAFAFA;
    border: 0px;
}

QProgressBar{
    border: 2px solid #A3A3A3;
    border-radius: 5px;
    height: 5px;
    text-align: center;
    color: black;
    font-size: 14px;
    font-weight: bold;

}

QProgressBar::chunk {
    background-color: rgba(190, 223, 124, 0.75);
    border-radius: 1px;
    width: 5 px;
    margin: 1px;
}
"""

parentFormat = """
QLabel{
    border-top: 3px solid #BEDF7C;
    border-bottom: 3px solid #8BA78C;
    border-radius: 5px;
    background-color: #FAFAFA;
}
"""

columnHeader = """
QLabel{
    border-top: 3px solid #BEDF7C;
    border-bottom: 3px solid #BEDF7C;
    border-radius: 5px;
    background-color: #8BA78C;
}
"""

accountDetails = """
QLabel{
    border-bottom: 1px solid #000000;
    border-right: 1px solid #A3A3A3;
    border-bottom-right-radius: 10px;
    Margin: 5px;
    padding-left: 5px;
    padding-right: 10px;
    background-color: rgba(163, 163, 163, 0.2);
}"""

subtotalBalanceFormat = """
QLabel{
    border-top: 1px solid #414E41;
    border-bottom: 1px solid #414E41;
    border-bottom-right-radius: 15px 15px;
    border-top-left-radius: 15px 15px;
    Margin: 5px;
    padding-right: 10px;
    background-color: #BEDF7C;
}
"""

messageFormat = """
QLabel{
    border-top: 3px solid #B41627;
    border-bottom: 3px solid #B41627;
    border-radius: 5px;
    background-color: #FAFAFA;
    color: #B41627;
}"""


if __name__ == "__main__":
    print("error")
