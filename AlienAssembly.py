from psychopy import visual
import pandas as pd
from numpy.random import randint
from PIL import Image
import time
from params import SCALE

ALIEN_SIZE = 0.3 * SCALE
REDUCED_ALIEN_SIZE = 0.2 * SCALE

def get_aliens(window, images_map_path, stim_path):
    """
    Params:
    window - window object that is displayed on
    images_map_path - map of feature id to feature path
    stim_path - stimulus file containing the alien descriptions

    Returns an array of aliens in the order of the stimulus file. Each
    alien is a list of stimuli that should be passed into the 'stim'
    param of BufferImageStim.
    """

    images_file = pd.read_excel(images_map_path, index_col=0)
    images_file.fillna(0, inplace=True)


    features = ['Body', 'Antenna', 'Eyes', 'Mouth', 'Tail', 'Arms', 'Legs']
    stim_file = pd.read_excel(stim_path, usecols=features, dtype=dict.fromkeys(features,str))


    aliens = []
    alien_names = []
    pos = (0, 0)


    for index, row in stim_file.iterrows():

        size = ALIEN_SIZE

        name = ""
        for i in row:
            name += i

        body_row = images_file.loc[row['Body'] + '_body']
        path_col = images_file['Image Path']

        # Body
        path = path_col.loc[row['Body'] + '_body']
        body = visual.ImageStim(window, image=path, pos=pos)
        body.size *= size

        # Skin and Color
        path = path_col.loc[row['Body'] + '_skin']
        # Randomly change the color of the alien slightly. Else color is set to given number.
        rand = randint(0, 80, size=(1, 3))
        color = tuple(*(255 - rand))
        name += '_(' + str(color[0]) + ',' + str(color[1]) + ',' + str(color[2]) + ')'
        skin = visual.ImageStim(window, image=path, pos=pos, color=color, colorSpace='rgb255')
        skin.size *= size

        base_id = row['Body'] + '_{}_{}'

        # Arms
        path = path_col.loc[base_id.format('arm', row['Arms'])]
        arms = visual.ImageStim(window, image=path, pos=pos)
        arms.size *= size

        # Legs
        path = path_col.loc[base_id.format('leg', row['Legs'])]
        legs = visual.ImageStim(window, image=path, pos=pos)
        legs.size *= size

        # Eyes
        path = path_col.loc[base_id.format('eye', row['Eyes'])]
        eyes = visual.ImageStim(window, image=path, pos=pos)
        eyes.size *= size

        # Mouth
        path = path_col.loc[base_id.format('mou', row['Mouth'])]
        mouth = visual.ImageStim(window, image=path, pos=pos)
        mouth.size *= size

        # Antenna
        path = path_col.loc[base_id.format('ant', row['Antenna'])]
        antenna = visual.ImageStim(window, image=path, pos=pos)
        antenna.size *= size

        # Tail Base
        path = path_col.loc[row['Body'] + '_tail']
        tail_b = visual.ImageStim(window, image=path, pos=pos)
        tail_b.size *= size

        # Tail
        path = path_col.loc[base_id.format('tail', row['Tail'])]
        tail = visual.ImageStim(window, image=path, pos=pos)
        tail.size *= size

        # Misc (depends on body)
        gloves = None
        if row['Body'] == 1:
            # Gloves
            path = path_col.loc[base_id.format('gloves', row['Arms'])]
            gloves = visual.ImageStim(window, image=path, pos=pos)
            gloves.size *= size

        stim_list = [tail_b, tail, arms, legs, body, skin, eyes, mouth, antenna]
        if gloves:
            stim_list.append(gloves)

        aliens.append(stim_list)
        alien_names.append(name)

    return aliens, alien_names
