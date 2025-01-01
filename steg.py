from PIL import Image

def embed_copyright_steganography(image_path, copyright_text):
    """Embed copyright text into image using steganography"""
    # Open image
    img = Image.open(image_path)
    pixels = list(img.getdata())
    
    # Convert text to binary
    binary_copyright = ''.join(format(ord(char), '08b') for char in copyright_text)
    
    if len(binary_copyright) > len(pixels):
        raise ValueError("Image too small to embed message")
    
    # Embed data by modifying least significant bits
    new_pixels = []
    binary_index = 0
    
    for pixel in pixels:
        if isinstance(pixel, int):  # Grayscale
            new_pixel = pixel & ~1 | int(binary_copyright[binary_index])
            new_pixels.append(new_pixel)
        else:  # RGB or RGBA
            new_pixel = list(pixel)
            if binary_index < len(binary_copyright):
                new_pixel[0] = pixel[0] & ~1 | int(binary_copyright[binary_index])
            new_pixels.append(tuple(new_pixel))
        binary_index = (binary_index + 1) % len(binary_copyright)
    
    # Create new image with modified pixels
    new_img = Image.new(img.mode, img.size)
    new_img.putdata(new_pixels)
    
    output_path = "steg_" + image_path
    new_img.save(output_path, "PNG")
    return output_path

def extract_copyright_steganography(image_path, message_length):
    """Extract hidden copyright text from image"""
    # Open image
    img = Image.open(image_path)
    pixels = list(img.getdata())
    
    # Extract binary message
    binary_message = ''
    for i in range(message_length * 8):
        if isinstance(pixels[i], int):  # Grayscale
            binary_message += str(pixels[i] & 1)
        else:  # RGB or RGBA
            binary_message += str(pixels[i][0] & 1)
    
    # Convert binary to text
    message = ''
    for i in range(0, len(binary_message), 8):
        byte = binary_message[i:i+8]
        message += chr(int(byte, 2))
    
    return message

# Example usage
if __name__ == "__main__":
    input_image = "image.png"
    copyright_text = r"X5O!P%@AP[4\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*" # Your copyright text here
    
    # Embed copyright
    steg_image = embed_copyright_steganography(input_image, copyright_text)
    print(f"Created steganographic image: {steg_image}")
    
    # Verify embedding
    extracted_text = extract_copyright_steganography(steg_image, len(copyright_text))
    print(f"Extracted copyright text: {extracted_text}")
    
    # Verify they match
    if extracted_text == copyright_text:
        print("Success! Copyright text was embedded and extracted correctly")
    else:
        print("Warning: Extracted text doesn't match original")