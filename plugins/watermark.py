# plugins/watermark.py

from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from config import FEATURE_VAULT

class WatermarkPlugin:
    """
    Watermark plugin: Adds watermark text to images before uploading.
    """

    def __init__(self):
        self.enabled = FEATURE_VAULT  # Use FEATURE_VAULT or create FEATURE_WATERMARK flag

    async def add_watermark(self, image_bytes: bytes, watermark_text: str = "AdvancedFileSharingBot") -> bytes:
        """
        Add watermark to an image and return new image bytes.
        """
        if not self.enabled:
            return image_bytes  # Return original if feature disabled

        # Open image
        img = Image.open(BytesIO(image_bytes)).convert("RGBA")

        # Create overlay for watermark
        txt_overlay = Image.new("RGBA", img.size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(txt_overlay)

        # Font size relative to image
        font_size = max(20, img.width // 20)
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            font = ImageFont.load_default()

        # Position watermark at bottom-right
        text_width, text_height = draw.textsize(watermark_text, font=font)
        position = (img.width - text_width - 10, img.height - text_height - 10)

        # Draw watermark
        draw.text(position, watermark_text, fill=(255, 255, 255, 128), font=font)

        # Merge overlay with original image
        watermarked = Image.alpha_composite(img, txt_overlay).convert("RGB")

        # Save to bytes
        output = BytesIO()
        watermarked.save(output, format="JPEG")
        return output.getvalue()
