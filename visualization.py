import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from scipy.interpolate import spline
import glob, os

import cufflinks as cf
from plotly.offline import init_notebook_mode, plot, iplot, download_plotlyjs
init_notebook_mode(connected=True)
cf.go_offline()

def print_KV7(file_name_1, file_name_2, n):
    #input data
    imcore = pd.read_table(file_name_1, names = [46.25, 90, 133.75, 177.5, 221.25, 265, 308.75])
    smaz = pd.read_table(file_name_2, names = [52.2015625, 95.9515625, 139.7015625, 183.4515625, 227.2015625, 270.9515625, 314.7015625])

    sns.set()
    fig = plt.figure()
    ax = fig.add_axes([0.15,0.1,0.8,0.8])
    #ImCore steps
    ax.plot(imcore.mean(), imcore.columns, color = 'red',marker='o', linestyle = 'steps', lw = '0.2')

    ynew = np.linspace(imcore.columns[0],imcore.columns[6],100)
    ImCore_smooth = spline(imcore.columns ,imcore.mean(),ynew)
    #ImCore spline
    ax.plot(ImCore_smooth, ynew, color = 'red', lw = '2', label='ImCore')
    #Smaz steps
    ax.plot(smaz.mean(), smaz.columns, color = 'black',marker='o', linestyle = 'steps', lw = '0.2')

    ynew2 = np.linspace(smaz.columns[0],smaz.columns[6],100)
    smaz_smooth = spline(smaz.columns ,smaz.mean(),ynew2)
    #Smaz spline
    ax.plot(smaz_smooth, ynew2, color = 'black', lw = '2', label='Smaz')
    #legend
    ax.legend(loc='best')
    ax.set_title('KV7')
    ax.set_ylabel('Height, cm')

    fig.savefig('KV7_'+str(n)+'.png', dpi = 300)

