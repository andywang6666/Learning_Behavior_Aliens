from psychopy import visual
import pandas as pd
from numpy.random import randint
from PIL import Image
import time
from params import SCALE

ALIEN_SIZE = 0.3 * SCALE
REDUCED_ALIEN_SIZE = 0.2 * SCALE

def get_alien(window, images_map_path, procedure):
    """
    Params:
    window - window object that is displayed on
    images_map_path - map of feature id to feature path
    procedure - a single line from the procedure file which to create the alien

    Returns an array of aliens in the order of the stimulus file. Each
    alien is a list of stimuli that should be passed into the 'stim'
    param of BufferImageStim.
    """

    images_file = pd.read_excel(images_map_path, index_col=0)
    images_file.fillna(0, inplace=True)


    features = ['Body', 'Antenna', 'Eyes', 'Mouth', 'Tail', 'Arms', 'Legs']
    alien_info = procedure[features].apply(int).apply(str)

    name = ''
    pos = (0, 0)

    size = ALIEN_SIZE

    for feat in alien_info:
        name += feat

    body_row = images_file.loc[alien_info['Body'] + '_body']
    path_col = images_file['Image Path']

    # Body
    path = path_col.loc[alien_info['Body'] + '_body']
    body = visual.ImageStim(window, image=path, pos=pos)
    body.size *= size

    # Skin and Color
    path = path_col.loc[alien_info['Body'] + '_skin']
    # Randomly change the color of the alien slightly. Else color is set to given number.
    rand = randint(0, 80, size=(1, 3))
    color = tuple(*(255 - rand))
    name += '_(' + str(color[0]) + ',' + str(color[1]) + ',' + str(color[2]) + ')'
    skin = visual.ImageStim(window, image=path, pos=pos, color=color, colorSpace='rgb255')
    skin.size *= size

    base_id = alien_info['Body'] + '_{}_{}'

    # Arms
    path = path_col.loc[base_id.format('arm', alien_info['Arms'])]
    arms = visual.ImageStim(window, image=path, pos=pos)
    arms.size *= size

    # Legs
    path = path_col.loc[base_id.format('leg', alien_info['Legs'])]
    legs = visual.ImageStim(window, image=path, pos=pos)
    legs.size *= size

    # Eyes
    path = path_col.loc[base_id.format('eye', alien_info['Eyes'])]
    eyes = visual.ImageStim(window, image=path, pos=pos)
    eyes.size *= size

    # Mouth
    path = path_col.loc[base_id.format('mou', alien_info['Mouth'])]
    mouth = visual.ImageStim(window, image=path, pos=pos)
    mouth.size *= size

    # Antenna
    path = path_col.loc[base_id.format('ant', alien_info['Antenna'])]
    antenna = visual.ImageStim(window, image=path, pos=pos)
    antenna.size *= size

    # Tail Base
    path = path_col.loc[alien_info['Body'] + '_tail']
    tail_b = visual.ImageStim(window, image=path, pos=pos)
    tail_b.size *= size

    # Tail
    path = path_col.loc[base_id.format('tail', alien_info['Tail'])]
    tail = visual.ImageStim(window, image=path, pos=pos)
    tail.size *= size

    # Misc (depends on body)
    gloves = None
    if alien_info['Body'] == 1:
        # Gloves
        path = path_col.loc[base_id.format('gloves', alien_info['Arms'])]
        gloves = visual.ImageStim(window, image=path, pos=pos)
        gloves.size *= size

    alien_object = [tail_b, tail, arms, legs, body, skin, eyes, mouth, antenna]
    if gloves:
        alien_object.append(gloves)

    return alien_object, name
