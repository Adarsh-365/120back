import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER

def create_invoice(filename="membership_invoice.pdf"):
    # Page setup - Letter size is 612 x 792 pt. 
    # Using 40pt margins leaves exactly 532pt of usable horizontal width.
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    # Color Palette Matching the Image
    PRIMARY_COLOR = colors.HexColor("#643C6E")  # Deep plum purple
    TEXT_DARK = colors.HexColor("#2D2D2D")      # Dark gray for body/headings
    TEXT_LIGHT = colors.HexColor("#5A5A5A")     # Muted gray for secondary text

    styles = getSampleStyleSheet()

    # --- Custom Typography / Styles ---
    company_name_style = ParagraphStyle(
        'CompanyNameStyle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=TEXT_DARK
    )

    company_style = ParagraphStyle(
        'CompanyStyle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=TEXT_LIGHT
    )

    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=30,
        leading=36,
        alignment=TA_RIGHT,
        textColor=PRIMARY_COLOR
    )

    bill_to_title = ParagraphStyle(
        'BillToTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14,
        textColor=PRIMARY_COLOR,
        spaceAfter=6
    )

    bill_to_name = ParagraphStyle(
        'BillToName',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=TEXT_DARK,
        spaceAfter=4
    )

    bill_to_details = ParagraphStyle(
        'BillToDetails',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=TEXT_DARK
    )

    meta_label = ParagraphStyle(
        'MetaLabel',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=14,
        alignment=TA_RIGHT,
        textColor=PRIMARY_COLOR
    )

    meta_val = ParagraphStyle(
        'MetaVal',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        alignment=TA_RIGHT,
        textColor=TEXT_DARK
    )

    table_header = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=12,
        textColor=colors.white
    )

    table_header_right = ParagraphStyle(
        'TableHeaderRight',
        parent=table_header,
        alignment=TA_RIGHT
    )

    table_cell = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=TEXT_DARK
    )

    table_cell_right = ParagraphStyle(
        'TableCellRight',
        parent=table_cell,
        alignment=TA_RIGHT
    )

    summary_label = ParagraphStyle(
        'SummaryLabel',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=TEXT_DARK
    )

    summary_label_bold = ParagraphStyle(
        'SummaryLabelBold',
        parent=summary_label,
        fontName='Helvetica-Bold',
        textColor=PRIMARY_COLOR
    )

    summary_val = ParagraphStyle(
        'SummaryVal',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        alignment=TA_RIGHT,
        textColor=TEXT_DARK
    )

    summary_val_bold = ParagraphStyle(
        'SummaryValBold',
        parent=summary_val,
        fontName='Helvetica-Bold',
        textColor=PRIMARY_COLOR
    )

    terms_title = ParagraphStyle(
        'TermsTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=PRIMARY_COLOR,
        spaceAfter=6
    )

    terms_body = ParagraphStyle(
        'TermsBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=TEXT_DARK
    )

    story = []

    # --- 1. HEADER SECTION (Company Info & Logo) ---
    company_info = [
        Paragraph("Your Company Inc.", company_name_style),
        Paragraph("1234 Company St,", company_style),
        Paragraph("Company Town, ST 12345", company_style)
    ]

    # Handle logo dynamically. It will render "logo.png" if present.
    if os.path.exists("logo.png"):
        logo_flowable = Image("images/logo.png", width=180, height=60)
    else:
        # Styled fallback box matching the "Upload Logo" look in your image
        logo_flowable = Table(
            [[Paragraph("<font color='#643C6E'>☁ <b>Upload Logo</b></font>", ParagraphStyle('PH', alignment=TA_CENTER, fontName='Helvetica', fontSize=14))]],
            colWidths=[180], rowHeights=[60]
        )
        logo_flowable.setStyle(TableStyle([
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#D1C4D9")), 
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F9F6FA")), 
        ]))

    header_table = Table([[company_info, logo_flowable]], colWidths=[352, 180])
    header_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ALIGN', (1,0), (1,0), 'RIGHT'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(header_table)
    story.append(Spacer(1, 20))

    # --- 2. TITLE SECTION ---
    title_para = Paragraph("MEMBERSHIP<br/>INVOICE", title_style)
    story.append(title_para)
    story.append(Spacer(1, 25))

    # --- 3. BILL TO & METADATA SECTION ---
    bill_to_flowables = [
        Paragraph("Bill To", bill_to_title),
        Paragraph("Customer Name", bill_to_name),
        Paragraph("1234 Customer St,", bill_to_details),
        Paragraph("Customer Town, ST 12345", bill_to_details)
    ]

    meta_data = [
        [Paragraph("Invoice #", meta_label), Paragraph("0000007", meta_val)],
        [Paragraph("Invoice date", meta_label), Paragraph("10-02-2025", meta_val)],
        [Paragraph("Due date", meta_label), Paragraph("10-16-2025", meta_val)]
    ]
    meta_table = Table(meta_data, colWidths=[110, 90])
    meta_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
    ]))

    middle_table = Table([[bill_to_flowables, meta_table]], colWidths=[332, 200])
    middle_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ALIGN', (1,0), (1,0), 'RIGHT'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(middle_table)
    story.append(Spacer(1, 30))

    # --- 4. ITEMS TABLE ---
    # Col widths sum up to 532 (40 + 292 + 100 + 100)
    table_data = [
        [
            Paragraph("QTY", table_header),
            Paragraph("Description", table_header),
            Paragraph("Unit Price", table_header_right),
            Paragraph("Amount", table_header_right)
        ],
        [
            Paragraph("1", table_cell),
            Paragraph("Annual membership fee", table_cell),
            Paragraph("300.00", table_cell_right),
            Paragraph("$300.00", table_cell_right)
        ],
        [
            Paragraph("1", table_cell),
            Paragraph("Access to premium content", table_cell),
            Paragraph("150.00", table_cell_right),
            Paragraph("$150.00", table_cell_right)
        ],
        [
            Paragraph("1", table_cell),
            Paragraph("Exclusive event entry", table_cell),
            Paragraph("100.00", table_cell_right),
            Paragraph("$100.00", table_cell_right)
        ],
        [
            Paragraph("1", table_cell),
            Paragraph("Monthly newsletter & perks", table_cell),
            Paragraph("50.00", table_cell_right),
            Paragraph("$50.00", table_cell_right)
        ]
    ]

    items_table = Table(table_data, colWidths=[40, 292, 100, 100])
    items_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY_COLOR),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('LINEBELOW', (0, -1), (-1, -1), 1, PRIMARY_COLOR),
    ]))
    story.append(items_table)
    story.append(Spacer(1, 10))

    # --- 5. SUMMARY SECTION ---
    # Column alignments align perfectly with the "Unit Price" and "Amount" columns above
    summary_data = [
        [
            "",
            Paragraph("Subtotal", summary_label),
            Paragraph("$600.00", summary_val)
        ],
        [
            "",
            Paragraph("Sales Tax ( 5% )", summary_label),
            Paragraph("$30.00", summary_val)
        ],
        [
            "",
            Paragraph("Total (USD)", summary_label_bold),
            Paragraph("$630.00", summary_val_bold)
        ]
    ]

    summary_table = Table(summary_data, colWidths=[332, 100, 100])
    summary_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (1,0), (-1,-1), 8),
        ('RIGHTPADDING', (1,0), (-1,-1), 8),
        ('LINEABOVE', (1, 2), (2, 2), 1, PRIMARY_COLOR),
        ('LINEBELOW', (1, 2), (2, 2), 1.5, PRIMARY_COLOR),
    ]))
    story.append(summary_table)
    story.append(Spacer(1, 100)) # Pushes terms to the bottom dynamically

    # --- 6. TERMS & CONDITIONS ---
    terms_flowables = [
        Paragraph("Terms and Conditions", terms_title),
        Paragraph("Payment is due in 14 days", terms_body),
        Paragraph("Please make checks payable to: Your Company Inc.", terms_body)
    ]
    story.append(KeepTogether(terms_flowables))

    # Build PDF File
    doc.build(story)

if __name__ == "__main__":
    create_invoice()