from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from civ_game.technology import TECHNOLOGIES
from civ_game.policy import POLICIES
from civ_game.buildings import BUILDINGS
from civ_game.units import UNITS
from civ_game.civilization_traits import CIVILIZATION_TRAITS

def generate_game_documentation():
    doc = SimpleDocTemplate("Game_Documentation.pdf")
    styles = getSampleStyleSheet()
    story = []

    # Title
    story.append(Paragraph("Civilization Game Documentation", styles['h1']))
    story.append(Spacer(1, 12))

    # Introduction
    story.append(Paragraph("Introduction", styles['h2']))
    intro_text = """
    This document provides a comprehensive guide to the Civilization game. The objective is to
    lead your chosen civilization from the ancient era to the modern age, competing against
    other civilizations for world dominance. Victory can be achieved through various means,
    including military conquest, technological superiority, and cultural influence.
    """
    story.append(Paragraph(intro_text, styles['Normal']))
    story.append(PageBreak())

    # Civilizations
    story.append(Paragraph("Civilizations", styles['h2']))
    for civ_key, civ_data in CIVILIZATION_TRAITS.items():
        story.append(Paragraph(civ_data['name'], styles['h3']))
        story.append(Paragraph(f"<b>Description:</b> {civ_data['description']}", styles['Normal']))
        story.append(Paragraph("<b>Advantages:</b>", styles['Normal']))
        for advantage in civ_data['advantages']:
            story.append(Paragraph(f"- {advantage}", styles['Normal']))
        story.append(Paragraph("<b>Disadvantages:</b>", styles['Normal']))
        for disadvantage in civ_data['disadvantages']:
            story.append(Paragraph(f"- {disadvantage}", styles['Normal']))
        story.append(Spacer(1, 12))
    story.append(PageBreak())

    # Technology Tree
    story.append(Paragraph("Technology Tree", styles['h2']))
    for tech_key, tech_data in TECHNOLOGIES.items():
        story.append(Paragraph(tech_data['name'], styles['h3']))
        story.append(Paragraph(f"<b>Cost:</b> {tech_data['cost']} research points", styles['Normal']))
        story.append(Paragraph(f"<b>Description:</b> {tech_data['description']}", styles['Normal']))
        if tech_data.get('requires'):
            story.append(Paragraph(f"<b>Requires:</b> {', '.join(tech_data['requires'])}", styles['Normal']))
        story.append(Spacer(1, 12))
    story.append(PageBreak())

    # Economic Policies
    story.append(Paragraph("Economic Policies", styles['h2']))
    for policy_key, policy_data in POLICIES.items():
        story.append(Paragraph(policy_data['name'], styles['h3']))
        story.append(Paragraph(f"<b>Description:</b> {policy_data['description']}", styles['Normal']))
        story.append(Paragraph(f"<b>Requires:</b> {policy_data['requires_tech']}", styles['Normal']))
        story.append(Spacer(1, 12))
    story.append(PageBreak())

    # Buildings
    story.append(Paragraph("Buildings", styles['h2']))
    for building_key, building_data in BUILDINGS.items():
        story.append(Paragraph(building_data['name'], styles['h3']))
        cost_str = ", ".join([f"{v} {k}" for k, v in building_data['cost'].items()])
        story.append(Paragraph(f"<b>Cost:</b> {cost_str}", styles['Normal']))
        story.append(Paragraph(f"<b>Requires:</b> {building_data['requires_tech']}", styles['Normal']))
        story.append(Paragraph(f"<b>Description:</b> {building_data['description']}", styles['Normal']))
        story.append(Spacer(1, 12))
    story.append(PageBreak())

    # Units
    story.append(Paragraph("Units", styles['h2']))
    for unit_key, unit_data in UNITS.items():
        story.append(Paragraph(unit_data['name'], styles['h3']))
        cost_str = ", ".join([f"{v} {k}" for k, v in unit_data['cost'].items()])
        story.append(Paragraph(f"<b>Cost:</b> {cost_str}", styles['Normal']))
        story.append(Paragraph(f"<b>Requires:</b> {unit_data['requires_tech']}", styles['Normal']))
        story.append(Paragraph(f"<b>Combat Strength:</b> {unit_data['combat_strength']}", styles['Normal']))
        story.append(Paragraph(f"<b>Description:</b> {unit_data['description']}", styles['Normal']))
        story.append(Spacer(1, 12))

    doc.build(story)
    print("Detailed game documentation generated successfully.")

if __name__ == "__main__":
    generate_game_documentation()