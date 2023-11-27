from PIL import Image, ImageOps, ImageDraw, ImageFont
from time import time, sleep, process_time_ns
import os
# function to convert the current image into circular image
def CircularImage(img):
    mask = Image.new('L', img.size, 0)
    draw = ImageDraw.Draw(mask) 
    draw.ellipse((0, 0) + img.size, fill = 255)
    output = ImageOps.fit(img, mask.size, centering=(0.5, 0.5), method = Image.BOX)
    output.putalpha(mask)
    return output


# function to make a background layer - square or circle shaped
# can be used as border
def BackgroundImage(imagesize, bordersize = 5, backgroundcolor = "#ffffff", circularimage = False):
    newsize = (int(imagesize[0] + bordersize * 2), int(imagesize[1] + bordersize * 2))
    borderimage = Image.new("RGB", newsize, backgroundcolor)
    if circularimage:
        return CircularImage(borderimage)
    else:
        return borderimage

# add an image on another image at mentioned position
# can be used to insert an image on other image and make an image with background by placing the main image over the background generated
def ImageInsert(mainimage, subimage, X = 50, Y = 50, distx = None, disty = None, cropimage = None):
    mx, my = mainimage.size
    sx, sy = subimage.size
    if distx == None:
        distx = int((mx - sx)/(100/X))
    if disty == None:
        disty = int((mx - sx)/(100/Y))
    if mx < sx or my < sy:
        print("Error: Sub image size is more then main image size")
        return None
    # dx, dy = (mx - sx) / (100 / X), (my - sy) / (100 / Y)
    dx, dy = distx, disty
    mainimage, subimage = mainimage.convert("RGBA"), subimage.convert("RGBA")
    if cropimage == None:
        cropimage = subimage
    for i in range(sx):
        for j in range(sy):
            if cropimage.load()[i, j][3] > 0:
                try:
                    mainimage.load()[i + dx, j + dy] = subimage.load()[i, j]
                except:
                    print(f"Error: {mainimage.size, i + dx, j + dy, i, j, dx, dy}")
    return mainimage

def get_best_text_color(background_color):
    # Convert background color to grayscale
    grayscale_color = (0.299 * background_color[0] + 0.587 * background_color[1] + 0.114 * background_color[2]) / 255
    
    # Calculate contrast ratios with black and white text
    contrast_ratio_black = (grayscale_color + 0.05) / (0 + 0.05)
    contrast_ratio_white = (grayscale_color + 0.05) / (1 + 0.05)
    
    # Choose the text color with the highest contrast ratio
    print(contrast_ratio_black, contrast_ratio_white)
    if contrast_ratio_black > contrast_ratio_white:
        return (0, 0, 0)
    else:
        return (255, 255, 255)

def get_best_text_color_2(background_color):
    # Convert background color to grayscale
    grayscale_color = (0.299 * background_color[0] + 0.587 * background_color[1] + 0.114 * background_color[2]) / 255
    # Calculate contrast ratio for each potential text color
    best_contrast_ratio = 0
    best_text_color = None

    for r in range(256):
        for g in range(256):
            for b in range(256):
                text_color_luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255
                contrast_ratio = (grayscale_color + 0.05) / (text_color_luminance + 0.05)

                if contrast_ratio > best_contrast_ratio:
                    best_contrast_ratio = contrast_ratio
                    best_text_color = (r, g, b)

    return best_text_color

def get_best_text_color_3(background_color):
    # Convert background color to grayscale
    grayscale_color = (0.299 * background_color[0] + 0.587 * background_color[1] + 0.114 * background_color[2]) / 255

    # Calculate contrast ratio for each potential text color
    best_contrast_ratio = 0
    best_text_color = None

    for r in range(0, 256, 10):
        for g in range(0, 256, 10):
            for b in range(0, 256, 10):
                text_color_luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255
                contrast_ratio = (grayscale_color + 0.05) / (text_color_luminance + 0.05)

                if contrast_ratio > best_contrast_ratio:
                    best_contrast_ratio = contrast_ratio
                    best_text_color = (r, g, b)

    return best_text_color

