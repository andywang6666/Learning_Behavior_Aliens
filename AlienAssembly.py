from psychopy import visual
import pandas as pd
from numpy.random import randint
from PIL import Image
import time
from params import SCALE

ALIEN_SIZE = 0.3 * SCALE
REDUCED_ALIEN_SIZE = 0.2 * SCALE

def get_aliens(window, images_map_path, features_path):
    """
    Params:
    window - window object that is displayed on
    images_map_path - map of feature id to feature path
    features_path - procedure file containing the alien descriptions
    # pos - tuple (x, y) for pixel coordinates alien is located
    size - size ratio respective to original size (<=0.3 recommended)

    This function reads in the color for the aliens from the procedure
    file. Color value of 255 is original color. >255 turns it green-blue.
    <255 makes the alien a range of colors.

    Returns an array of aliens in the order of the procedure file. Each
    alien is a list of stimuli that should be passed into the 'stim'
    param of BufferImageStim.
    """

    images_file = pd.read_excel(images_map_path, index_col=0)
    images_file.fillna(0, inplace=True)


    features = ['Body', 'Arms', 'Legs', 'Eyes', 'Mouth', 'Antenna', 'Tail', 'Color']
    features_file = pd.read_csv(features_path)
    features_file = features_file.loc[features_file['Trial Type'] != 'FeatureTest']
    features_file = features_file.loc[features_file['Trial Type'] != 'Instruct']
    trial_type = features_file['Trial Type']
    features_file = features_file[features].astype('int')
    

    aliens = []

    pos = (0, 0)

    size = 0

    trial_type_list = []
    trial_type_list_index = 0

    for index, value in trial_type.items():
        trial_type_list.append(str(value))


    for index, row in features_file.iterrows():
        
        if trial_type_list[trial_type_list_index] == 'GeneralTest':
            size = REDUCED_ALIEN_SIZE
        else:
            size = ALIEN_SIZE
        trial_type_list_index += 1
        

        body_row = images_file.loc[str(row['Body']) + '_body']
        path_col = images_file['Image Path']

        # Body
        path = path_col.loc[str(row['Body']) + '_body']
        body = visual.ImageStim(window, image=path, pos=pos)
        body.size *= size

        # Skin and Color
        path = path_col.loc[str(row['Body']) + '_skin']
        # If color is 255, then randomly change the color of the alien slightly. Else color is set to given number.
        rand = randint(0, 80, size=(1, 3))
        color = row['Color'] if row['Color'] != 255 else tuple(*(255 - rand))
        skin = visual.ImageStim(window, image=path, pos=pos, color=color, colorSpace='rgb255')
        skin.size *= size

        base_id = str(row['Body']) + '_{}_{}'

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
        path = path_col.loc[str(row['Body']) + '_tail']
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

    return aliens
