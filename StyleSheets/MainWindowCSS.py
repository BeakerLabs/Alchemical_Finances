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

mainWindow = """

QMainWindow{
    background-color: #FAFAFA;
}

QLabel#labelStaticTA{
    border-top: 3px solid #414E41;
    border-bottom: 3px solid #414E41;
    border-top-left-radius: 15px;
    border-bottom-left-radius: 15px;
    background-color: #8BA78C;
    margin-left: 20px;
}

QLabel#labelTAssests{
    border-top: 3px solid #414E41;
    border-bottom: 3px solid #414E41;
    border-top-right-radius: 15px;
    border-bottom-right-radius: 15px;
    background-color: rgba(163, 163, 163, 0.4);
    margin-right: 20px;
    color: #696969;
}

QLabel#labelStaticTL{
    border-top: 3px solid #B41627;
    border-bottom: 3px solid #B41627;
    border-top-left-radius: 15px;
    border-bottom-left-radius: 15px;
    background-color: #8BA78C;
    margin-left: 20px;
}

QLabel#labelTLiabilities{
    border-top: 3px solid #B41627;
    border-bottom: 3px solid #B41627;
    border-top-right-radius: 15px;
    border-bottom-right-radius: 15px;
    background-color: rgba(163, 163, 163, 0.4);
    margin-right: 20px;
    color: #696969;
}

QLabel#labelStaticTN{
    border-top: 3px solid #414E41;
    border-bottom: 3px solid #414E41;
    border-top-left-radius: 15px;
    border-bottom-left-radius: 15px;
    background-color: #8BA78C;
    margin-left: 20px;
}

QLabel#labelNW{
    border-top: 3px solid #414E41;
    border-bottom: 3px solid #414E41;
    border-top-right-radius: 15px;
    border-bottom-right-radius: 15px;
    background-color: #BEDF7C;
    margin-right: 20px;
}

QPushButton{
    border: 1px solid #414E41;
    background-color: #A3A3A3;
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

QScrollBar:vertical{
    background: #D3D3D3;
    width: 15px;
    margin: 22px 0 20px 0;
}

QScrollBar::handle:vertical {
    background: #414E41;
    min-height: 20px;
}

QScrollBar::add-line:vertical{
    background: #FAFAFA;
    height: 20px;
    subcontrol-position: bottom;
    subcontrol-origin: margin;
}

QScrollBar::sub-line:vertical{
    background: #FAFAFA;
    height: 20px;
    subcontrol-position: top;
    subcontrol-origin: margin;
}

QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical{
    width: 5px;
    height: 5px;
    background: #BEDF7C;
}

QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical{
    background: none;
}

QScrollBar:horizontal {
    background: #D3D3D3;
    height: 15px;
    margin: 0px 20px 0px 20px;
}

QScrollBar::handle:horizontal {
    background: #414E41;
    min-width: 20px;
}

QScrollBar::add-line:horizontal {
    background: #FAFAFA;
    width: 20px;
    subcontrol-position: right;
    subcontrol-origin: margin;
}

QScrollBar::sub-line:horizontal {
    background: #FAFAFA;
    width: 20px;
    subcontrol-position: left;
    subcontrol-origin: margin;
}

QScrollBar::left-arrow:horizontal, QScrollBar::right-arrow:horizontal {
    width: 5px;
    height: 5px;
    background: #BEDF7C;
}

QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
    background: none;
}

QTabWidget::pane { /* The tab widget frame */
    border-top: 2px solid #414E41;
}

QTabWidget::tab-bar {
    left: 5px; /* move to the right by 5px */
}

/* Style the tab using the tab sub-control. Note that it reads QTabBar _not_ QTabWidget */
QTabBar::tab {
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                stop: 0 #E1E1E1, stop: 0.4 #DDDDDD,
                                stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3);
    border: 2px solid #414E41;
    border-bottom-color: #FAFAFA; /* same as the pane color */
    border-top-left-radius: 2px;
    border-top-right-radius: 2px;
    min-width: 90px;
    padding: 4px;
    font-size: 14px;
    color: #000000;
    font-weight: bold;
}

QTabBar::tab:selected {
    border-color: #414E41;
    background-color:  #8BA78C;
    border-bottom-color: #BEDF7C; 
}

QTabBar::tab:!selected {
    margin-top: 2px; /* make non-selected tabs look smaller */   
} 

QTabBar::tab:hover {
    background: qlineargradient(x1: 0, y1: 0, x2: 0 y2: 1,
                                stop: 0 #BEDF7C, stop: 0.4 #B4D969,
                                stop: 0.5 #AFD06D, stop: 0.1 #B8D774);
}

QTabBar::tab:disabled {
    border-color: #414E41;
    background-color:  #FAFAFA;
    border-bottom-color: #FAFAFA; 
}

QMenuBar {
    background-color: #FAFAFA;
    spacing: 5px;
    color: #000000;
}

QMenuBar:item:selected {
    background: #8BA78C;
}

QMenuBar:item:pressed {
    background: #BEDF7C;
}

QMenu {
    background-color: #FAFAFA;
    spacing: 5px;
    color: #000000;
}

QMenu:item:selected {
    background: #8BA78C;
}

QMenu:item:pressed {
    background: #BEDF7C;
}
"""

if __name__ == "__main__":
    import os
    import sys
    sys.tracebacklimit = 0
    raise RuntimeError(f"Check your Executable File.\n{os.path.basename(__file__)} is not intended as independent script")