def get_best_text_color_4(background_color):
    # Convert background color to grayscale
    grayscale_color = (0.299 * background_color[0] + 0.587 * background_color[1] + 0.114 * background_color[2]) / 255

    # Calculate contrast ratio for black and white text colors
    contrast_ratio_black = (grayscale_color + 0.05) / (0.05)
    contrast_ratio_white = (grayscale_color + 0.05) / (1.05)

    # Determine the best text color based on the contrast ratio
    if contrast_ratio_black > contrast_ratio_white:
        best_text_color = (0, 0, 0)  # Black text color
    else:
        best_text_color = (255, 255, 255)  # White text color

    return best_text_color


# function to add text to image of mentioned font
def TextInsert(image, Text, TextColor = "#777777", font = "noto_sans.ttf", FontSize = 16, X = 50, Y = 50, distx = None, disty = None, alignx = "center", aligny = "center", shrink = False, shrink_buffer = 100, stroke = 0):
    FontSize = int(FontSize)
    img = ImageDraw.Draw(image)
    
    Font = ImageFont.truetype(font, FontSize)
    W, H = image.size
    x, y = img.textsize(text = Text, font = Font)
    if shrink:
        while x > W - shrink_buffer:
            FontSize -= 5
            Font = ImageFont.truetype(font, FontSize)
            x, y = img.textsize(text = Text, font = Font)
    if distx == None:
        if alignx == "center":
            distx = int(((X/100) * W) - x/2)
        if alignx == "right":
            distx = int(((X/100) * W) - x)
        if alignx == "left":
            distx = int(((X/100) * W)) 
        if aligny == "center":
                disty = int(((Y/100) * H) - y/2)
        if aligny == "top":
            disty = int(((Y/100) * H) - y)
        if aligny == "bottom":
            disty = int(((Y/100) * H)) 
    else:
        if alignx == "center":
            distx = int(distx - x/2)
        if alignx == "right":
            distx = int(distx)
        if alignx == "left":
            distx = int(distx - x) 
        if aligny == "center":
                disty = int(disty - y/2)
        if aligny == "top":
            disty = int(disty - y)
        if aligny == "bottom":
            disty = int(disty) 
    center = distx + x // 2, disty + y // 2
    if TextColor == 'auto':
        # temp_colors = [image.getpixel((num, center[1])) for num in range(0, image.size[0], 100)]
        # tmp = [sum(col[ind] for col in temp_colors) for ind in range(len(temp_colors[0]))]
        # temp_color = tuple(int(color / len(temp_colors)) for color in tmp)
        # temp_color = tuple(int((255) - color / len(temp_colors)) for color in tmp)
        # print(temp_color, end = ' ')
        # TextColor = []
        # avg_color = int(sum(temp_color) / len(temp_color))
        # if avg_color > 196 or avg_color < 64:
        #     add_factor = 0
        # elif avg_color < 128:
        #     add_factor = -48
        # else:
        #     add_factor = 48
        # for color in temp_color:
        #     TextColor.append(max(min(color + add_factor, 255), 0))
        
        # TextColor = get_best_text_color_4(temp_color)
        # print(temp_color, TextColor)
        # TextColor = 224 if (sum(temp_color) / len(temp_color)) > 96 else 32
        TextColor = 225
        TextColor_ = 255 - 225
    else:
        TextColor_ = TextColor

    if stroke != 0:
        img.text((distx - stroke, disty - stroke), text = Text, fill = tuple(TextColor_ for _ in range(3)) if type(TextColor_) == int else TextColor_, font = Font)
        img.text((distx + stroke, disty - stroke), text = Text, fill = tuple(TextColor_ for _ in range(3)) if type(TextColor_) == int else TextColor_, font = Font)
        img.text((distx - stroke, disty + stroke), text = Text, fill = tuple(TextColor_ for _ in range(3)) if type(TextColor_) == int else TextColor_, font = Font)
        img.text((distx + stroke, disty + stroke), text = Text, fill = tuple(TextColor_ for _ in range(3)) if type(TextColor_) == int else TextColor_, font = Font)
    img.text((distx, disty), text = Text, fill = tuple(TextColor_ for _ in range(3)) if type(TextColor_) == int else TextColor_, font = Font)
    return image

