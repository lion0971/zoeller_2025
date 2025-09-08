from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Flowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# 註冊 Noto Sans TC 開源字型
pdfmetrics.registerFont(TTFont('NotoSansTC', 'NotoSansTC-VariableFont_wght.ttf'))

# PDF 檔案名稱
filename = "服務學習活動方案_NotoSansTC_分隔線.pdf"

# 建立 PDF
doc = SimpleDocTemplate(filename, pagesize=A4,
                        rightMargin=2*cm, leftMargin=2*cm,
                        topMargin=2*cm, bottomMargin=2*cm)

styles = getSampleStyleSheet()

# 設定中文字型
styles["Normal"].fontName = 'NotoSansTC'
styles["Normal"].fontSize = 12
styles["Normal"].leading = 20

styles.add(ParagraphStyle(name='TitleChinese',
                          parent=styles['Heading1'],
                          fontName='NotoSansTC',
                          fontSize=18,
                          leading=24,
                          spaceAfter=20,
                          alignment=1,
                          textColor=colors.HexColor("#2E4053")))

styles.add(ParagraphStyle(name='SectionHeader',
                          parent=styles['Heading2'],
                          fontName='NotoSansTC',
                          fontSize=14,
                          leading=20,
                          spaceAfter=6,
                          textColor=colors.HexColor("#1A5276")))

# 自訂分隔線 Flowable
class SectionDivider(Flowable):
    def __init__(self, width, height=4, color=colors.HexColor("#D6EAF8")):
        super().__init__()
        self.width = width
        self.height = height
        self.color = color

    def draw(self):
        self.canv.setFillColor(self.color)
        self.canv.rect(0, 0, self.width, self.height, fill=1, stroke=0)

# 頁首頁尾
def header_footer(canvas, doc):
    canvas.saveState()
    width, height = A4
    # 頁首色塊
    canvas.setFillColor(colors.HexColor("#A9CCE3"))
    canvas.rect(0, height-30, width, 30, fill=True, stroke=False)
    canvas.setFillColor(colors.black)
    canvas.setFont('NotoSansTC', 10)
    canvas.drawString(2*cm, height-20, "服務學習活動方案")
    # 頁尾色塊
    canvas.setFillColor(colors.HexColor("#D6DBDF"))
    canvas.rect(0, 0, width, 30, fill=True, stroke=False)
    canvas.setFillColor(colors.black)
    canvas.setFont('NotoSansTC', 10)
    canvas.drawRightString(width-2*cm, 15, f"第 {doc.page} 頁")
    canvas.restoreState()

# 內容
content = []

# 封面
content.append(Spacer(1, 8*cm))
content.append(Paragraph("服務學習活動方案", styles['TitleChinese']))
content.append(Spacer(1, 4*cm))
content.append(Paragraph("申請職位：課外活動行政專員", styles['Normal']))
content.append(Paragraph("應徵者：XXX", styles['Normal']))
content.append(PageBreak())

# 範例章節
sections = [
    ("🌱 活動方案名稱", "社區健康小幫手：大學生走入社區的健康促進服務學習計畫"),
    ("🎯 活動目標", "1. 結合醫學、護理、生命科學專業，讓學生將所學應用於真實場域。\n"
                     "2. 協助社區民眾提升健康知識與自我照護能力。\n"
                     "3. 培養學生公共服務態度、團隊合作與跨域溝通能力。\n"
                     "4. 建立大學與社區的長期合作平台，實踐大學社會責任（USR）。"),
    ("👥 參與對象", "‧ 陽明交通大學在學學生（醫學、護理、藥學、公共衛生、生命科學系為主，亦開放跨院系參與）。\n"
                     "‧ 服務對象：鄰近社區居民、銀髮族、弱勢家庭。"),
    ("📅 活動內容與流程", "1️⃣ 前期培訓（2週）\n"
                     "- 工作坊：健康促進與社區服務倫理\n"
                     "- 跨系小組分工（健康檢測組、衛教宣導組、生活關懷組）\n"
                     "- 學習基本服務技巧（血壓量測、健康諮詢、簡易心肺復甦術、飲食運動衛教）\n\n"
                     "2️⃣ 社區服務（4週）\n"
                     "- 每週一次，深入合作社區據點\n"
                     "- 活動：健康檢測、衛教小講堂、生活關懷、親子互動\n\n"
                     "3️⃣ 成果回饋（1週）\n"
                     "- 成果分享會，學生小組提交服務反思報告"),
    ("📊 預期效益", "‧ 對學生：提升公共服務能力、加深專業知識實踐、培養同理心\n"
                     "‧ 對社區：居民獲得基礎健康知識、增強自我健康管理能力\n"
                     "‧ 對學校：展現大學社會責任，強化校園與社區連結"),
    ("💡 評估方式", "1. 學生：服務反思報告 + 同儕互評 + 導師回饋\n"
                     "2. 社區：問卷調查民眾滿意度\n"
                     "3. 學校：活動成果納入USR案例")
]

for title, text in sections:
    content.append(Paragraph(title, styles['SectionHeader']))
    # 加入分隔線
    content.append(Spacer(1,2))
    content.append(SectionDivider(width=doc.width, height=4, color=colors.HexColor("#D6EAF8")))
    content.append(Spacer(1,6))
    content.append(Paragraph(text.replace("\n","<br/>"), styles['Normal']))
    content.append(Spacer(1, 12))

# 生成 PDF
doc.build(content, onFirstPage=header_footer, onLaterPages=header_footer)

print(f"已生成 PDF: {filename}")