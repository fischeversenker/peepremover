from PIL import Image, ImageFile
import math

def save_bitmask(mask_data, name, size, format = 'png'):
    mask = Image.new('1', size)
    mask.putdata(mask_data)
    mask.save('%s.%s' % (name, format))

def load_images(count = 1, path = '.', format = 'png'):
    paths = ['%s.%s' % (n, format) for n in range(1, count+1)]
    names = ['%s' % n for n in range(1, count+1)]
    imgs = [Image.open('%s/%s.%s' % (path, n, format)) for n in range(1, count+1)]
    return zip(paths, names, imgs)

def different(pos, data_a, data_b, min=20):
    r_a, g_a, b_a = data_a[pos]
    r_b, g_b, b_b = data_b[pos]
    diff_r = abs(r_a - r_b) < min
    diff_g = abs(g_a - g_b) < min
    diff_b = abs(b_a - b_b) < min
    return diff_r or diff_g or diff_b

def print_square_mask(mask_data):
    width = math.sqrt(len(mask_data))
    print('\n--')
    for n in range(0, int(width)):
        zeroth = int(n*width)
        print(mask_data[zeroth], mask_data[zeroth+1], mask_data[zeroth+2], mask_data[zeroth+3])

def difference_masks(imgs):
    masks = []
    for p_a, n_a, i_a in imgs:
        d_a = i_a.getdata()
        w, h = i_a.size
        for p_b, n_b, i_b in imgs:
            # continue if comparing image to itself or lower
            if n_a <= n_b:
                break

            pix_difference = 0
            d_b = i_b.getdata()
            mask_diff = []
            for n in range(0, len(d_a)):
                if different(n, d_a, d_b):
                    pix_difference += 1
                    mask_diff.append(0)
                else:
                    mask_diff.append(1)

            if pix_difference > 0:
                mask = (n_a, n_b, mask_diff)
                save_bitmask(mask_diff, '%sx%s' % (n_a, n_b), i_a.size)
                masks.append(mask)
                # print_square_mask(mask_diff, w, h)

        # get rid of duplicates
        # TODO

    return masks

imgs = load_images(3, './marienplatz', 'jpg')
masks = difference_masks(imgs)
print(['%sx%s:\n' % (n_a, n_b) for n_a, n_b, mask in masks])
    
# for now: manually applying masks to images. Wrongly.
# figure out how to correspond mask to images...
# eventually: calculate best pixel from all avaiable ones.
# Basically figure out for each pixel which color matches most of the frame the best

finale_img = Image.new('RGB', imgs[0][2].size)
mask = Image.new('1', imgs[0][2].size)
# for n in range(0,len(imgs)):
mask.putdata(masks[0][2])
finale_img = Image.composite(finale_img, imgs[1][2], mask)
mask.putdata(masks[1][2])
# save_bitmask(masks[1][2], 'finaltest2', imgs[1][2].size)
finale_img = Image.composite(finale_img, imgs[1][2], mask)
mask.putdata(masks[2][2])
finale_img = Image.composite(finale_img, imgs[1][2], mask)

finale_img.save('final3a.png')
