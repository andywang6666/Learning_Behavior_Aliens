from psychopy import visual, core, event, monitors
import csv
import random
import os
import datetime
import pandas as pd
import math


from params import CONDITION, SUBJECT_ID, HRES, VRES, EXPHRES, EXPVRES, SCREENDISTANCE, SCREENWIDTH, FILEPATH, INPUT_MODE, OFFSET, PROCEDURE_PATH, RESULTS_PATH, FEATURE_PATH, IMAGES_MAP_PATH, INSTRUCTIONS_PATH, CONTEXTS_PATH, SCALE
from AlienAssembly import get_aliens

'''More constant parameters used for the functions.'''
ALIEN_ALIGN_LEFT_POS = (-0.3 * SCALE, 0.1 * SCALE)
ALIEN_ALIGN_RIGHT_POS = (0.3 * SCALE, 0.1 * SCALE)
ALIEN_ALIGN_CENTER_POS = (0, 0.1 * SCALE)
GENERAL_ALIEN_ALIGN_CENTER = (0, 0.2 * SCALE)
CONTEXT_ALIGN_CENTER_POS = (0, 0.1 * SCALE)
CONTEXT_ALIGN_LEFT_POS = (-0.4 * SCALE, 0.1 * SCALE)
CONTEXT_ALIGN_RIGHT_POS = (0.4 * SCALE, 0.1 * SCALE)
GENERAL_CONTEXT_ALIGN_LEFT = (-0.6 * SCALE, -0.2 * SCALE)
GENERAL_CONTEXT_ALIGN_RIGHT = (0.6 * SCALE, -0.2 * SCALE)
GENERAL_CONTEXT_ALIGN_CENTER = (0, -0.2 * SCALE)

FEATURE_ALIGN_CENTER_POS = ALIEN_ALIGN_CENTER_POS
FEATURE_BUTTONS_X_POSITIONS = [-0.5 * SCALE, 0, 0.5 * SCALE]
FEATURE_BUTTONS_Y_POSITIONS = [-0.3 * SCALE]
MEMORY_BUTTONS_X_POSITIONS = [-0.6 * SCALE, -0.2 * SCALE, 0.2 * SCALE, 0.6 * SCALE]
MEMORY_BUTTONS_Y_POSITIONS = [-0.3 * SCALE]
GENERAL_BUTTONS_X_POSITIONS = [-0.6 * SCALE, 0, 0.6 * SCALE]
GENERAL_BUTTONS_Y_POSITIONS = [-0.2 * SCALE]
NUM_STUDY_BUTTONS = 2
NUM_MEMORY_BUTTONS = 4
NUM_FEATURE_BUTTONS = 3
NUM_GENERAL_BUTTONS = 3
NUM_FEATURES = 8
ALIEN_SIZE = 0.3
REDUCED_ALIEN_SIZE = 0.2
CONTEXT_SIZE = [1.1 * SCALE, 0.7 * SCALE]
REDUCED_CONTEXT_SIZE = [0.45 * SCALE, 0.3 * SCALE]
FEATURE_SIZE = 0.3 * SCALE

'''This index keeps track of the next alien we use when we encounter a trial that involves drawing an alien. We increment it by 1 every time we have a trial type involving an alien.'''
current_alien_index = 0
'''This is the alien list keeping track of aliens used in the experiment, appearing in the same order as the trials they are in.'''
alien_list = []

def start_clock():
    clock = core.Clock()
    clock.reset()

    return clock

def create_window():
    experiment_monitor = monitors.Monitor('expMonitor', distance=SCREENDISTANCE, width = SCREENWIDTH)
    experiment_monitor.setSizePix((EXPHRES, EXPVRES))
    experiment_monitor.saveMon()
    window = visual.Window([HRES, VRES], allowGUI = True, monitor = experiment_monitor, units = 'height', color = 'white', fullscr = True, screen=0)

    return window

def read_procedural_csv():
    procedural_file_list = pd.read_csv(FILEPATH + PROCEDURE_PATH + SUBJECT_ID + 'proc.csv')
    return procedural_file_list

