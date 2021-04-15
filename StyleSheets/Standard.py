"""
This Pyside6 (Qt) CSS Stylesheet is intended to provide consistent and reusable formatting. To minimize potential errors.

Colors:
1) #BEDF7C -- 190, 223, 124
2) #8BA78C -- 139, 167, 140
3) #414E41 -- 65, 78, 65
4) #FAFAFA -- 250, 250, 250
5) #A3A3A3 -- 163, 163, 163

"""

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

QComboBox{
    background-color: #414E41;
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
    border: 1px solid #8BA78C;
    selection-background-color: #A3A3A3;
    selection-color: black;
}

QComboBox:selection{
    background: white;
}

QDateEdit{
    border: 1px solid #414E41;
    background-color: #414E41;
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

QTabWidget::pane { /* The tab widget frame */
    border-top: 2px solid #414E41;
}

QTabWidget::tab-bar {
    left: 5px; /* move to the right by 5px */
}

/* Style the tab using the tab sub-control. Note that
    it reads QTabBar _not_ QTabWidget */
QTabBar::tab {
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                stop: 0 #E1E1E1, stop: 0.4 #DDDDDD,
                                stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3);
    border: 2px solid #414E41;
    border-bottom-color: #FAFAFA; /* same as the pane color */
    border-top-left-radius: 2px;
    border-top-right-radius: 2px;
    min-width: 8px;
    padding: 2px;
    font-size: 10px;
    color: #414E41;
    font-weight: bold;
}

QTabBar::tab:selected, QTabBar::tab:hover {
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                stop: 0 #fafafa, stop: 0.4 #f4f4f4,
                                stop: 0.5 #e7e7e7, stop: 1.0 #fafafa);
}

QTabBar::tab:selected {
    border-color: #414E41;
    border-bottom-color: #FAFAFA; /* same as pane color */
}

QTabBar::tab:!selected {
    margin-top: 2px; /* make non-selected tabs look smaller */   
} 


"""

loginTitleFrame = """
QFrame#r2frame{
    border: 2px solid #A3A3A3;
    border-top: 5px solid #BEDF7C;
    border-bottom: 5px solid #BEDF7C;
    border-radius: 5px;
    background-color: #8BA78C;
}

QLabel#labelTitle{
    font-style: bold;
}

QLabel#labelSubTitle{
    font-style: italic;
}
"""

welcomeMesgFrame = """
QFrame#scrollFrame{
    border-top: 3px solid #BEDF7C;
    border-bottom: 3px solid #BEDF7C;
    border-radius: 5px;
    background-color: #414E41;
}

QScrollArea#messageScroll{
    background-color: #414E41;
}
"""

mainWindow = """
QMainWindow{
    background-color: #FAFAFA;
}

QLabel#labelStaticTA{
    border-top: 3px solid #414E41;
    border-bottom: 3px solid #414E41;
    border-radius: 15px;
    background-color: #8BA78C;
    padding-right: -1px;
    margin-right: -1px;
    margin-left: 50px;
}

QLabel#labelTAssests{
    border-top: 3px solid #414E41;
    border-bottom: 3px solid #414E41;
    border-radius: 15px;
    background-color: rgba(163, 163, 163, 0.4);
    padding-left: -1px;
    margin-left: -1px;
    margin-right: 50px;
}

QLabel#labelStaticTL{
    border-top: 3px solid #B41627;
    border-bottom: 3px solid #B41627;
    border-radius: 15px;
    background-color: #8BA78C;
    padding-right: 0px;
    margin-right: 0px;
    margin-left: 50px;
}

QLabel#labelTLiabilities{
    border-top: 3px solid #B41627;
    border-bottom: 3px solid #B41627;
    border-radius: 15px;
    background-color: rgba(163, 163, 163, 0.4);
    padding-left: -1px;
    margin-left: -1px;
    margin-right: 50px;
}

QLabel#labelStaticTN{
    border-top: 3px solid #414E41;
    border-bottom: 3px solid #414E41;
    border-radius: 15px;
    background-color: #8BA78C;
    padding-right: 0px;
    margin-right: 0px;
    margin-left: 50px;
}

QLabel#labelNW{
    border-top: 3px solid #414E41;
    border-bottom: 3px solid #414E41;
    border-radius: 15px;
    background-color: #BEDF7C;
    padding-left: 0px;
    margin-left: 0px;
    margin-right: 50px;
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

backgroundColor = """
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

generalError = """
QLineEdit{
    border: 3px solid #B41627;
    border-radius: 2px;
}

QLabel{
    color: #B41627;
}
"""


if __name__ == "__main__":
    print("error")
