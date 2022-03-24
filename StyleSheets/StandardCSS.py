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

standardAppearance = """
QDialog{
    background-color: #FAFAFA;
}

QLineEdit{
    border: 1px solid #414E41;
    border-radius: 8px;
}

QLineEdit:Disabled{
    border: 1px solid #748b75;
    background-color: rgba(163, 163, 163, 0.4);
}

QListWidget{
    border: 1px solid #414E41;
    border-radius: 2px;
}

QTextEdit{
    border: 1px solid #414E41;
    border-radius: 2px;
}

QPushButton{
    border: 1px solid #414E41;
    background: qlineargradient(x1: 0, y1: 0, x2: 0 y2: 1,
                                stop: 0 #A3A3A3, stop: 0.4 #999999,
                                stop: 0.5 #9E9E9E, stop: 0.1 #ADADAD);
    border-radius: 2px;
    font-weight: bold;
    padding: 2px;
    padding-right: 15px;
    padding-left: 15px;
}

QPushButton:pressed{
    border: 2px solid #414E41;
    background-color: #BEDF7C;
    border-radius: 2px;
    padding: 2px;
    padding-right: 15px;
    padding-left: 15px;
}

QPushButton:hover{
    border: 2px solid #414E41;
    background-color: #BEDF7C;
    background: qlineargradient(x1: 0, y1: 0, x2: 0 y2: 1,
                            stop: 0 #BEDF7C, stop: 0.4 #B4D969,
                            stop: 0.5 #AFD06D, stop: 0.1 #B8D774);
    padding: 2px;
    padding-right: 15px;
    padding-left: 15px;
}

QPushButton:disabled{
    border: 1px solid #414E41;
    background-color: #FAFAFA;
    border-radius: 2px;
    padding: 2px;
    padding-right: 15px;
    padding-left: 15px;
}

QComboBox{
    background-color: rgba(65, 78, 65, 0.75);
    color: white;
}

QComboBox:hover{
    background-color: #BEDF7C;
}

QComboBox:disabled{
    background-color: #FAFAFA;
    color: #A3A3A3;
}

QComboBox QAbstractItemView{
    selection-background-color: #A3A3A3;
    selection-color: black;
}

QComboBox:selection{
    background: white;
}

QDateEdit{
    border: 1px solid #414E41;
    background-color: rgba(65, 78, 65, 0.75);
    color: white;
}

QDateEdit:hover{
    background-color: #BEDF7C;
}

QDateEdit QAbstractItemView{
    border: 1px solid #414E41;
    selection-background-color: #A3A3A3;
    selection-color: black;
}

QDateEdit:disabled{
    background-color: #FAFAFA;
    color: #A3A3A3;
}

QInputDialog{
    background-color: #FAFAFA;
}

QSpinBox{
   height: 25px;
}

QSpinBox::QAbstractItemVIew {
    font-size: 10px;
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

QTableView {
    font-size: 16px;
}
"""

if __name__ == "__main__":
    import os
    import sys
    sys.tracebacklimit = 0
    raise RuntimeError(f"Check your Executable File.\n{os.path.basename(__file__)} is not intended as independent script")
