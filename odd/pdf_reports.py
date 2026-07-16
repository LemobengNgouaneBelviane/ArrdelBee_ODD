import io
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.units import cm
from django.conf import settings
from django.utils.timezone import now as timezone_now
import os

def generate_project_alignment_report(project):
    """
    Génère un rapport PDF d'alignement ODD pour un projet.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=2*cm, leftMargin=2*cm, topMargin=2*cm, bottomMargin=2*cm)
    styles = getSampleStyleSheet()
    
    # Styles personnalisés
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.HexColor('#1a237e'),
        alignment=1, # Center
        spaceAfter=20
    )
    
    section_style = ParagraphStyle(
        'SectionStyle',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#1a237e'),
        spaceBefore=15,
        spaceAfter=10,
        borderPadding=5,
        borderWidth=0,
        backColor=colors.HexColor('#f0f1f5')
    )

    elements = []

    # 1. Logo et En-tête
    logo_path = os.path.join(settings.BASE_DIR, '../Frontend_General_Arrdel/public/logo-arrdelbee.jpg')
    if os.path.exists(logo_path):
        img = Image(logo_path, width=4*cm, height=2*cm)
        img.hAlign = 'CENTER'
        elements.append(img)
    
    elements.append(Spacer(1, 0.5*cm))
    elements.append(Paragraph("FICHE D'ALIGNEMENT ODD & SND30", title_style))
    elements.append(Paragraph(f"PROJET : {project.name.upper()}", styles['Heading3']))
    elements.append(Spacer(1, 0.5*cm))

    # 2. Informations Générales
    data_info = [
        ["Territoire :", project.territory or "Non spécifié"],
        ["Secteur :", project.sector.name if project.sector else "Non spécifié"],
        ["Budget :", f"{project.budget:,.0f} FCFA".replace(',', ' ')],
        ["Bénéficiaires :", str(project.beneficiaries_count or "Non spécifié")],
        ["Statut :", project.get_status_display()],
        ["Date de certification :", project.updated_at.strftime("%d/%m/%Y") if project.status == 'validated' else "En cours"],
    ]
    t_info = Table(data_info, colWidths=[5*cm, 10*cm])
    t_info.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ]))
    elements.append(t_info)

    # 3. Scores et Performance
    elements.append(Paragraph("SCORES DE PERFORMANCE ET ALIGNEMENT", section_style))
    data_scores = [
        ["Indicateur", "Score", "Poids", "Score Pondéré"],
        ["Alignement ODD", f"{project.score_odd}%", "45%", f"{float(project.score_odd)*0.45:.1f}"],
        ["Alignement SND30", f"{project.score_snd30}%", "30%", f"{float(project.score_snd30)*0.3:.1f}"],
        ["Alignement Local (PCD/PRD)", f"{project.score_local}%", "25%", f"{float(project.score_local)*0.25:.1f}"],
        ["SCORE GLOBAL", f"{project.score_global}%", "100%", f"{project.score_global}"],
    ]
    t_scores = Table(data_scores, colWidths=[6*cm, 3*cm, 3*cm, 3*cm])
    t_scores.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a237e')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#e8eaf6')),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ]))
    elements.append(t_scores)
    
    elements.append(Spacer(1, 0.5*cm))
    elements.append(Paragraph(f"GRADE DE CERTIFICATION : {project.grade}", styles['Heading3']))

    # 4. Détails des Alignements ODD
    elements.append(Paragraph("DÉTAILS DES ALIGNEMENTS ODD", section_style))
    alignments = project.sdg_alignments.select_related('indicator__target__sdg')
    if alignments.exists():
        data_odd = [["Code", "ODD", "Description de l'indicateur"]]
        for al in alignments:
            data_odd.append([
                al.indicator.code,
                f"ODD {al.indicator.target.sdg.number}",
                Paragraph(al.indicator.description, styles['Normal'])
            ])
        t_odd = Table(data_odd, colWidths=[2.5*cm, 2*cm, 10.5*cm])
        t_odd.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f5f5f5')),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]))
        elements.append(t_odd)
    else:
        elements.append(Paragraph("Aucun alignement ODD enregistré.", styles['Italic']))

    # 5. Axes SND30
    elements.append(Paragraph("ALIGNEMENT STRATÉGIE NATIONALE (SND30)", section_style))
    snd30 = project.snd30_alignments.select_related('axis')
    if snd30.exists():
        for al in snd30:
            elements.append(Paragraph(f"<b>Axe {al.axis.number} :</b> {al.axis.name}", styles['Normal']))
            elements.append(Spacer(1, 0.1*cm))
    else:
        elements.append(Paragraph("Aucun axe SND30 sélectionné.", styles['Italic']))

    # Pied de page (Simulation de tampon/signature)
    elements.append(Spacer(1, 2*cm))
    curr_date = timezone_now().strftime('%d/%m/%Y')
    elements.append(Paragraph(f"<div align='right'>Fait à Yaoundé, le {curr_date}</div>", styles['Normal']))
    elements.append(Spacer(1, 0.5*cm))
    elements.append(Paragraph("<div align='right'><b>L'ADMINISTRATEUR ARRDELBEE</b></div>", styles['Normal']))

    # Construction du PDF
    doc.build(elements)
    pdf = buffer.getvalue()
    buffer.close()
    return pdf
