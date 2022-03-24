#  Copyright (c) 2021 Beaker Labs LLC.
#  This software the GNU LGPLv3.0 License
#  www.BeakerLabsTech.com
#  contact@beakerlabstech.com

import os
import sys

from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle

from Toolbox.Formatting_Tools import cash_format, remove_space, decimal_places
from Toolbox.SQL_Tools import obtain_sql_list, obtain_sql_value


class Generate_user_report:

    def __init__(self, request, error_log):
        super().__init__()

        # Program Error Logger
        self.error_Logger = error_log

        # ---- Program --------------------------------------------------------------------------------------------------------------------------------------------------------
        # request = [Database, User Name, Report Content list, destination directory]
        report_date = datetime.now().strftime('%Y%m%d%M')
        report_date_visual = datetime.now().strftime('%B %d, %Y; %H:%M')
        copyright_year = datetime.now().strftime('%Y')
        filename = "{0} - {1} - Report.pdf".format(report_date, request[1])
        save_name = os.path.join(request[3], filename)
        # save_name = os.path.join(os.path.expanduser("~"), "Desktop/", filename)  # "OneDrive\Desktop/"
        author = request[1]
        title = "User Generated Report"
        subtitle = f"Generated by Alchemical Finances -- a Beaker Labs LLC product (c) {copyright_year}"

        pdf = canvas.Canvas(save_name, pagesize=letter, bottomup=1)
        width, height = letter
        pdf.setTitle(filename)
        pdf.setAuthor(author)
        pdf.setFillColorRGB(0, 0, 0)

        # def documentRuler(pdf):
        #     pdf.drawString(100, 25, 'x100')
        #     pdf.drawString(200, 25, 'x200')
        #     pdf.drawString(300, 25, 'x300')
        #     pdf.drawString(400, 25, 'x400')
        #     pdf.drawString(500, 25, 'x500')
        #     pdf.drawString(550, 25, 'x550')
        #     pdf.drawString(600, 25, 'x600')
        #
        #     pdf.drawString(10, 25, 'y10/x25')
        #     pdf.drawString(10, 100, 'y100')
        #     pdf.drawString(10, 200, 'y200')
        #     pdf.drawString(10, 300, 'y300')
        #     pdf.drawString(10, 400, 'y400')
        #     pdf.drawString(10, 500, 'y500')
        #     pdf.drawString(10, 600, 'y600')
        #     pdf.drawString(10, 700, 'y700')
        #     pdf.drawString(10, 750, 'y750')
        #     pdf.drawString(10, 780, 'y800')

        # documentRuler(pdf)
        # Part 0 - Logo Import
        logo = os.path.join(os.getcwd(), 'Resources/AF Logo.jpg')  # Add , '../', when testing BuildReports.py directly
        pdf.drawImage(logo, 50, 645, width=75, height=75)

        # Part 1 - Report Title
        pdf.setFillColorRGB(0, 0, 0)
        pdf.setFont('Times-Bold', 24)
        pdf.drawString(140, 685, title)

        # Part 2 - Report Subtitle w/ separation line
        pdf.setFont('Times-Roman', 8)
        pdf.drawString(140, 673, subtitle)

        # Part 3 - Report Date
        pdf.setFont('Times-Roman', 16)
        pdf.drawString(140, 645, report_date_visual)
        pdf.line(50, 640, 550, 640)

        # Part 4 - Net Worth Table
        pdf.setFont('Times-Bold', 16)
        table_title = "User Account Snapshot*"
        pdf.drawCentredString(300, 618, table_title)
        # net_worth = [1] Net w/o comma [2] Net w/ Comma [3] Assets w/ comma [4] liabilities w/comma
        snapshot = self.generate_snapshot(request)
        snapshot_data = [['Gross', 'Liabilities', 'Net Worth'],
                         [snapshot[0], snapshot[1], snapshot[2]]]

        elements = []

        net_worth_table = Table(snapshot_data, colWidths=125, rowHeights=25,)
        elements.append(net_worth_table)
        # (Column, Row) --- (0, 0) = TOP Left (-1, -1) = Bottom Right
        net_worth_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BACKGROUND', (0, 0), (-1, 0), colors.green),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('LINEBELOW', (0, 0), (-1, 0), 0.25, colors.black),
            ('LINEBELOW', (0, -1), (-1, -1), 0.25, colors.black),
            ('LINEBEFORE', (0, 0), (0, -1), 0.25, colors.black),
            ('LINEAFTER', (-1, 0), (-1, -1), 0.25, colors.black),
            ('FONTNAME', (0, 0), (-1, 0), 'Times-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('FONTNAME', (0, -1), (-1, -1), 'Times-Roman'),
            ('FONTSIZE', (0, -1), (-1, -1), 11),
        ]))
        net_worth_table.wrapOn(pdf, width, height)
        net_worth_table.drawOn(pdf, 113, 566,)
        pdf.line(50, 555, 550, 555)

        data_note = "* Snapshot represents the user's requested summary information. Report may not include all available information."
        pdf.setFont('Times-Roman', 8)
        pdf.drawString(50, 25, data_note)

        # Part 5 -  Page 1 Summary Report Table
        report_construction = self.summary_report_table(request)
        #  report_construction == [table data, table header rows, row counts, table style]

        qty_tables = len(report_construction[0])
        columnWidths = [200, 125, 125]
        page = 1

        for num in range(0, qty_tables):

            pdf.setFont('Times-Roman', 8)
            pdf.drawString(525, 25, "page {0} of {1}".format(page, qty_tables))

            # determines the starting point for the tables by page and table length
            if report_construction[2][0] < 26:
                starting_point = ((26 - report_construction[2][0]) * 18) + 75
            elif num > 0 and report_construction[2][num] < 29:
                starting_point = ((29 - report_construction[2][num]) * 18) + 75
            else:
                starting_point = 75

            if num > 0:
                # Part 0 - Logo Import
                pdf.drawImage(logo, 50, 645, width=75, height=75)

                # Part 1 - Report Title
                pdf.setFillColorRGB(0, 0, 0)
                pdf.setFont('Times-Bold', 24)
                pdf.drawString(140, 685, title)

                # Part 2 - Report Subtitle w/ separation line
                pdf.setFont('Times-Roman', 8)
                pdf.drawString(140, 673, subtitle)

                # Part 3 - Report Date
                pdf.setFont('Times-Roman', 16)
                pdf.drawString(140, 645, report_date_visual)
                pdf.line(50, 640, 550, 640)

            table = Table(report_construction[0][num], colWidths=columnWidths, rowHeights=18,)
            elements.append(table)
            table.setStyle((TableStyle(report_construction[3][num])))
            table.wrapOn(pdf, width, height)
            table.drawOn(pdf, 75, starting_point)
            pdf.showPage()
            page += 1

        pdf.save()
        os.startfile(save_name)

    def summary_report_table(self, request):
        parenttype_list = request[2]  # Used to determine what parent types to include in the list.
        acc_statement_list = []  # List of Sqlite3 statements to acquire a list of accounts by parent type.
        st_statement_list = []  # List of Sqlite3 statements to acquire subtotals for each parent type.
        accounts = []  # List containing a list of accounts by parent type.
        subtotals = []  # List of subtotals by parent type.
        report_structure = []  # Full list of lists for the table(s)
        shares_dct = {}

        column_header = ["Account Name", "Account Type", "Balance"]
        column_header_alt = ["Account Name", "Shares Count", "Balance"]

        summary_style = [
            ('LINEABOVE', (0, 0), (-1, -1), 0.25, colors.black),
            ('LINEBELOW', (0, 0), (-1, -1), 0.25, colors.black),
            ('LINEBEFORE', (0, 0), (0, -1), 0.25, colors.black),
            ('LINEAFTER', (-1, 0), (-1, -1), 0.25, colors.black),
        ]

        # Generates the sql statement list for the different parent types and places into list
        for lst in parenttype_list:
            parent_type = lst[0]
            acc_statement = """SELECT ID, SubType, Balance, ParentType, Ticker_Symbol FROM Account_Summary WHERE ParentType='""" + parent_type + """' ORDER BY ID, SubType, Balance DESC LIMIT 0, 49999"""
            acc_statement_list.append(acc_statement)
            # Generates list of account balances by parent type
            st_statement = """SELECT SUM(Balance) FROM Account_summary WHERE ParentType= '""" + parent_type + """'"""
            st_statement_list.append(st_statement)

        # Generates list of account lists by parent type
        for statement in acc_statement_list:
            parenttype_qty = obtain_sql_list(statement, request[0], self.error_Logger)
            accounts.append(parenttype_qty)

        # Generate Dictionary of Equity Shares
        for parent in accounts:
            for account in parent:
                if account[3] == "Equity":
                    sql_account = remove_space(account[0])
                    share_statement = f"""SELECT SUM(Purchased - Sold) FROM '{sql_account}'"""
                    shares = obtain_sql_value(share_statement, request[0], self.error_Logger)
                    shares_dct[account[0]] = decimal_places(shares[0], 4)

        # Generates list of parent type subtotals
        for statement in st_statement_list:
            subtotal = obtain_sql_value(statement, request[0], self.error_Logger)
            subtotal = subtotal[0]

            if subtotal is None:
                subtotal = 0

            if "Debt" in statement or "Credit" in statement:
                subtotal = - subtotal

            subtotal = cash_format(subtotal, 2)
            subtotals.append(subtotal[1])

        # y used to iterate through parent types for report
        y = 0

        # Generates report_Structure which is composed of lists for each parent type to theoretically have their own table.
        for lst in parenttype_list:
            parent_type = lst[0]
            parenttype_acc_list = accounts[y]
            if len(parenttype_acc_list) == 0:
                pass
                y += 1
            else:
                if parent_type == "Equity":
                    temp_list = [lst, column_header_alt]
                else:
                    temp_list = [lst, column_header]

                for account in parenttype_acc_list:
                    balance = account[2]

                    if parent_type == "Debt" or parent_type == "Credit":
                        balance = - balance

                    formatted_balance = cash_format(balance, 2)

                    if parent_type == "Equity":
                        columnTwo = shares_dct[account[0]]
                    else:
                        columnTwo = account[1]

                    if account[4] is None:
                        convert = [account[0], columnTwo, formatted_balance[1]]
                    else:
                        final_name = f"({account[4]})  {account[0]}"
                        convert = [final_name, columnTwo, formatted_balance[1]]
                    temp_list.append(convert)
                subtotal_row = ["", "Subtotal", subtotals[y]]
                temp_list.append(subtotal_row)
                report_structure.append(temp_list)
                y += 1

        table_data = []  # List of lists of table data. Each sub list equates to a table
        table_header_rows = []  # List containing a list of table header rows. This is used for styling
        table_row_counts = []  # List of row counts for tables
        table_styles = []  # Contains a list containing a list of tables style

        table = []  # List to hold individual table data prior to being added to table_data
        header_rows = []  # List to hold individual table data

        total_row_count = 0
        ongoing_row_count = 0
        row_count = 0

        for pt_list in report_structure:
            count = len(pt_list)
            total_row_count += count

        # Breaks the report structure into separate tables.
        for pt_list in report_structure:  # report structure's outer lists are by parent type
            for row_list in pt_list:  # the inner list structure would be by row
                if len(table_data) < 1:
                    table.append(row_list)
                    if row_list in parenttype_list:
                        header_rows.append(row_count)
                    else:
                        pass
                    row_count += 1
                    ongoing_row_count += 1
                    # if row_count == 26 or row_list == report_structure[-1][-1]:
                    if row_count == 26 or ongoing_row_count == total_row_count:
                        table_data.append(table)
                        table_header_rows.append(header_rows)
                        table_row_counts.append(row_count)
                        table = []
                        header_rows = []
                        row_count = 0

                elif len(table_data) >= 1:
                    table.append(row_list)
                    if row_list in parenttype_list:
                        header_rows.append(row_count)
                    else:
                        pass
                    row_count += 1
                    ongoing_row_count += 1
                    # if row_count == 29 or row_list == report_structure[-1][-1]:
                    if row_count == 26 or ongoing_row_count == total_row_count:
                        table_data.append(table)
                        table_header_rows.append(header_rows)
                        table_row_counts.append(row_count)
                        table = []
                        header_rows = []
                        row_count = 0

        # used to iterate through tables
        t = 0

        # Builds the Style sheet for each table
        for table in table_data:
            build_style = self.set_style(table, table_header_rows[t], request[2])
            for style in summary_style:
                build_style.append(style)
            table_styles.append(build_style)
            t += 1

        return table_data, table_header_rows, table_row_counts, table_styles

    def set_style(self, table_data, header_rows, parenttypes):
        table_style = []
        table_components = []
        for x in range(0, len(header_rows)):
            reference_row = header_rows[x]
            try:
                next_ref_row = header_rows[x + 1]
            # if the reference row is the last in the header_rows list
            except IndexError:
                # if the last row is a "Subtotal"
                if table_data[-1][1] == "Subtotal":
                    next_ref_row = len(table_data)
                # if the last row is a header
                elif header_rows[x] == len(table_data):
                    next_ref_row = 0
                # if the last row is an account
                else:
                    next_ref_row = len(table_data)

            header_style = [
                ('VALIGN', (0, reference_row), (-1, reference_row), 'TOP'),
                ('BACKGROUND', (0, reference_row), (-1, reference_row), colors.green),
                ('TEXTCOLOR', (0, reference_row), (-1, reference_row), colors.white),
                ('FONTNAME', (0, reference_row), (-1, reference_row), 'Times-Bold'),
                ('FONTSIZE', (0, reference_row), (-1, reference_row), 12),
            ]
            columnH_style = [
                ('BACKGROUND', (0, reference_row + 1), (-1, reference_row + 1), colors.lightgrey),
                ('TEXTCOLOR', (0, reference_row + 1), (-1, reference_row + 1), colors.black),
                ('FONTNAME', (0, reference_row + 1), (-1, reference_row + 1), 'Times-Bold'),
                ('FONTSIZE', (0, reference_row + 1), (-1, reference_row + 1), 12),
                ('ALIGN', (0, reference_row + 1), (0, next_ref_row - 2), 'LEFT'),
                ('ALIGN', (1, reference_row + 1), (1, next_ref_row - 2), 'CENTER'),
            ]
            account_style = [
                ('FONTNAME', (0, reference_row + 2), (-1, next_ref_row - 1), 'Times-Roman'),
                ('FONTSIZE', (0, reference_row + 2), (-1, next_ref_row - 1), 11),
                ('BACKGROUND', (1, reference_row + 2), (1, next_ref_row - 1), colors.beige),
                ('ALIGN', (2, reference_row + 1), (2, next_ref_row - 2), 'RIGHT'),
            ]
            subtotal_style = [
                ('BACKGROUND', (0, next_ref_row - 1), (-1, next_ref_row - 1), colors.lightgrey),
                ('FONTNAME', (0, next_ref_row - 1), (-1, next_ref_row - 1), 'Times-Bold'),
                ('FONTSIZE', (0, next_ref_row - 1), (-1, next_ref_row - 1), 12),
                ('ALIGN', (1, next_ref_row - 1), (-1, next_ref_row - 1), 'RIGHT'),
            ]
            last_row = [
                ('ALIGN', (1, -1), (1, -1), 'CENTER'),
                ('ALIGN', (2, -1), (2, -1), 'RIGHT'),
            ]

            if reference_row == header_rows[-1]:
                if table_data[-1][1] == "Subtotal":
                    table_components.append(header_style)
                    table_components.append(columnH_style)
                    table_components.append(account_style)
                    table_components.append(subtotal_style)
                elif table_data[-1] in parenttypes:
                    table_components.append(header_style)
                else:
                    table_components.append(header_style)
                    table_components.append(columnH_style)
                    table_components.append(account_style)
                    table_components.append(last_row)
            else:
                table_components.append(header_style)
                table_components.append(columnH_style)
                table_components.append(account_style)
                table_components.append(subtotal_style)

            if header_rows[0] != 0:
                if table_data[0][1] == "Subtotal":
                    reference_row = 0

                    subtotal_first_row = [
                        ('BACKGROUND', (0, reference_row), (-1, reference_row), colors.lightgrey),
                        ('FONTNAME', (0, reference_row), (-1, reference_row), 'Times-Bold'),
                        ('FONTSIZE', (0, reference_row), (-1, reference_row), 12),
                        ('ALIGN', (1, reference_row), (-1, reference_row), 'RIGHT'),
                    ]

                    table_components.append(subtotal_first_row)

                elif table_data[0][0] == "Account Name":
                    reference_row = 0
                    next_ref_row = header_rows[0]

                    columnH_first_row = [
                        ('BACKGROUND', (0, reference_row), (-1, reference_row), colors.lightgrey),
                        ('TEXTCOLOR', (0, reference_row), (-1, reference_row), colors.black),
                        ('FONTNAME', (0, reference_row), (-1, reference_row), 'Times-Bold'),
                        ('FONTSIZE', (0, reference_row), (-1, reference_row), 12),
                        ('ALIGN', (0, reference_row), (0, next_ref_row - 2), 'LEFT'),
                        ('ALIGN', (1, reference_row), (1, next_ref_row - 2), 'CENTER'),
                        ('ALIGN', (1, reference_row), (2, next_ref_row - 2), 'RIGHT'),

                        ('FONTNAME', (0, reference_row + 1), (-1, next_ref_row - 2), 'Times-Roman'),
                        ('FONTSIZE', (0, reference_row + 1), (-1, next_ref_row - 2), 11),
                        ('BACKGROUND', (1, reference_row + 1), (1, next_ref_row - 2), colors.beige),
                        ('ALIGN', (1, reference_row), (1, next_ref_row - 2), 'CENTER'),

                        ('BACKGROUND', (0, next_ref_row - 1), (-1, next_ref_row - 1), colors.lightgrey),
                        ('FONTNAME', (0, next_ref_row - 1), (-1, next_ref_row - 1), 'Times-Bold'),
                        ('FONTSIZE', (0, next_ref_row - 1), (-1, next_ref_row - 1), 12),
                        ('ALIGN', (1, next_ref_row - 1), (-1, next_ref_row - 1), 'RIGHT'),

                    ]

                    table_components.append(columnH_first_row)

                else:
                    reference_row = 0
                    next_ref_row = header_rows[0]

                    missing_header = [
                        ('FONTNAME', (0, reference_row), (-1, next_ref_row - 2), 'Times-Roman'),
                        ('FONTSIZE', (0, reference_row), (-1, next_ref_row - 2), 12),
                        ('BACKGROUND', (1, reference_row), (1, next_ref_row - 2), colors.beige),
                        ('ALIGN', (1, reference_row), (1, next_ref_row - 2), 'CENTER'),
                        ('ALIGN', (2, reference_row), (2, next_ref_row - 2), 'RIGHT'),
                        ('BACKGROUND', (0, next_ref_row - 1), (-1, next_ref_row - 1), colors.lightgrey),
                        ('FONTNAME', (0, next_ref_row - 1), (-1, next_ref_row - 1), 'Times-Bold'),
                        ('FONTSIZE', (0, next_ref_row - 1), (-1, next_ref_row - 1), 12),
                        ('ALIGN', (1, next_ref_row - 1), (-1, next_ref_row - 1), 'RIGHT'),
                    ]

                    table_components.append(missing_header)

            for lst in table_components:
                for style in lst:
                    table_style.append(style)

        return table_style

    def generate_snapshot(self, request):
        assets = 0
        liabilities = 0
        for header_lst in request[2]:
            parent_type = header_lst[0]
            statement = "SELECT sum(Balance) FROM main.Account_Summary WHERE ParentType='" + parent_type + "'"
            raw_balance = obtain_sql_value(statement, request[0], self.error_Logger)
            raw_balance = raw_balance[0]
            if raw_balance is None:
                raw_balance = 0.0
            if parent_type == "Debt" or parent_type == "Credit":
                balance = -raw_balance
                liabilities += balance
            else:
                assets += raw_balance

        display_assets = cash_format(assets, 2)
        display_liabilities = cash_format(liabilities, 2)
        display_net = cash_format((assets + liabilities), 2)
        snapshot = [display_assets[1], display_liabilities[1], display_net[1]]

        return snapshot


if __name__ == "__main__":
    sys.tracebacklimit = 0
    raise RuntimeError(f"Check your Executable File.\n{os.path.basename(__file__)} is not intended as independent script")
