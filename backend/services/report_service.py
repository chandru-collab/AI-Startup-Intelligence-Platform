from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.lib import colors
from reportlab.graphics.shapes import Drawing, Rect, String, Line
from reportlab.pdfgen import canvas
import os
import re
import json
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

def clean_pdf_text(text: str) -> str:
    """Sanitize text to avoid invalid characters or unprintable unicode symbols in ReportLab standard fonts."""
    if not text:
        return ""
    
    # Common currency and typography symbol replacements
    replacements = {
        "₹": "INR ",
        "€": "EUR ",
        "£": "GBP ",
        "’": "'",
        "‘": "'",
        "“": '"',
        "”": '"',
        "–": "-",
        "—": "-",
        "•": "*",
        "\u25a0": "",  # remove unicode black box
    }
    
    for orig, repl in replacements.items():
        text = text.replace(orig, repl)
        
    # Convert non-ascii to safe HTML entity equivalents or ascii fallbacks
    cleaned = []
    for char in text:
        if ord(char) < 128:
            cleaned.append(char)
        elif char in ("\n", "\r", "\t"):
            cleaned.append(char)
        else:
            cleaned.append(f"&#{ord(char)};")
    return "".join(cleaned)


class NumberedCanvas(canvas.Canvas):
    """Pass-through canvas that computes dynamic 'Page X of Y' footers and top headers."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 9)
        self.setFillColor(colors.HexColor("#64748b"))

        # Running Header (Page 2+)
        if self._pageNumber > 1:
            self.drawString(54, 750, "Executive Intelligence Report")
            self.setStrokeColor(colors.HexColor("#cbd5e1"))
            self.setLineWidth(0.5)
            self.line(54, 742, 558, 742)

        # Running Footer (All Pages)
        self.setStrokeColor(colors.HexColor("#cbd5e1"))
        self.setLineWidth(0.5)
        self.line(54, 45, 558, 45)

        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 30, page_text)
        self.drawString(54, 30, "CONFIDENTIAL - AI STARTUP INTELLIGENCE")
        self.restoreState()


class ReportService:
    def __init__(self):
        self.reports_dir = "generated_reports"
        if not os.path.exists(self.reports_dir):
            os.makedirs(self.reports_dir)

    def draw_growth_meter(self, growth_text: str):
        """Draws a responsive, 504pt full-width visual growth meter infographic."""
        d = Drawing(504, 65)
        
        trajectory = str(growth_text).lower()
        fill_color = colors.HexColor("#3b82f6") # default blue
        percent = 0.55
        label = "Moderate Growth"
        
        if re.search(r'\b(high|hyper|rapid|strong|surge|explosive)\b', trajectory):
            fill_color = colors.HexColor("#16a34a") # green
            percent = 0.85
            label = "High Growth"
        elif re.search(r'\b(low|struggling|decline|stagnant|slow|risk|unfunded)\b', trajectory):
            fill_color = colors.HexColor("#dc2626") # red
            percent = 0.25
            label = "Low Growth"
            
        # Background bar (504pt full width)
        d.add(Rect(0, 18, 504, 20, fillColor=colors.HexColor("#f1f5f9"), strokeColor=colors.HexColor("#cbd5e1"), rx=4, ry=4))
        
        # Fill bar
        bar_width = int(504 * percent)
        d.add(Rect(0, 18, bar_width, 20, fillColor=fill_color, strokeColor=None, rx=4, ry=4))
        
        # Axis Labels
        d.add(String(2, 2, "Low Growth", fontSize=9, fontName="Helvetica-Bold", fillColor=colors.HexColor("#64748b")))
        d.add(String(225, 2, "Moderate Growth", fontSize=9, fontName="Helvetica-Bold", fillColor=colors.HexColor("#64748b")))
        d.add(String(440, 2, "High Growth", fontSize=9, fontName="Helvetica-Bold", fillColor=colors.HexColor("#64748b")))
        
        # Indicator Label above bar
        badge_x = min(max(bar_width - 45, 5), 410)
        d.add(String(badge_x, 44, f"Prediction: {label}", fontSize=11, fontName="Helvetica-Bold", fillColor=fill_color))
        
        return d

    def make_section_header(self, title_text: str) -> Table:
        """Creates a full-width (504pt) section header card."""
        p_style = ParagraphStyle(
            'SecHeaderStyle',
            fontName='Helvetica-Bold',
            fontSize=12,
            leading=15,
            textColor=colors.HexColor("#1e3a8a")
        )
        p = Paragraph(f"<b>{title_text}</b>", p_style)
        t = Table([[p]], colWidths=[7.0 * inch])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#e0e7ff")),
            ('PADDING', (0,0), (-1,-1), 6),
            ('TOPPADDING', (0,0), (-1,-1), 6),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
            ('LEFTPADDING', (0,0), (-1,-1), 8),
            ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ]))
        return t

    def generate_startup_pdf(self, state_data: dict) -> str:
        startup_name = state_data.get("startup_name", "Unknown_Startup")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.reports_dir}/{startup_name}_{timestamp}.pdf"
        
        try:
            doc = SimpleDocTemplate(
                filename,
                pagesize=letter,
                rightMargin=0.75 * inch,
                leftMargin=0.75 * inch,
                topMargin=0.75 * inch,
                bottomMargin=0.75 * inch
            )
            
            Story = []
            styles = getSampleStyleSheet()
            
            # Master Typography Styles
            title_style = ParagraphStyle(
                'DocTitle',
                parent=styles['Heading1'],
                fontName='Helvetica-Bold',
                fontSize=24,
                leading=28,
                textColor=colors.HexColor("#1e293b"),
                alignment=TA_CENTER,
                spaceAfter=4
            )
            
            subtitle_style = ParagraphStyle(
                'DocSubtitle',
                parent=styles['Normal'],
                fontName='Helvetica',
                fontSize=12,
                leading=16,
                textColor=colors.HexColor("#475569"),
                alignment=TA_CENTER,
                spaceAfter=4
            )
            
            date_style = ParagraphStyle(
                'DocDate',
                parent=styles['Normal'],
                fontName='Helvetica',
                fontSize=9,
                leading=12,
                textColor=colors.HexColor("#94a3b8"),
                alignment=TA_CENTER,
                spaceAfter=18
            )
            
            body_style = ParagraphStyle(
                'DocBody',
                parent=styles['Normal'],
                fontName='Helvetica',
                fontSize=10,
                leading=15,
                textColor=colors.HexColor("#334155"),
                spaceAfter=8
            )
            
            bullet_style = ParagraphStyle(
                'DocBullet',
                parent=body_style,
                leftIndent=12,
                spaceAfter=6
            )
            
            table_header_style = ParagraphStyle(
                'TblHeader',
                fontName='Helvetica-Bold',
                fontSize=11,
                leading=14,
                textColor=colors.whitesmoke
            )
            
            tbl_cell_title = ParagraphStyle(
                'TblCellTitle',
                fontName='Helvetica-Bold',
                fontSize=10,
                leading=14,
                textColor=colors.HexColor("#1e293b")
            )
            
            tbl_cell_body = ParagraphStyle(
                'TblCellBody',
                fontName='Helvetica',
                fontSize=9.5,
                leading=14,
                textColor=colors.HexColor("#334155")
            )

            # --- HEADER BANNER ---
            Story.append(Paragraph("Executive Intelligence Report", title_style))
            Story.append(Paragraph(f"Target Entity: <b>{clean_pdf_text(startup_name.upper())}</b>", subtitle_style))
            Story.append(Paragraph(f"Generated on {datetime.now().strftime('%B %d, %Y at %H:%M:%S')}", date_style))
            Story.append(Spacer(1, 8))
            
            # Extract and Clean Data
            summary = clean_pdf_text(str(state_data.get("research_data", {}).get("summary", "No summary available.")))
            funding = clean_pdf_text(str(state_data.get("funding_data", {}).get("analysis", "No funding data.")))
            hiring = clean_pdf_text(str(state_data.get("hiring_data", {}).get("analysis", "No hiring data.")))
            news_raw = state_data.get("news_data", {}).get("headlines", "No news data.")
            social = clean_pdf_text(str(state_data.get("social_data", {}).get("sentiment_analysis", "No social data.")))
            verification = clean_pdf_text(str(state_data.get("verification_status", {}).get("details", "Not verified.")))
            growth = clean_pdf_text(str(state_data.get("growth_prediction", {}).get("trajectory", "Unknown")))
            recommendation = clean_pdf_text(str(state_data.get("investment_insights", {}).get("recommendation", "Unknown")))
            
            # --- 1. OVERVIEW ---
            Story.append(self.make_section_header("1. Executive Overview"))
            Story.append(Spacer(1, 8))
            Story.append(Paragraph(summary.replace('\n', '<br/>'), body_style))
            Story.append(Spacer(1, 10))
            
            # --- 2. METRICS TABLE ---
            Story.append(self.make_section_header("2. Key Indicators"))
            Story.append(Spacer(1, 8))
            
            table_data = [
                [
                    Paragraph("Metric", table_header_style),
                    Paragraph("Analysis Summary", table_header_style)
                ],
                [
                    Paragraph("Funding & Runway", tbl_cell_title),
                    Paragraph(funding.replace('\n', '<br/>'), tbl_cell_body)
                ],
                [
                    Paragraph("Hiring & Team", tbl_cell_title),
                    Paragraph(hiring.replace('\n', '<br/>'), tbl_cell_body)
                ],
                [
                    Paragraph("Social Sentiment", tbl_cell_title),
                    Paragraph(social.replace('\n', '<br/>'), tbl_cell_body)
                ]
            ]
            
            t = Table(table_data, colWidths=[1.75 * inch, 5.25 * inch])
            t.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1e3a8a")),
                ('ALIGN', (0,0), (-1,-1), 'LEFT'),
                ('VALIGN', (0,0), (-1,-1), 'TOP'),
                ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor("#ffffff"), colors.HexColor("#f8fafc")]),
                ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
                ('TOPPADDING', (0,0), (-1,-1), 7),
                ('BOTTOMPADDING', (0,0), (-1,-1), 7),
                ('LEFTPADDING', (0,0), (-1,-1), 8),
                ('RIGHTPADDING', (0,0), (-1,-1), 8),
            ]))
            Story.append(t)
            Story.append(Spacer(1, 14))
            
            # --- 3. INFOGRAPHIC: GROWTH ---
            growth_flowables = [
                self.make_section_header("3. Growth Trajectory Prediction"),
                Spacer(1, 8),
                Paragraph(growth.replace('\n', '<br/>'), body_style),
                Spacer(1, 6),
                self.draw_growth_meter(growth),
                Spacer(1, 14)
            ]
            Story.append(KeepTogether(growth_flowables))
            
            # --- 4. VERIFICATION STATUS ---
            is_verified = state_data.get("verification_status", {}).get("is_verified", False)
            ver_bg = colors.HexColor("#dcfce7") if is_verified else colors.HexColor("#fee2e2")
            ver_border = colors.HexColor("#86efac") if is_verified else colors.HexColor("#fca5a5")
            ver_text_color = colors.HexColor("#15803d") if is_verified else colors.HexColor("#b91c1c")
            
            status_header = "STATUS: VERIFIED" if is_verified else "STATUS: DISCREPANCIES FOUND"
            
            ver_p = Paragraph(
                f"<b>{status_header}</b><br/>{verification.replace(chr(10), '<br/>')}",
                ParagraphStyle(
                    'VerCardContent',
                    fontName='Helvetica',
                    fontSize=9.5,
                    leading=14,
                    textColor=ver_text_color
                )
            )
            
            ver_table = Table([[ver_p]], colWidths=[7.0 * inch])
            ver_table.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,-1), ver_bg),
                ('BOX', (0,0), (-1,-1), 1, ver_border),
                ('PADDING', (0,0), (-1,-1), 10),
                ('TOPPADDING', (0,0), (-1,-1), 10),
                ('BOTTOMPADDING', (0,0), (-1,-1), 10),
            ]))
            
            ver_flowables = [
                self.make_section_header("4. Data Verification Status"),
                Spacer(1, 8),
                ver_table,
                Spacer(1, 14)
            ]
            Story.append(KeepTogether(ver_flowables))
            
            # --- 5. RECENT NEWS ---
            Story.append(self.make_section_header("5. Recent Intelligence (News)"))
            Story.append(Spacer(1, 8))
            
            # Parse news into bullet list if formatted as stringified python list or multiline string
            news_items = []
            if isinstance(news_raw, list):
                news_items = [clean_pdf_text(str(item)) for item in news_raw]
            elif isinstance(news_raw, str):
                cleaned_news = news_raw.strip()
                if cleaned_news.startswith("[") and cleaned_news.endswith("]"):
                    try:
                        import ast
                        parsed_items = ast.literal_eval(cleaned_news)
                        if isinstance(parsed_items, list):
                            news_items = [clean_pdf_text(str(item)) for item in parsed_items]
                    except Exception:
                        pass
                if not news_items:
                    news_items = [clean_pdf_text(line.strip("-• ")) for line in cleaned_news.split("\n") if line.strip()]
                    
            if news_items:
                for item in news_items:
                    Story.append(Paragraph(f"• {item}", bullet_style))
            else:
                Story.append(Paragraph("No recent news recorded.", body_style))
                
            Story.append(Spacer(1, 14))
            
            # --- 6. RECOMMENDATION ---
            rec_p = Paragraph(
                f"<b>RECOMMENDATION & INVESTMENT THESIS</b><br/><br/>{recommendation.replace(chr(10), '<br/>')}",
                ParagraphStyle(
                    'RecCardContent',
                    fontName='Helvetica-Bold',
                    fontSize=11,
                    leading=16,
                    alignment=TA_CENTER,
                    textColor=colors.HexColor("#ffffff")
                )
            )
            
            rec_table = Table([[rec_p]], colWidths=[7.0 * inch])
            rec_table.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#1e3a8a")),
                ('PADDING', (0,0), (-1,-1), 14),
                ('TOPPADDING', (0,0), (-1,-1), 14),
                ('BOTTOMPADDING', (0,0), (-1,-1), 14),
                ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ]))
            
            rec_flowables = [
                self.make_section_header("6. Investment Thesis & Recommendation"),
                Spacer(1, 8),
                rec_table
            ]
            Story.append(KeepTogether(rec_flowables))
            
            # Build PDF with NumberedCanvas callback
            doc.build(Story, canvasmaker=NumberedCanvas)
            logger.info(f"Generated perfectly aligned PDF report: {filename}")
            return filename
            
            
        except Exception as e:
            logger.error(f"Failed to generate PDF for {startup_name}: {e}")
            import traceback
            logger.error(traceback.format_exc())
            return ""

report_service = ReportService()

