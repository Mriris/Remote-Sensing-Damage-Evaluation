import cv2

def resize_(srcImg, width, height):

    image = srcImg
    h, w, c = image.shape

    top, bottom, left, right = (0, 0, 0, 0)


    long_side = max(h, w)
    if h >= w:
        ratio = float(height) / long_side

    elif h < w:
        ratio = float(width) / long_side

    # resize the long side and add black border to the both size of the short side
    resi = cv2.resize(image, (0, 0), fx=ratio, fy=ratio, interpolation=cv2.INTER_NEAREST)

    res_height, res_width, res_c = resi.shape

    if h >= w:
        if res_width < width:
            dw = width - res_width
            left = dw // 2
            right = dw - left

    elif h < w:
        if res_height < height:
            dh = height - res_height
            top = dh // 2
            bottom = dh - top

    BLACK = [114, 114, 114]
    dstImg = cv2.copyMakeBorder(resi, top, bottom, left, right, cv2.BORDER_CONSTANT, value=BLACK)

    return dstImg
