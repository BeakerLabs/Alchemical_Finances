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

transFrame = """
QFrame#lInputFrame{
    border-top: 3px solid #BEDF7C;
    border-top-left-radius: 45px;
    border-bottom: 3px solid #8BA78C;
    background: rgba(163, 163, 163, 0.3);
    margin-right: -1px;
}

QFrame#rInputFrame{
    border-top: 3px solid #BEDF7C;
    border-bottom: 3px solid #8BA78C;
    border-bottom-right-radius: 45px;
    background: rgba(163, 163, 163, 0.3);
    margin-left: -1px;
}

QFrame#leftFrame{
    border-top: 3px solid #BEDF7C;
    border-bottom: 3px solid #8BA78C;
    border-radius: 5px;
    background-color: #FAFAFA;
}

QFrame#centerFrame{
    border-top: 3px solid #BEDF7C;
    border-bottom: 3px solid #8BA78C;
    border-radius: 5px;
    background-color: #FAFAFA;
}

QFrame#rightFrame{
    border-top: 3px solid #BEDF7C;
    border-bottom: 3px solid #8BA78C;
    border-radius: 5px;
    background-color: #FAFAFA;
}

"""

spendingLabel = """
QLabel{
    border-top: 3px solid #BEDF7C;
    border-bottom: 3px solid #8BA78C;
    border-radius: 5px;
    background-color: #FAFAFA;
    padding-top: 10px;
    padding-bottom: 10px;
    margin-bottom: 10px;
    box-shadow: -5px -5px #777777;
}
"""


if __name__ == "__main__":
    print("error")
