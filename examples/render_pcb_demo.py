"""
Sample PCB generator demo script to create a minimal PCB layout preview with custom silkscreen text.
"""

from PIL import Image, ImageDraw, ImageFont

def generate_pcb(output_path="HRL_PCB_Preview.png", text="HRL"):
    width, height = 1400, 900
    img = Image.new("RGB", (width, height), color=(15, 17, 20))
    draw = ImageDraw.Draw(img)

    try:
        title_font = ImageFont.truetype("arial.ttf", 36)
        font = ImageFont.truetype("arial.ttf", 160)
        subfont = ImageFont.truetype("arial.ttf", 26)
        meta_font = ImageFont.truetype("consola.ttf", 20)
    except:
        font = ImageFont.load_default()
        title_font = font
        subfont = font
        meta_font = font

    draw.text((700, 60), "CADENCE ALLEGRO X - PCB PREVIEW", fill=(220, 220, 220), font=title_font, anchor="mm")
    draw.text((700, 100), "Project: D:\\CadenceProjects\\HRL_Test\\HRL_board.brd", fill=(120, 140, 160), font=meta_font, anchor="mm")

    # PCB Board Outline (Layer: Board Geometry / Outline)
    pcb_rect = [200, 150, 1200, 750]
    draw.rounded_rectangle(pcb_rect, radius=35, fill=(16, 58, 32), outline=(212, 175, 55), width=5)

    # Corner Mounting Holes (with Gold Annular Rings)
    for cx, cy in [(270, 220), (1130, 220), (270, 680), (1130, 680)]:
        draw.ellipse([cx-32, cy-32, cx+32, cy+32], fill=(212, 175, 55), outline=(160, 130, 35), width=3)
        draw.ellipse([cx-18, cy-18, cx+18, cy+18], fill=(15, 17, 20))

    # Decorative Copper Traces & Buses
    draw.line([(350, 220), (500, 220), (600, 320)], fill=(28, 92, 52), width=8)
    draw.line([(1050, 220), (900, 220), (800, 320)], fill=(28, 92, 52), width=8)
    draw.line([(350, 680), (500, 680), (600, 580)], fill=(28, 92, 52), width=8)
    draw.line([(1050, 680), (900, 680), (800, 580)], fill=(28, 92, 52), width=8)

    # Center Silkscreen Box
    draw.rounded_rectangle([380, 290, 1020, 610], radius=20, outline=(245, 245, 245), width=4)

    # Silkscreen Printed Text
    draw.text((700, 410), text, fill=(255, 255, 255), font=font, anchor="mm")
    draw.text((700, 520), f"DESIGN: {text} PCB TEST", fill=(255, 255, 255), font=subfont, anchor="mm")
    draw.text((700, 560), "TOP SILKSCREEN (SILK_TOP) | 2-LAYER FR-4", fill=(200, 220, 200), font=meta_font, anchor="mm")

    # Test Pin Headers (Gold Plated)
    for i in range(10):
        px = 475 + i * 50
        draw.rectangle([px-12, 200, px+12, 240], fill=(218, 180, 60), outline=(150, 120, 30), width=2)
        draw.ellipse([px-6, 214, px+6, 226], fill=(15, 17, 20))
        # bottom header
        draw.rectangle([px-12, 660, px+12, 700], fill=(218, 180, 60), outline=(150, 120, 30), width=2)
        draw.ellipse([px-6, 674, px+6, 686], fill=(15, 17, 20))

    img.save(output_path)
    print(f"Generated {output_path} successfully!")

if __name__ == "__main__":
    generate_pcb()