def print_KQ_map(ImC_KV = False, ImC_KQ = False, smaz_KV = False, smaz_KQ =False, point_num = 0):
    #input data
    if   ImC_KQ is False:
        dataset3 = pd.read_table(ImC_KV, names=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24]).mean(axis=1)
    elif ImC_KV is False:
        dataset3 = pd.read_table(ImC_KQ, names=['KQ'])['KQ']

    if   smaz_KQ is False:
        dataset2 = pd.read_table(smaz_KV, names=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24]).mean(axis=1)
    elif smaz_KV is False:
        dataset2 = pd.read_table(smaz_KQ, names=['KQ'])['KQ']


    # -*- coding: utf-8 -*-
    #
    # draws a 360 deg. map read from file
    from PIL import Image, ImageDraw, ImageFont
    #
    mm = 3.7795  # 1mm~3.7795 pxl
    #    fonts setup
    isocp = 'isocpeui.ttf'
    font = ImageFont.truetype(isocp, 26)
    font_legend = ImageFont.truetype(isocp, 41)
    font_lesser = ImageFont.truetype(isocp, 45)
    font_large = ImageFont.truetype(isocp, 40)
    #    image dimensions
    field_x = 770 * mm
    field_y = 700 * mm
    side = 30 * mm  # hexagon side length
    bottom_left = (270 * mm, 630 * mm)  # coordinates of the top point of the bottom left cell
    image = Image.new("RGB", (int(field_x), int(field_y)), (255, 255, 255, 255))
    draw = ImageDraw.Draw(image)
    #
    ###########################################################
    #                    <INPUT>
    ###########################################################
    # legend
    leg_str1 = "БИПР"
    leg_str2 = "Voyage"
    leg_str3 = "DYN3D"
    leg_str4 = "Арена"
    # output filename
    output_fn = "output.png"
    # input filenames
    input_fn1 = "1.txt"
    input_fn2 = "2.txt"
    input_fn3 = "3.txt"
    input_fn4 = "4.txt"
    input_fn5 = '5.txt'
    years = 'years.txt'
    ##########################################################
    #                   </INPUT>
    ##########################################################
    rows_south = [10, 11, 12, 13, 14]  # cells in row (bottom half)
    rows_north = [13, 12, 11, 10, 9]  # cells in row (top half)

    #
    #    calculation of a single cell points coordinates from side and top point
    def single_hex(start, side):
        coordinates = []
        coordinates.append(start)  # starts from the top point and goes clockwise
        coordinates.append(tuple([start[0] + (((side ** 2) - (0.5 * side) ** 2) ** 0.5), start[1] + 0.5 * side]))
        coordinates.append(tuple([start[0] + (((side ** 2) - (0.5 * side) ** 2) ** 0.5), start[1] + 1.5 * side]))
        coordinates.append(tuple([start[0], start[1] + 2 * side]))
        coordinates.append(tuple([start[0] - (((side ** 2) - (0.5 * side) ** 2) ** 0.5), start[1] + 1.5 * side]))
        coordinates.append(tuple([start[0] - (((side ** 2) - (0.5 * side) ** 2) ** 0.5), start[1] + 0.5 * side]))
        return coordinates

    #
    #    calculation of top points for 163 cells
    def startpoints(bottom_left, side):
        half_width = ((side ** 2) - (0.5 * side) ** 2) ** 0.5
        starts = []
        starts.append(bottom_left)
        for i in range(5):
            starts.append(tuple([bottom_left[0] + 2 * (i + 1) * half_width, bottom_left[1]]))
        starts.append(tuple([bottom_left[0] - 3 * half_width, bottom_left[1] - 1.5 * side]))
        localstart = tuple([bottom_left[0] - 3 * half_width, bottom_left[1] - 1.5 * side])
        for i in range(8):
            starts.append(
                tuple([(bottom_left[0] - 3 * half_width) + 2 * (i + 1) * half_width, bottom_left[1] - 1.5 * side]))
        for i in rows_south:
            localstart = tuple([localstart[0] - half_width, localstart[1] - 1.5 * side])
            starts.append(localstart)
            for j in range(i - 1):
                starts.append(tuple([localstart[0] + 2 * (j + 1) * half_width, localstart[1]]))
        starts.append(tuple([bottom_left[0] - 7 * half_width, bottom_left[1] - 10.5 * side]))
        for i in range(12):
            starts.append(
                tuple([bottom_left[0] - 7 * half_width + 2 * (i + 1) * half_width, bottom_left[1] - 10.5 * side]))
        starts.append(tuple([bottom_left[0] - 8 * half_width, bottom_left[1] - 12 * side]))
        for i in range(13):
            starts.append(
                tuple([bottom_left[0] - 8 * half_width + 2 * (i + 1) * half_width, bottom_left[1] - 12 * side]))
        localstart = tuple([bottom_left[0] - 8 * half_width, bottom_left[1] - 12 * side])
        for i in rows_north:
            localstart = tuple([localstart[0] + half_width, localstart[1] - 1.5 * side])
            starts.append(localstart)
            for j in range(i - 1):
                starts.append(tuple([localstart[0] + 2 * (j + 1) * half_width, localstart[1]]))
        starts.append(tuple([bottom_left[0], bottom_left[1] - 21 * side]))
        for i in range(5):
            starts.append(tuple([bottom_left[0] + 2 * (i + 1) * half_width, bottom_left[1] - 21 * side]))
        return starts

    def startpoints_leg(bottom_left, side):
        half_width = ((side ** 2) - (0.5 * side) ** 2) ** 0.5
        starts = []
        starts.append(tuple([bottom_left[0] - 1103, -1400 + bottom_left[1] - 8.5 * half_width]))
        starts.append(tuple([bottom_left[0] - 1103, -1400 + bottom_left[1] - 8.5 * half_width + 2.0 * side]))
        starts.append(tuple([bottom_left[0] - 1103, -1400 + bottom_left[1] - 8.5 * half_width + 2 * 2.0 * side]))
        starts.append(tuple([bottom_left[0] - 1103, -1400 + bottom_left[1] - 8.5 * half_width + 3 * 2.0 * side]))
        return starts

    #    assemble a list of all required coordinates for 163 cells
    def hex_coordinates(starts):
        res = []
        for startpoint in starts:
            res.append(single_hex(startpoint, side))
        return res

    #
    #    10th cr bank marks
    def cr_starts(starts):
        crstrt = []
        for i in [30, 51, 57, 105, 111, 132]:
            crstrt.append(tuple([starts[i][0], starts[i][1] + 2 * mm]))
        return crstrt

    #
    def cr_bank(starts):
        res = []
        for startpoint in starts:
            res.append(single_hex(startpoint, side - 2 * mm))
        return res

    #
    #    calculation of text box coordinates for enumeration
    def enumeration_startpoints(starts):
        x_indent = 6 * mm
        y_indent = 4 * mm
        enum_starts = []
        for startpoint in starts:
            enum_starts.append(tuple([startpoint[0] - x_indent, startpoint[1] + y_indent]))
        return enum_starts

    #
    #    four left entries in a cell
    def left_entries(starts):
        x_indent = 22 * mm
        y_indent = 29 * mm
        step = 10 * mm
        entry1_starts, entry2_starts, entry3_starts, entry4_starts = [], [], [], []
        for startpoint in starts:
            entry1_starts.append(tuple([startpoint[0] - x_indent, startpoint[1] + y_indent]))
            entry2_starts.append(tuple([startpoint[0] - x_indent, startpoint[1] + y_indent + step]))
            entry3_starts.append(tuple([startpoint[0] - x_indent, startpoint[1] + y_indent + 2 * step]))
            entry4_starts.append(tuple([startpoint[0] - x_indent, startpoint[1] + y_indent + 3 * step]))
        return [entry1_starts, entry2_starts, entry3_starts, entry4_starts]

    #
    #    four right entries in a cell
    def right_entries(starts):
        x_indent = 4 * mm
        y_indent = 29 * mm
        step = 10 * mm
        entry1_starts, entry2_starts, entry3_starts, entry4_starts = [], [], [], []
        for startpoint in starts:
            entry1_starts.append(tuple([startpoint[0] + x_indent, startpoint[1] + y_indent]))
            entry2_starts.append(tuple([startpoint[0] + x_indent, startpoint[1] + y_indent + step]))
            entry3_starts.append(tuple([startpoint[0] + x_indent, startpoint[1] + y_indent + 2 * step]))
            entry4_starts.append(tuple([startpoint[0] + x_indent, startpoint[1] + y_indent + 3 * step]))
        return [entry1_starts, entry2_starts, entry3_starts, entry4_starts]

    #    four right entries in a cell
    def center_entries(starts):
        x_indent = 12 * mm
        y_indent = 15 * mm
        step = 9 * mm
        entry1_starts, entry2_starts, entry3_starts, entry4_starts = [], [], [], []
        for startpoint in starts:
            entry1_starts.append(tuple([startpoint[0] - x_indent, startpoint[1] + y_indent]))
            entry2_starts.append(tuple([startpoint[0] - 0.5 * x_indent, startpoint[1] + 1.2 * y_indent + step]))
            entry3_starts.append(tuple([startpoint[0] - x_indent, startpoint[1] + 1.2 * y_indent + 2 * step]))
            entry4_starts.append(tuple([startpoint[0] - 0.5 * x_indent, startpoint[1] + 1.3 * y_indent + 3 * step]))
        return [entry1_starts, entry2_starts, entry3_starts, entry4_starts]

    def center2_entries(starts):
        x_indent = 12 * mm
        y_indent = 15 * mm
        step = 13 * mm
        entry1_starts, entry2_starts, entry3_starts, entry4_starts = [], [], [], []
        for startpoint in starts:
            entry1_starts.append(tuple([startpoint[0] - x_indent, startpoint[1] + y_indent]))
            entry2_starts.append(tuple([startpoint[0] - 0.5 * x_indent, startpoint[1] + 1.2 * y_indent + step]))
            entry3_starts.append(tuple([startpoint[0] - x_indent, startpoint[1] + 1.2 * y_indent + 2 * step]))
            entry4_starts.append(tuple([startpoint[0] - 0.5 * x_indent, startpoint[1] + 1.3 * y_indent + 3 * step]))
        return [entry1_starts, entry2_starts, entry3_starts, entry4_starts]

    #
    shaded = [0, 1, 2, 3, 4, 5, 7, 8, 9, 10, 11, 12, 17, 18, 19, 20, 21, 28, 29, 30, 31, 40, 41, 42, 53, 54, 67,
              81, 82, 83, 84, 85, 86, 87, 96, 97, 98, 99, 100, 101, 110, 111, 112, 113, 114, 123, 124, 125, 126, 135,
              136, 137, 146, 147, 156,
              88, 89, 90, 91, 92, 93, 94, 102, 103, 104, 105, 106, 107, 115, 116, 117, 118, 119, 127, 128, 129, 130,
              138, 139, 140, 148, 149]

    #

    #    draw hexagonal cells
    def cells_cr(coords):
        for coord_list in coords:
            draw.polygon(coord_list, outline='black')

    def cells(coords, dev):

        # red=hex(255)
        # green=hex(255/10)
        # print (red[2:])
        for i in range(len(dev)):
            red = int('{:3.0f}'.format(85 * dev[i]))
            green = int('{:3.0f}'.format(-102 * dev[i] + 561))

            print(red, green, red + green)
            if int(red) > 255:
                red = 255
            elif red < 0:
                red = 0
            if int(green) < 0:
                green = 0
            elif int(green) > 255:
                green = 255
            r = hex(red)[2:]
            g = hex(green)[2:]

            if len(r) < 2:
                r = '0' + r
            if len(g) < 2:
                g = '0' + g
            draw.polygon(coords[i], outline='black', fill='#' + r + g + '00')
            # if dev[i]>5:
            #    draw.polygon(coords[i], outline='black', fill='#'+r+g'00')
            # if dev[i]>2 and dev[i]<=5:
            #    draw.polygon(coords[i], outline='black', fill='#ff9999')
            # if dev[i]>1 and dev[i]<=2:
            #    draw.polygon(coords[i], outline='black', fill='#ffff66')
            # if dev[i]<=1 :
            #    draw.polygon(coords[i], outline='black', fill='#66ff66')
            # else:
            #    draw.polygon(coords[i], outline='black')

    def cells_leg(coords):
        for i in range(len(coords)):
            if i == 1:
                draw.polygon(coords[i], outline='black', fill='#f3f3f3')
            if i == 2:
                draw.polygon(coords[i], outline='black', fill='#d8d8d8')
            if i == 3:
                draw.polygon(coords[i], outline='black', fill='#b9b9b9')
            else:
                draw.polygon(coords[i], outline='black')

    #
    #    enumerate cells
    def numbers(starts):
        nums = range(1, 164)
        i = -1
        for startpoint in starts:
            i += 1
            if len(str(nums[i])) == 1:
                draw.text(startpoint, '  ' + str(nums[i]), font=font, fill='black')
            elif len(str(nums[i])) == 2:
                draw.text(startpoint, ' ' + str(nums[i]), font=font, fill='black')

            else:
                draw.text(startpoint, str(nums[i]), font=font, fill='black')

    #
    #    read data
    def readdata(fname):
        res, res1 = [], []
        with open(fname, 'r') as inp:
            for line in inp:
                lisp = line.split()
                if len(lisp) > 1:
                    res.append(float(line.split()[0]))
                    res1.append(float(line.split()[1]))

        return [res, res1]

    #    read data
    def read_map(fname):
        fa = []
        res, res1 = [], []
        with open(fname, 'r') as inp:
            for line in inp:
                res.append(line.split())
        res.reverse()
        for line in res:
            for fuel in line:
                fa.append(fuel)
        return fa

    #
    #    plot data from dataset
    def plotdata(dataset, coords):
        i = 0
        for startpoint in coords:
            draw.text(startpoint, dataset[i], font=font_large, fill='black')
            i += 1

    #
    #    dataset files, enumerated from top left entry

    dataset1 = read_map('map.imcore')
    print(len(dataset1))

    dataset4 = ['{: ^6.2f}'.format((dataset3[i] - dataset2[i]) / dataset2[i] * 100) for i in range(0, len(dataset2))]

    dataset2 = ['{: ^6.2f}'.format(dataset2[i]) for i in range(len(dataset2))]
    dataset3 = ['{: ^6.2f}'.format(dataset3[i]) for i in range(len(dataset3))]

    #
    #    draw a legend
    def legend():
        half_width = ((side ** 2) - (0.5 * side) ** 2) ** 0.5
        lside = 1.5 * side
        lstart = tuple([(bottom_left[0] - 7 * half_width) - 100, (bottom_left[1] - 22 * side) + 200])
        x_num = 10
        y_num = 20
        x_dat = 100
        y_dat = 150
        x_datr = 0
        dstep = 70
        draw.polygon(single_hex(lstart, lside), outline='black')
        draw.text(tuple([lstart[0] - x_num, lstart[1] + y_num]), '№', font=font, fill='black')
        centry0 = tuple([lstart[0] - 40, lstart[1] + 40])
        centry1 = tuple([lstart[0] - 80, lstart[1] + 80])
        centry2 = tuple([lstart[0] - 115, lstart[1] + 230])
        centry3 = tuple([lstart[0] - 40, lstart[1] + 250])
        lentry1 = tuple([lstart[0] - 130, lstart[1] + 170])
        lentry2 = tuple([lstart[0] - 100, lstart[1] + 130])
        rentry1 = tuple([lstart[0] + 15, lstart[1] + 170])
        rentry2 = tuple([lstart[0] + 40, lstart[1] + 130])
        #
        draw.text(lentry1, "набор1", font=font_legend, fill='black')
        draw.text(rentry1, "набор2", font=font_legend, fill='black')
        draw.text(lentry2, "kq", font=font_legend, fill='black')
        draw.text(rentry2, "kq", font=font_legend, fill='black')
        draw.text(centry0, "Кассеты", font=ImageFont.truetype(isocp, 25), fill='black')
        draw.text(centry2, "Отклонение,%", font=font_legend, fill='black')
        draw.text(centry1, "тип ТВС", font=font_legend, fill='black')

    #
    #
    cells(hex_coordinates(startpoints(bottom_left, side)), [abs(float(x)) for x in dataset4])
    cells_cr(cr_bank(cr_starts(startpoints(bottom_left, side))))
    numbers(enumeration_startpoints(startpoints(bottom_left, side)))
    plotdata(dataset1, center_entries(startpoints(bottom_left, side))[0])
    plotdata(dataset2, left_entries(startpoints(bottom_left, side))[0])
    plotdata(dataset3, right_entries(startpoints(bottom_left, side))[0])
    plotdata(dataset4, center2_entries(startpoints(bottom_left, side))[2])

    legend()
    # cells_leg(hex_coordinates(startpoints_leg(bottom_left, side)))
    # plotdata([' ТВС' for x in range(len(startpoints_leg(bottom_left, side)))],center_entries(startpoints_leg(bottom_left, side))[0])
    # plotdata([' 1',' 2',' 3',' 4'],center_entries(startpoints_leg(bottom_left, side))[1])
    # plotdata([' год' for x in range(len(startpoints_leg(bottom_left, side)))],center_entries(startpoints_leg(bottom_left, side))[2])

    #
    del draw
    image.save('KQ_'+str(point_num)+'.png')

