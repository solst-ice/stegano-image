from PIL import Image

def extract_copyright_steganography(image_path, length=70):  # Default length is 50 chars
    """Extract hidden copyright text from image"""
    # Open image
    img = Image.open(image_path)
    pixels = list(img.getdata())
    
    # Extract binary message
    binary_message = ''
    for i in range(length * 8):  # Each character needs 8 bits
        if i >= len(pixels):
            break
        if isinstance(pixels[i], int):  # Grayscale
            binary_message += str(pixels[i] & 1)
        else:  # RGB or RGBA
            binary_message += str(pixels[i][0] & 1)
    
    # Convert binary to text
    message = ''
    for i in range(0, len(binary_message), 8):
        byte = binary_message[i:i+8]
        try:
            message += chr(int(byte, 2))
        except ValueError:
            break
            
    return message

# Example usage
image_path = "GgO-RwwXIAAsBbl.png"  # Replace with your image name
extracted_text = extract_copyright_steganography(image_path)
print(f"Extracted text: {extracted_text}")