def ProgressBar(image, X = 50, Y = 50, distx = None, disty = None, width = None, height = None, edge = False, align = "center", bordercolor = "#000000", innercolor = "#777777", edgecolor = "#dddddd"):

    draw = ImageDraw.Draw(image)   
    x, y = image.size
    tw, th = width / 2, height / 2
    dist_xc = x * (X/100)
    dist_yc = y * (Y/100)
    distx = (dist_xc - width/2)
    disty = (dist_yc - height/2)
    print(distx, disty)
    # if distx == None:
    #     distx = ((X/100) * x)
    # if disty == None:
    #     disty = ((Y/100) * y)
    # print(distx, disty)
    draw.ellipse((distx, disty, distx + height, disty + height), fill = innercolor)
    draw.rectangle((distx + height // 2, disty, distx + height / 2 + width, disty + height), fill = innercolor)
    draw.ellipse((distx + width, disty, distx + width + height, disty + height), fill = innercolor)
    if edge:
        draw.ellipse((distx + width, disty, distx + width + height, disty + height), fill = edgecolor)
    return image


def StatusImage(user_name, current_xp, total_xp, xp_level, xp_rank, coin_count, coin_rank, background = "bg.png", profile = "profile.png"):
    progress_percent = int(current_xp / total_xp * 100)
    image = Image.open(background)
    profile = Image.open(profile)
    ImageDraw.Draw(image).ellipse((52, 52, 264, 264), "#123456")
    profile = profile.resize((200, 200))
    image = ImageInsert(image, profile, distx = 58, disty = 58, cropimage = CircularImage(Image.new("RGB", profile.size)))
    ProgressBar(image, distx = 30, disty = 323, width = 900, height = 40, innercolor = "#456789")
    ProgressBar(image, distx = 33, disty = 326, width = 900, height = 34, innercolor = "#123456")
    ProgressBar(image, distx = 33, disty = 326, width = int(900 * (progress_percent / 100)), height = 34, innercolor = "#7edbf7")
    image, x, y = TextInsert(image, f"{current_xp} / {total_xp} XP", "#ffffff", FontSize = 34, alignx = "left", aligny = "top", distx = 950, disty = 310)
    image, x, y = TextInsert(image, f"{user_name}", "#ffffff", FontSize = 34, alignx = "right", aligny = "top", distx = 50, disty = 312)
    image, x, y = TextInsert(image, f"Rank #{xp_rank}", "#ffffff", FontSize = 40, alignx = "right", aligny = "bottom", distx = 300, disty = 180)
    image, x, y = TextInsert(image, f"Level {xp_level}", "#ffffff", FontSize = 40, alignx = "right", aligny = "bottom", distx = 300, disty = 100)
    # coin = Image.open("coin.png")
    # coin = coin.resize((60, 60))
    # image = ImageInsert(image, coin, distx = 300, disty = 100, cropimage = CircularImage(Image.new("RGB", coin.size)))
    # image, x, y = TextInsert(image, f"{coin_count}", "#FFF700", FontSize = 40, alignx = "right", aligny = "bottom", distx = 370, disty = 100)
    # image, x, y = TextInsert(image, f"Rank #{coin_rank}", "#FFF700", FontSize = 40, alignx = "right", aligny = "bottom", distx = 300, disty = 180)
    image.save("temp.png")
    return image
# start = process_time_ns()
# StatusImage(user_name = "mrunknown #9999", current_xp = 0, total_xp = 500, xp_level = 10, xp_rank = 10, coin_count = 100, coin_rank = 1, )
# print(f"Time taken: {(process_time_ns() - start) / 1000000000}")

def StatusImageHex(user_name, current_xp, total_xp, xp_level, xp_rank, coin_count, coin_rank, background = "bg.png", profile = "profile.png"):
    progress_percent = int(current_xp / total_xp * 100)
    image = Image.open("bg_2.png")
    profile = Image.open(profile)
    # ImageDraw.Draw(image).ellipse((52, 52, 264, 264), "#123456")
    profile = profile.resize((200, 200))
    bgimage1 = Image.new("RGB", (220, 220), "#3b2836")
    bgimage2 = Image.new("RGB", (210, 210), "#ffffff")
    image = ImageInsert(image, bgimage1, distx = 48, disty = 48, cropimage = Image.open("profile_trace.png").resize(bgimage1.size))
    image = ImageInsert(image, bgimage2, distx = 53, disty = 53, cropimage = Image.open("profile_trace.png").resize(bgimage2.size))
    # image = ImageInsert(image, profile, distx = 58, disty = 58, cropimage = Image.open("profile_trace.png").resize())
    image = ImageInsert(image, profile, distx = 58, disty = 58, cropimage = Image.open("profile_trace.png").resize(profile.size))
    ProgressBar(image, distx = 30, disty = 323, width = 900, height = 40, innercolor = "#aabbcc")
    ProgressBar(image, distx = 33, disty = 326, width = 900, height = 34, innercolor = "#123456")
    ProgressBar(image, distx = 33, disty = 326, width = int(900 * (progress_percent / 100)), height = 34, innercolor = "#7edbf7")
    image, x, y = TextInsert(image, f"{current_xp} / {total_xp} XP", "#ffffff", FontSize = 34, alignx = "left", aligny = "top", distx = 950, disty = 310)
    image, x, y = TextInsert(image, f"{user_name}", "#ffffff", FontSize = 34, alignx = "right", aligny = "top", distx = 50, disty = 312)
    image, x, y = TextInsert(image, f"Rank #{xp_rank}", "#ffffff", FontSize = 40, alignx = "right", aligny = "bottom", distx = 300, disty = 180)
    image, x, y = TextInsert(image, f"Level {xp_level}", "#ffffff", FontSize = 40, alignx = "right", aligny = "bottom", distx = 300, disty = 100)
    # coin = Image.open("coin.png")
    # coin = coin.resize((60, 60))
    # image = ImageInsert(image, coin, distx = 300, disty = 100, cropimage = CircularImage(Image.new("RGB", coin.size)))
    # image, x, y = TextInsert(image, f"{coin_count}", "#FFF700", FontSize = 40, alignx = "right", aligny = "bottom", distx = 370, disty = 100)
    # image, x, y = TextInsert(image, f"Rank #{coin_rank}", "#FFF700", FontSize = 40, alignx = "right", aligny = "bottom", distx = 300, disty = 180)
    image.save("temp.png")
    return image
# start = process_time_ns()
# StatusImageHex(user_name = "mrunknown #9999", current_xp = 0, total_xp = 500, xp_level = 10, xp_rank = 10, coin_count = 100, coin_rank = 1, )
# print(f"Time taken: {(process_time_ns() - start) / 1000000000}")

def welcome_image(user, profileimage_path):
    # saving user's profile image
    image = Image.open(os.path.join("Welcome", "bg.png"))
    # setting the width of user name based on the length of the name
    image, x, y = TextInsert(image, f"{user} Just joined the server!", FontSize = 46, X = 50, Y = 75, shrink = True, TextColor = "#ffffff")
    image, x, y = TextInsert(image, f"member #{user.guild.member_count}", FontSize = 36, X = 50, Y = 85, shrink = True, TextColor = "#dddddd")
    profile = Image.open(profileimage_path).resize((256, 256))
    p, q = profile.size
    bgimage = Image.new("RGB", (p + 10, q + 10), "#ffffff")
    image = ImageInsert(image, bgimage, distx = image.size[0] // 2 - bgimage.size[0] // 2, disty = 55, cropimage = Image.open("profile_trace.png").resize(bgimage.size))
    # image = ImageInsert(image, profile, distx = 58, disty = 58, cropimage = Image.open("profile_trace.png").resize())
    image = ImageInsert(image, profile, distx = image.size[0] // 2 - profile.size[0] // 2, disty = 60, cropimage = Image.open("profile_trace.png").resize(profile.size))
    image.save(os.path.join("Welcome", "welcomeimage.png"))