def print_AO(file_name1, file_name2):
    IC_AO = pd.read_table(file_name1, names=['ImCore'])
    smaz_AO = pd.read_table(file_name2, names=['smaz'])

    sns.set()
    fig = plt.figure()
    ax = fig.add_axes([0.15,0.15,0.8,0.8])

    ax.plot(IC_AO.index.values, IC_AO['ImCore'], color='red', lw='2', label = 'ImCore')
    ax.plot(smaz_AO.index.values, smaz_AO['smaz'], color='black', lw='2', label='smaz')
    ax.legend(loc='best')
    ax.set_title('Axial offset')
    ax.set_ylabel('AO, %')
    ax.set_xlabel('day')

    fig.savefig('AO.png', dpi = 300)

def print_Bor(file_name1, file_name2):
    IC_bor = pd.read_table(file_name1, names='1')
    smaz_bor = pd.read_table(file_name2, names='1')

    sns.set()
    fig = plt.figure()
    ax = fig.add_axes([0.15,0.15,0.8,0.8])

    ax.plot(IC_bor.index.values, IC_bor['1'], color='blue', lw='2', label = 'ImCore')
    ax.plot(smaz_bor.index.values, smaz_bor['1'], color='black', lw='2', label='smaz')
    ax.legend(loc='best')
    ax.set_title('bor')
    ax.set_ylabel('Cb, g/kg')
    ax.set_xlabel('day')

    fig.savefig('bor.png', dpi = 300)