def create_results_file():
    '''Creates a results file if a previous one doesn't exist.'''
    if os.path.isfile(FILEPATH + RESULTS_PATH + SUBJECT_ID + "result.csv"):
        return 0

    with open(FILEPATH + RESULTS_PATH + SUBJECT_ID + "result.csv", 'w+t', newline='') as results_file:
        procedural_file_writer = csv.writer(results_file, delimiter= ',')
        procedural_file_writer.writerow(["ID", "Trial Type", "Schedule", "Instruction Path", "Body", "Arms", "Legs", "Eyes", "Mouth", "Antenna", "Tail", "Color", "Feature Path", "Context Path 1", "Context Path 2", "Left/Right", "Correct Answer", "Order", "ResponseTime", "Response", "Accuracy", "Confidence", "Trial Start", "Alien Onset Time"])

    return 1

def get_results_status():
    '''Gets the index of the last procedure that the previous experiment stopped at.'''
    results_list = []
    with open(FILEPATH + RESULTS_PATH + SUBJECT_ID + "result.csv", 'rt') as results_file:
        results_reader = csv.reader(results_file, delimiter=',')
        results_list = list(results_reader)

    return len(results_list) - 1

def rgb_to_hex(rgb_tuple):
    '''Converts a RGB color tuple to its hexadecimal representation.'''
    return_hex = '#'
    '''Hexadecimal looks like #1AB2C3'''
    '''Maps a decimal value to its hexadecimal digit. The decimal value is the key, or index, and the hexadecimal digit is the value.'''
    hex_dict = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']
    '''Each color value (in RGB order) corresponds to 2 hexadecimal digits.'''
    for value in rgb_tuple:
        return_hex += hex_dict[(value % 256) // 16]
        return_hex += hex_dict[value % 16]
    return return_hex

def create_buttons_from_dimensions(window, x_pos_array, y_pos_array, num_buttons, colorGradient, opaqueness, width, height):
    '''Handles detailed functions of creating buttons using dimension parameters.'''
    fill_color_array = []
    button_array = []
    '''If the color gradient condition is not specified, the buttons will have a white fill color, as specified by the RGB tuple.'''
    if not colorGradient:
        for i in range (num_buttons):
            fill_color_array.append((255, 255, 255))
    else:
        '''This makes the button's fill color go from dark red to light red, and then light blue to dark blue.'''
        '''The color gradient allows the subject to distinguish between the different answer choices.'''
        for i in range (num_buttons):
            if (i < num_buttons / 2):
                red_color = 255
                green_color = math.floor(80 + i * (120 / num_buttons))
                blue_color = math.floor(80 + i * (120 / num_buttons))
                fill_color_array.append((red_color, green_color, blue_color))
            else:
                red_color = math.floor(80 + (num_buttons - i) * (120 / num_buttons))
                green_color = math.floor(80 + (num_buttons - i) * (120 / num_buttons))
                blue_color = 255
                fill_color_array.append((red_color, green_color, blue_color))

    '''Creates the buttons in the window from dimensions.'''
    for i in range (num_buttons):
        button_array.append(visual.Rect(window, opacity = opaqueness, fillColor = rgb_to_hex(fill_color_array[i]), fillColorSpace = 'rgb', width = width, height = height, lineWidth = .5, lineColor = 'black', pos = (x_pos_array[i], y_pos_array[0])))
    return button_array


def create_buttons(window):
    '''Creates buttons for all 4 different types of phases. Does this calling detailed button creation functions.'''
    instruction_buttons = create_buttons_from_dimensions(window, [0], [0], 1, False, 0, 2, 1)
    memory_buttons = create_buttons_from_dimensions(window, MEMORY_BUTTONS_X_POSITIONS, MEMORY_BUTTONS_Y_POSITIONS, NUM_MEMORY_BUTTONS, True, 1, 0.3 * SCALE, 0.1 * SCALE)
    feature_buttons = create_buttons_from_dimensions(window, FEATURE_BUTTONS_X_POSITIONS, FEATURE_BUTTONS_Y_POSITIONS, NUM_FEATURE_BUTTONS, False, 1, 0.3 * SCALE, 0.1 * SCALE)
    general_buttons = create_buttons_from_dimensions(window, GENERAL_BUTTONS_X_POSITIONS, GENERAL_BUTTONS_Y_POSITIONS, NUM_GENERAL_BUTTONS, False, 0, 0.45 * SCALE, 0.3 * SCALE)
    return instruction_buttons, memory_buttons, feature_buttons, general_buttons

def button_text_from_dimensions(window, text_content, x_pos_array, y_pos_array, num_buttons):
    '''Handles detailed functions of creating text on buttons using dimension parameters.'''
    text_array = []
    for i in range(num_buttons):
        text_array.append(visual.TextStim(window, pos = [x_pos_array[i], y_pos_array[0]], text = text_content[i], color='black', height = 0.04 * SCALE))
    return text_array

def create_buttons_text(window):
    '''Creates text on buttons used for all 4 phases of the experiment.'''
    '''Text content contains what will be displayed on the buttons for each trial, with the number of entries in each list for each phase
    corresponding to the number of buttons for that phase, corresponding to the buttons in left to right order.''' 
    memory_text_content = ["1 - Sure,\n   new", "2 - Unsure,\n     new", "3 - Sure,\n    old", "4 - Unsure,\n      old"]
    feature_text_content = ["Studied", "Tested", "New"]
    general_text_content = ["Left Context", "Middle Context", "Right Context"]

    memory_button_text = button_text_from_dimensions(window, memory_text_content, MEMORY_BUTTONS_X_POSITIONS, MEMORY_BUTTONS_Y_POSITIONS, NUM_MEMORY_BUTTONS)
    feature_button_text = button_text_from_dimensions(window, feature_text_content, FEATURE_BUTTONS_X_POSITIONS, FEATURE_BUTTONS_Y_POSITIONS, NUM_FEATURE_BUTTONS)
    return memory_button_text, feature_button_text







def draw_context(window, context_position, context_path, image_size):
    '''Draws context(environment) alien is in on the screen.'''
    context = visual.ImageStim(window, image = FILEPATH + CONTEXTS_PATH + context_path + ".jpg", size = image_size, pos = context_position)
    context.draw()

def draw_alien(window, stim_list, position):
    '''Draws alien on the screen at the specified position.'''
    for stim in stim_list:
        stim.pos = position
        stim.draw()

def get_response(window, mouse, button_array, clock, wait_time, num_options, input_mode, return_list):
    '''Depending on the input mode(mouse, MRI buttons, etc.), gets a response from the user under the timed conditions(wait_time), and returns
        the response as well as the response time.'''

    '''A negative wait-time means that there is no time limit.'''
    response_time = wait_time
    response = 'No answer'

    if input_mode == 0:
        '''Mouse input'''
        if wait_time < 0:
            start_time = clock.getTime()
            '''When the user presses the mouse on one of the buttons, the function will get the response.'''
            while True:
                for i in range(0, len(button_array)):
                    if mouse.isPressedIn(button_array[i], buttons = [0]):
                        response_time = clock.getTime() - start_time
                        response = i
                        return_list.extend([response_time, response])
                        return response_time, response

        else:
            '''Timed version of the block of code above.'''
            timer = core.Clock()
            timer.add(wait_time)
            start_time = clock.getTime()
            while timer.getTime() < 0:
                for i in range(0, len(button_array)):
                    if mouse.isPressedIn(button_array[i], buttons = [0]):
                        response_time = clock.getTime() - start_time
                        response = i
                        return_list.extend([response_time, response])
                        return response_time, response


            return_list.extend([clock.getTime() - start_time, 'No answer'])
            return clock.getTime() - start_time, 'No answer'



    elif input_mode == 1 or input_mode == 2 or input_mode == 3:
        '''Key input'''
        start_time = clock.getTime()
        '''Only difference between 2 input modes is that they use different keys.'''
        if input_mode == 1:
             keys = ['q', '1', '2', '3', '4']
        elif input_mode == 2:
             keys = ['q', 'd', 'f', 'j', 'k']
        else:
             keys = ['q', 'left', 'right']
        
        '''Gets response when one of the keys above is pressed. If the key pressed is 'q', the experiment ends. Otherwise, the appropriate response is collected.'''

        if wait_time < 0:
            selection = event.waitKeys(keyList = keys[0:num_options + 1], timeStamped=clock)
            if selection[0][0] == 'q':
                window.close()
                core.quit()
            for i in range(1, num_options + 1):
                if selection[0][0] == keys[i]:
                    response = i - 1
                    return_list.extend([selection[0][1] - start_time, response])
                    return selection[0][1] - start_time, response


        else:
            selection = event.waitKeys(maxWait=wait_time, keyList = keys[0:num_options + 1], timeStamped=clock)
            if selection is None:
                response = 'No answer'
                return_list.extend([clock.getTime() - start_time, response])
                return [clock.getTime() - start_time, response]
            if selection[0][0] == 'q':
                window.close()
                core.quit()
            for i in range(1, num_options + 1):
                if selection[0][0] == keys[i]:
                    response = i - 1
            return_list.extend([selection[0][1] - start_time, response])
            return selection[0][1] - start_time, response


def record_procedure(procedure, results):
    '''Records the results for each phase, which are the parameters to the function, in the appropriate CSV file.'''
    '''result_row = procedure.to_list().extend((response_time, response, accuracy, confidence))'''
    with open(FILEPATH + RESULTS_PATH + SUBJECT_ID + "result.csv", 'a', newline='') as procedure_file:
        result_row = procedure.append(pd.Series(results))
        procedure_csv_writer = csv.writer(procedure_file, delimiter=',')
        procedure_csv_writer.writerow(result_row)

def display_incorrect_message(window):
    window.flip()
    window.flip()
    incorrect_message = visual.TextStim(window, pos = (0, 0), text = "You missed the alien. Respond faster next time", color = 'black', height = 0.1)
    incorrect_message.draw()
    window.flip(clearBuffer=False)

def post_procedure(window, procedure, results):
    '''After every trial, the results are written to the result file and the screen is cleared.'''
    record_procedure(procedure, results)
    window.flip()
    window.flip()
    core.wait(0.5)

def delay(clock, delay_time):
    '''Delays the program by a set amount of time.'''
    start_time = clock.getTime()
    while clock.getTime() - start_time < delay_time:
        continue

def draw_buttons_and_text(button_array, text_array, num_buttons):
    
    for i in range(num_buttons):
        button_array[i].draw()
    if text_array != "NA":
        for i in range(num_buttons):
            text_array[i].draw()

def instruction_procedure(window, mouse, clock, procedure, button_array):
    '''The instruction procedure displays the instructions for the upcoming trial types for the subject to follow. The subject presses a key to
    indicate that they will move on, or in the case of the mouse input mode, presses the mouse.'''

    instruction_path = procedure['Instruction Path']
    
    image = visual.ImageStim(window, image = FILEPATH + INSTRUCTIONS_PATH + instruction_path, pos = (0, 0))
    image.draw()
    window.flip(clearBuffer=False)
    
    num_options = 1 if INPUT_MODE == 0 else 4
    procedure_start_time = datetime.datetime.now()
    response_time, response = get_response(window, mouse, button_array, clock, -2, num_options, INPUT_MODE, [])
    
    results = ["NA", "NA", "NA", "NA", procedure_start_time, "NA"]
    post_procedure(window, procedure, results)
    window.flip()

def draw_images(clock, window, context_path):
    delay(clock, 1)
    draw_context(window, CONTEXT_ALIGN_CENTER_POS, context_path, CONTEXT_SIZE)
    window.flip(clearBuffer=False)


def study_procedure(window, mouse, clock, procedure):
    '''In the study phase, the user sees the context for 1.5 second, before seeing the alien flash in the context within the next second, and must
    answer which side the alien is on using the buttons within 3 seconds of the flash. If they are correct, they will study the alien in its context for 4 more seconds.
    Otherwise, nothing happens.'''
    global current_alien_index
    procedure_start_time = clock.getTime()
    
    '''Determines a random time within a 1 second window an alien will flash'''
    alien_onset = random.random() 
    current_alien = alien_list[current_alien_index]
    context_path = procedure['Context Path 1']

    '''Draws context'''
    draw_context(window, CONTEXT_ALIGN_CENTER_POS, context_path, CONTEXT_SIZE)
    window.flip(clearBuffer=False)
    context_start_time = datetime.datetime.now()

    '''1 second delay'''
    delay(clock, 1.5 + alien_onset)
    
    '''Draws alien in context, along with buttons.'''
    possible_answers = ["Left", "Right"]
    alien_position = ALIEN_ALIGN_RIGHT_POS if (int(procedure['Left/Right']) == 1) else ALIEN_ALIGN_LEFT_POS
    draw_context(window, CONTEXT_ALIGN_CENTER_POS, context_path, CONTEXT_SIZE)
    draw_alien(window, current_alien, alien_position)
    window.flip(clearBuffer=False)
    alien_start_time = datetime.datetime.now()

    return_list = []

    response_time, response = get_response(window, mouse, "NA", clock, 1, 2, 3, return_list)


    if (response == "No answer"):
         draw_context(window, CONTEXT_ALIGN_CENTER_POS, context_path, CONTEXT_SIZE)
         window.flip(clearBuffer=False)
         response_time, response = get_response(window, mouse, "NA", clock, 2, 2, 3, return_list)
         response_time += 1

    '''If the response is incorrect, display an appropriate error message.'''
    if response == "No answer" or procedure['Correct Answer'] != possible_answers[int(response)]:
        accuracy = 0
        display_incorrect_message(window)
        delay(clock, 2)
    else:
        '''If the user answers correctly, display the alien and context for 4 more seconds.'''
        accuracy = 1
        draw_context(window, CONTEXT_ALIGN_CENTER_POS, context_path, CONTEXT_SIZE)
        draw_alien(window, current_alien, ALIEN_ALIGN_CENTER_POS)
        window.flip(clearBuffer=False)
        delay(clock, 4)

    recorded_response = response if response == "No answer" else possible_answers[int(response)]
    results = [response_time, recorded_response, accuracy, "NA", context_start_time, alien_start_time]
    post_procedure(window, procedure, results)
    current_alien_index += 1
    


def memory_procedure(window, mouse, clock, procedure, memory_buttons, button_text):
    '''In this phase, the user is tested on his memory by being presented with an alien, and then answering whether or not that alien was
    encountered in the study phase. Additionally, he also answers whether or not he is sure or unsure about his answer.'''

    '''Draws alien and buttons on screen.'''
    global current_alien_index
    current_alien = alien_list[current_alien_index]
    
    draw_alien(window, current_alien, ALIEN_ALIGN_CENTER_POS)
    draw_buttons_and_text(memory_buttons, button_text, NUM_MEMORY_BUTTONS)
    window.flip(clearBuffer=False)
    procedure_start_time = datetime.datetime.now()

    response_time, response = get_response(window, mouse, memory_buttons, clock, -1, 4, INPUT_MODE, [])
    possible_answers = ["Sure, new", "Unsure, new", "Sure, old", "Unsure, old"]

    accuracy = 1 if (response < 2 and procedure['Correct Answer'] == "New") or (response >= 2 and procedure['Correct Answer'] == "Old") else 0
    confidence = 1 if (response == 0 or response == 2) else 0
    
    results = [response_time, possible_answers[int(response)], accuracy, confidence, procedure_start_time, "NA"]
    post_procedure(window, procedure, results)
    current_alien_index += 1

def draw_feature(window, feature_position, feature_path):
    feature = visual.ImageStim(window, image = FILEPATH + feature_path, pos = feature_position)
    feature.size *= FEATURE_SIZE
    feature.draw()


def feature_procedure(window, mouse, clock, procedure, feature_buttons, button_text):
    '''Gets feature to be tested.'''
    possible_answers = ["Studied", "Tested", "New"]
    feature_path = FILEPATH + FEATURE_PATH + procedure['Feature Path']
    '''Draws feature tested along with buttons.'''
    draw_feature(window, FEATURE_ALIGN_CENTER_POS, feature_path)
    draw_buttons_and_text(feature_buttons, button_text, NUM_FEATURE_BUTTONS)
    window.flip(clearBuffer=False)
    procedure_start_time = datetime.datetime.now()
    '''Gets response and records it.'''
    response_time, response = get_response(window, mouse, feature_buttons, clock, -1, 3, INPUT_MODE, [])
    accuracy = 1 if procedure['Correct Answer'] == possible_answers[int(response)] else 0

    results = [response_time, possible_answers[int(response)], accuracy, "NA", procedure_start_time, "NA"]
    post_procedure(window, procedure, results)



def general_procedure(window, mouse, clock, procedure, general_buttons):
    '''In this phase, the user is tested on his ability to generalize his knowledge of aliens and contexts by being presented with an alien and
    3 contexts, and determining which context the alien is most likely to belong in. 2 of the contexts are contexts the user has studied before,
    and the third is a non-studied context.'''

    '''Draws alien and buttons.'''
    global current_alien_index
    current_alien = alien_list[current_alien_index]
    draw_alien(window, current_alien, GENERAL_ALIEN_ALIGN_CENTER)
    current_alien_index += 1
    draw_buttons_and_text(general_buttons, "NA", NUM_GENERAL_BUTTONS)

    '''Picks contexts to be used from the file.'''
    context_path_1 = procedure['Context Path 1']
    context_path_2 = procedure['Context Path 2']
    context_path_3 = procedure['Context Path 3']


    possible_answers = ["Left", "Middle", "Right"]
    draw_context(window, GENERAL_CONTEXT_ALIGN_LEFT, context_path_1, REDUCED_CONTEXT_SIZE)
    draw_context(window, GENERAL_CONTEXT_ALIGN_CENTER, context_path_2, REDUCED_CONTEXT_SIZE)
    draw_context(window, GENERAL_CONTEXT_ALIGN_RIGHT, context_path_3, REDUCED_CONTEXT_SIZE)

    window.flip(clearBuffer=False)
    procedure_start_time = datetime.datetime.now()

    response_time, response = get_response(window, mouse, general_buttons, clock, -1, 3, INPUT_MODE, [])
    accuracy = 1 if procedure['Correct Answer'] == possible_answers[int(response)] else 0

    results = [response_time, possible_answers[int(response)], accuracy, "NA", procedure_start_time, "NA"]
    post_procedure(window, procedure, results)

def main():

    '''Function responsible for executing the code running the alien experiment.'''
    
    '''Starts the clock at 0. This marks the beginning of the experiment.'''
    clock = start_clock()

    window = create_window()
    '''Determines visibility of mouse based on input mode'''
    is_visible = False if (INPUT_MODE != 0) else True
    mouse = event.Mouse(visible=is_visible,  newPos = None, win=window)

    global alien_list
    global current_alien_index
    alien_list = get_aliens(window, IMAGES_MAP_PATH, PROCEDURE_PATH + SUBJECT_ID + "proc.csv")

    current_alien_index = 0

    procedural_file_list = read_procedural_csv()

    '''First, we determine whether or not there is already data from a previous experiment on the same subject.'''
    new_session = create_results_file()

    '''If there is, we get the index of the procedure that the experiment stopped at.'''
    current_status = 0
    if new_session == 0:
        current_status = get_results_status()


    
    instruction_buttons, memory_buttons, feature_buttons, general_buttons = create_buttons(window)

    memory_button_text, feature_button_text = create_buttons_text(window)

    for index, procedure in procedural_file_list.iterrows():
        if current_status > 0:
            '''We skip procedures until we get to the one that the previous experiment run stopped at.'''
            if procedure['Trial Type'] != 'Instruct' and procedure['Trial Type'] != 'FeatureTest':
                '''We also offset the index keeping track of which alien to get to account for the skipped procedures.'''
                current_alien_index += 1
            current_status -= 1
            continue 
        
        '''Executes specific type of procedure based on the trial type read.'''
        if procedure['Trial Type'] == 'Instruct':
            instruction_procedure(window, mouse, clock, procedure, instruction_buttons)
        elif procedure['Trial Type'] == 'Study':
            study_procedure(window, mouse, clock,  procedure)
        elif procedure['Trial Type'] == 'MemoryTest':
            memory_procedure(window, mouse, clock, procedure, memory_buttons, memory_button_text)
        elif procedure['Trial Type'] == 'FeatureTest':
            feature_procedure(window, mouse, clock, procedure, feature_buttons, feature_button_text)
        elif procedure['Trial Type'] == 'GeneralTest':
            general_procedure(window, mouse, clock, procedure, general_buttons)




if __name__ == '__main__':
    main()
