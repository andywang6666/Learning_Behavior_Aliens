from psychopy import visual
import pandas as pd
from PIL import Image
import time

def get_aliens(images_map_path, row, window):
    """
    Returns an array of list of stimuli for the alien of the given row
    """
    
    images_file = pd.read_excel(images_map_path, index_col=0)
    images_file.fillna(0, inplace=True)
    
    size = 0.3
    
    color = row['Color']

    body_row = images_file.loc[str(int(row['Body'])) + '_body']
    path_col = images_file['Image Path']

    side_offset = 0.5 if row['Left/Right'] == 'right' else -0.5

    # Body
    path = path_col.loc[str(int(row['Body'])) + '_body']
    pos = (side_offset, 0)
    body = visual.ImageStim(window, image=path, pos=pos)
    body.size *= size
    '''
    # Skin
    path = path_col.loc[str(int(row['Body'])) + '_skin']
    pos = (side_offset, 0)
    skin = visual.ImageStim(window, image=path, pos=pos, color=color, colorSpace='rgb255')
    skin.size *= size
    '''

    base_id = str(int(row['Body'])) + '_{}_{}'

    # Arms
    path = path_col.loc[base_id.format('arm', int(row['Arms']))]
    pos = (body_row['Arms_X'] + side_offset, body_row['Arms_Y'])
    arms = visual.ImageStim(window, image=path, pos=pos)
    arms.size *= size

    # Legs
    path = path_col.loc[base_id.format('leg', int(row['Legs']))]
    pos = (body_row['Legs_X'] + side_offset, body_row['Legs_Y'])
    legs = visual.ImageStim(window, image=path, pos=pos)
    legs.size *= size

    # Eyes
    path = path_col.loc[base_id.format('eye', int(row['Eyes']))]
    pos = (body_row['Eyes_X'] + side_offset, body_row['Eyes_Y'])
    eyes = visual.ImageStim(window, image=path, pos=pos)
    eyes.size *= size

    # Mouth
    path = path_col.loc[base_id.format('mou', int(row['Mouth']))]
    pos = (body_row['Mouth_X'] + side_offset, body_row['Mouth_Y'])
    mouth = visual.ImageStim(window, image=path, pos=pos)
    mouth.size *= size

    # Antenna
    path = path_col.loc[base_id.format('ant', int(row['Antenna']))]
    pos = (body_row['Antenna_X'] + side_offset, body_row['Antenna_Y'])
    antenna = visual.ImageStim(window, image=path, pos=pos)
    antenna.size *= size

    # Tail Base
    path = path_col.loc[str(int(row['Body'])) + '_tail']
    pos = (body_row['Tail_X'] + side_offset, body_row['Tail_Y'])
    tail_b = visual.ImageStim(window, image=path, pos=pos)
    tail_b.size *= size

    # Tail
    path = path_col.loc[base_id.format('tail', int(row['Tail']))]
    pos = (body_row['Tail_X'] + side_offset, body_row['Tail_Y'])
    tail = visual.ImageStim(window, image=path, pos=pos)
    tail.size *= size

    # Misc (depends on body)
    gloves = None
    if row['Body'] == 1:
        # Gloves
        path = path_col.loc[base_id.format('gloves', row['Arms'])]
        pos = (body_row['Misc_X'] + side_offset, body_row['Misc_Y'])
        gloves = visual.ImageStim(window, image=path, pos=pos)
        gloves.size *= size

    stim_list = [tail_b, tail, arms, legs, body, eyes, mouth, antenna]
    if gloves:
        stim_list.append(gloves)
        
    return stim_list