def visualization():
    for fl in list(filter(lambda fold: os.path.isdir(fold), glob.glob('*'))):
        os.chdir(fl)
        data_sets = list(filter(lambda fold: os.path.isdir(fold), glob.glob('*')))

        os.chdir(data_sets[0]) #1_ImCore dir
        ImCore_KV7_data  = list(map(lambda path: os.path.abspath(path), glob.glob('KV7*')))
        ImCore_KV7_data.sort()
        ImCore_KV24_data = list(map(lambda path: os.path.abspath(path), glob.glob('KV_*')))
        ImCore_KV24_data.sort()
        ImCore_KQ_data   = list(map(lambda path: os.path.abspath(path), glob.glob('KQ*')))
        ImCore_KQ_data.sort()
        ImCore_AO_data   = os.path.abspath('AO.out')
        ImCore_bor_data  = os.path.abspath('bor.out')
        os.chdir('..')

        os.chdir(data_sets[1])  #2_smaz_dir
        smaz_KV7_data  = list(map(lambda path: os.path.abspath(path), glob.glob('KV7*')))
        smaz_KV7_data.sort()
        smaz_KV24_data = list(map(lambda path: os.path.abspath(path), glob.glob('KV_*')))
        smaz_KV24_data.sort()
        smaz_KQ_data   = list(map(lambda path: os.path.abspath(path), glob.glob('KQ*')))
        smaz_KQ_data.sort()
        smaz_AO_data   = os.path.abspath('AO.out')
        smaz_bor_data  = os.path.abspath('bor.out')
        os.chdir('..')

        #KV7 plots building
        for n, points in enumerate(ImCore_KV7_data):
            print_KV7(ImCore_KV7_data[n], smaz_KV7_data[n], n+1)

        #KQ maps building
        if (len(ImCore_KV24_data) > 0 and len(smaz_KQ_data) > 0):
            for n, points in enumerate(ImCore_KV24_data):
                print_KQ_map(ImC_KV = ImCore_KV24_data[n], smaz_KQ = smaz_KQ_data[n], point_num=n+1)

        elif (len(ImCore_KQ_data) > 0 and len(smaz_KQ_data) > 0):
            for n, points in enumerate(ImCore_KQ_data):
                print_KQ_map(ImC_KQ=ImCore_KQ_data[n], smaz_KQ=smaz_KQ_data[n], point_num=n+1)

        elif (len(ImCore_KQ_data) > 0 and len(smaz_KV24_data) > 0):
            for n, points in enumerate(ImCore_KQ_data):
                print_KQ_map(ImC_KQ=ImCore_KQ_data[n], smaz_KV=smaz_KV24_data[n], point_num=n+1)

        elif (len(ImCore_KV24_data) > 0 and len(smaz_KV24_data) > 0):
            for n, points in enumerate(ImCore_KV24_data):
                print_KQ_map(ImC_KV=ImCore_KV24_data[n], smaz_KV=smaz_KV24_data[n], point_num=n+1)

        #AO plon building
        print_AO(ImCore_AO_data, smaz_AO_data)

        #BOR plot building
        print_Bor(ImCore_bor_data, smaz_bor_data)

        os.chdir('..')

#***RUNNING***
visualization()