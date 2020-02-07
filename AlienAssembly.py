from psychopy import visual
import pandas as pd
from numpy.random import randint
from PIL import Image
import time
from params import SCALE

ALIEN_SIZE = 0.3 * SCALE
REDUCED_ALIEN_SIZE = 0.2 * SCALE

def get_alien(window, features_path, procedure):
    """
    Params:
    window - window object that is displayed on
    features_path - map of feature id to feature path
    procedure - a single line from the procedure file which to create the alien

    Returns an array of aliens in the order of the stimulus file. Each
    alien is a list of stimuli that should be passed into the 'stim'
    param of BufferImageStim.
    """

    features = ['Body', 'Antenna', 'Eyes', 'Mouth', 'Tail', 'Arms', 'Legs']
    alien_info = procedure[features].apply(int).apply(str)

    name = ''
    pos = (0, 0)

    size = ALIEN_SIZE

    for feat in alien_info:
        name += feat

    base_id = alien_info['Body'] + '_{}_{}.png'

    # Body
    path = features_path + alien_info['Body'] + '_body.png'
    body = visual.ImageStim(window, image=path, pos=pos)
    body.size *= size

    # Skin and Color: Male and female has different skin image name formats
    if alien_info['Body'] == '1':
        path = features_path + base_id.format('skin', alien_info['Arms'])
    else:
        path = features_path + alien_info['Body'] + '_skin.png'
    # Randomly change the color of the alien slightly. Else color is set to given number.
    rand = randint(0, 80, size=(1, 3))
    color = tuple(*(255 - rand))
    name += '_(' + str(color[0]) + ',' + str(color[1]) + ',' + str(color[2]) + ')'
    skin = visual.ImageStim(window, image=path, pos=pos, color=color, colorSpace='rgb255')
    skin.size *= size

    # Arms: only female has 'arms'
    if alien_info['Body'] == '1':
        # Male alien has 'gloves', but is just called 'arms' here for convenience
        path = features_path + base_id.format('glove', alien_info['Arms'])
        arms = visual.ImageStim(window, image=path, pos=pos)
        arms.size *= size
    else:
        path = features_path + base_id.format('arm', alien_info['Arms'])
        arms = visual.ImageStim(window, image=path, pos=pos)
        arms.size *= size

    # Legs
    path = features_path + base_id.format('leg', alien_info['Legs'])
    legs = visual.ImageStim(window, image=path, pos=pos)
    legs.size *= size

    # Eyes
    path = features_path + base_id.format('eye', alien_info['Eyes'])
    eyes = visual.ImageStim(window, image=path, pos=pos)
    eyes.size *= size

    # Mouth
    path = features_path + base_id.format('mou', alien_info['Mouth'])
    mouth = visual.ImageStim(window, image=path, pos=pos)
    mouth.size *= size

    # Antenna
    path = features_path + base_id.format('ant', alien_info['Antenna'])
    antenna = visual.ImageStim(window, image=path, pos=pos)
    antenna.size *= size

    # NO TAIL BASE
    # # Tail Base
    # path = features_path + alien_info['Body'] + '_tail'
    # tail_b = visual.ImageStim(window, image=path, pos=pos)
    # tail_b.size *= size

    # Tail
    path = features_path + base_id.format('tail', alien_info['Tail'])
    tail = visual.ImageStim(window, image=path, pos=pos)
    tail.size *= size


    # Different layers ordering for male and female aliens
    if alien_info['Body'] == '1':
        alien_object = [tail, skin, arms, legs, body, eyes, mouth, antenna]
    else:
        alien_object = [tail, arms, legs, body, skin, eyes, mouth, antenna]

    return alien_object, name
