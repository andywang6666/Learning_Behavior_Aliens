from psychopy import visual, core, event, monitors 
import csv
import random
import os
import datetime

from params import CONDITION, SUBJECT_ID, HRES, VRES, EXPHRES, EXPVRES, SCREENDISTANCE, SCREENWIDTH, FILEPATH, INPUT_MODE, OFFSET
'''More constant parameters used for the functions.'''
ALIEN_ALIGN_LEFT_POS = (-0.2, 0.2)
ALIEN_ALIGN_RIGHT_POS = (0.2, 0.2)
ALIEN_ALIGN_CENTER_POS = (0, 0.2)
CONTEXT_ALIGN_CENTER_POS = (0, 0.25)
CONTEXT_ALIGN_LEFT_POS = (-0.4, 0.25)
CONTEXT_ALIGN_RIGHT_POS = (0.4, 0.25)
GENERAL_CONTEXT_ALIGN_LEFT = (-0.4, -0.225)
GENERAL_CONTEXT_ALIGN_RIGHT = (0.4, -0.225)
GENERAL_CONTEXT_ALIGN_CENTER = (0, -0.225)

FEATURE_ALIGN_CENTER_POS = ALIEN_ALIGN_CENTER_POS
STUDY_BUTTON_X_POSITIONS = [-0.2, 0.2]
STUDY_BUTTON_Y_POSITIONS = [-0.2]
FEATURE_BUTTONS_X_POSITIONS = [-0.4, -0.08, 0.24]
FEATURE_BUTTONS_Y_POSITIONS = [-0.2]
MEMORY_BUTTONS_X_POSITIONS = [-0.5, -0.18, 0.14, 0.46]
MEMORY_BUTTONS_Y_POSITIONS = [-0.2]
GENERAL_BUTTONS_X_POSITIONS = [-0.4, 0, 0.4]
GENERAL_BUTTONS_Y_POSITIONS = [-0.425]
NUM_STUDY_BUTTONS = 2
NUM_MEMORY_BUTTONS = 4
NUM_FEATURE_BUTTONS = 3
NUM_GENERAL_BUTTONS = 3
NUM_FEATURES = 8
ALIEN_SIZE = [0.45, 0.6]
CONTEXT_SIZE = [0.9, 0.7]
REDUCED_CONTEXT_SIZE = [0.3, 0.3]
FEATURE_SIZE = [0.05, 0.05]

def create_window():
    experiment_monitor = monitors.Monitor('expMonitor', distance=SCREENDISTANCE, width = SCREENWIDTH)
    experiment_monitor.setSizePix((EXPHRES, EXPVRES))
    experiment_monitor.saveMon()
    window = visual.Window([HRES, VRES], allowGUI = True, monitor = experiment_monitor, units = 'height', color = 'white', fullScr = True, screen=0)

    return window

def read_procedural_csv():
    with open('Data/Procedures/' + SUBJECT_ID + 'proc.csv', 'rt') as procedure_file:
         procedural_file_reader =  csv.reader(procedure_file, delimiter = ',')
         procedural_file_list = list(procedural_file_reader)
    return procedural_file_list


def create_results_file():
    with open(SUBJECT_ID + "result.csv", 'w+t', newline='') as results_file:
        procedural_file_writer = csv.writer(results_file, delimiter= ',')
        procedural_file_writer.writerow(["ID", "Phase", "Alien Path", "Gender", "Tail", "Hands", "Feet", "Hair", "Mouth", "Eyes", "Context Path", "Context Path 2", "Left/Right", "Correct Answer", "ResponseTime", "Response", "Accuracy", "Confidence"])

    return 1

def create_buttons_from_dimensions(window, x_pos_array, y_pos_array, num_buttons):
    '''Handles detailed functions of creating buttons using dimension parameters.'''
    button_array = []
    for i in range (num_buttons):
        button_array.append(visual.Rect(window, width = 0.2, height = 0.05, lineWidth = .5, lineColor = 'black', pos = (x_pos_array[i], y_pos_array[0])))
    return button_array


def create_buttons(window):
    '''Creates buttons for all 4 different types of phases. Does this calling detailed button creation functions.'''
    study_buttons = create_buttons_from_dimensions(window, STUDY_BUTTON_X_POSITIONS, STUDY_BUTTON_Y_POSITIONS, NUM_STUDY_BUTTONS)
    memory_buttons = create_buttons_from_dimensions(window, MEMORY_BUTTONS_X_POSITIONS, MEMORY_BUTTONS_Y_POSITIONS, NUM_MEMORY_BUTTONS)
    feature_buttons = create_buttons_from_dimensions(window, FEATURE_BUTTONS_X_POSITIONS, FEATURE_BUTTONS_Y_POSITIONS, NUM_FEATURE_BUTTONS)
    general_buttons = create_buttons_from_dimensions(window, GENERAL_BUTTONS_X_POSITIONS, GENERAL_BUTTONS_Y_POSITIONS, NUM_GENERAL_BUTTONS)
    return study_buttons, memory_buttons, feature_buttons, general_buttons

def button_text_from_dimensions(window, text_content, x_pos_array, y_pos_array, num_buttons):
    '''Handles detailed functions of creating text on buttons using dimension parameters.'''
    text_array = []
    for i in range(num_buttons):
        text_array.append(visual.TextStim(window, pos = [x_pos_array[i], y_pos_array[0]], text = text_content[i], color='black', height = 0.025))
    return text_array

def create_buttons_text(window):
    '''Creates text on buttons used for all 4 phases of the experiment.'''
    '''Text content contains what will be displayed on the buttons for each trial, with the number of entries in each list for each phase
    corresponding to the number of buttons for that phase, corresponding to the buttons in left to right order.''' 
    study_text_content = ["Left", "Right"]
    memory_text_content = ["Sure, new", "Unsure, new", "Sure, old", "Unsure, old"]
    feature_text_content = ["Studied", "Tested", "New"]
    general_text_content = ["Left Context", "Middle Context", "Right Context"]

    study_button_text = button_text_from_dimensions(window, study_text_content, STUDY_BUTTON_X_POSITIONS, STUDY_BUTTON_Y_POSITIONS, NUM_STUDY_BUTTONS)
    memory_button_text = button_text_from_dimensions(window, memory_text_content, MEMORY_BUTTONS_X_POSITIONS, MEMORY_BUTTONS_Y_POSITIONS, NUM_MEMORY_BUTTONS)
    feature_button_text = button_text_from_dimensions(window, feature_text_content, FEATURE_BUTTONS_X_POSITIONS, FEATURE_BUTTONS_Y_POSITIONS, NUM_FEATURE_BUTTONS)
    general_button_text = button_text_from_dimensions(window, general_text_content, GENERAL_BUTTONS_X_POSITIONS, GENERAL_BUTTONS_Y_POSITIONS, NUM_GENERAL_BUTTONS)
    return study_button_text, memory_button_text, feature_button_text, general_button_text

'''def instruction_procedure(window, mouse, procedure):'''






def draw_context(window, context_position, context_path, image_size):
    '''Draws context(environment) alien is in on the screen.'''
    context = visual.ImageStim(window, image = FILEPATH + context_path, size = image_size, pos = context_position)
    context.draw()

def draw_alien(window, alien_position, alien_path):
    '''Draws alien on the screen.'''
    alien = visual.ImageStim(window, image = FILEPATH + alien_path, size = ALIEN_SIZE, pos = alien_position)
    alien.draw()

def get_response(window, mouse, button_array, clock, wait_time, num_options):
    '''Depending on the input mode(mouse, MRI buttons, etc.), gets a response from the user under the timed conditions(wait_time), and returns
        the response as well as the response time.'''
    response_time = wait_time
    response = 'No answer'

    if INPUT_MODE == 0:
        '''Mouse input'''
        if wait_time < 0:
            start_time = clock.getTime()
            '''When the user presses the mouse on one of the buttons, the function will get the response.'''
            while True:
                for i in range(0, len(button_array)):
                    if mouse.isPressedIn(button_array[i], buttons = [0]):
                        response_time = clock.getTime() - start_time
                        response = i
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
                        return response_time, response
            
            return wait_time, 'No answer'



    elif INPUT_MODE == 1 or INPUT_MODE == 2:
        '''Key input'''
        start_time = clock.getTime()
        '''Only difference between 2 input modes is that they use different keys.'''
        if INPUT_MODE == 1:
             keys = ['q', '1', '2', '3', '6', '7', '8']
        else:
             keys = ['q', 's', 'd', 'f', 'j', 'k', 'l']
        
        
        '''Gets response when a key is pressed. If the key pressed is 'q', the experiment ends. Otherwise, the appropriate response is collected.'''
        
        if wait_time < 0:
            selection = event.waitKeys(keyList = keys[0:num_options + 1], timeStamped=clock)
            if selection[0][0] == 'q':
                window.close()
                core.quit()
            for i in range(1, num_options + 1):
                if selection[0][0] == keys[i]:
                    response = i - 1
                    return selection[0][1] - start_time, response
        
        
        else:
            selection = event.waitKeys(maxWait=wait_time, keyList = keys[0:num_options + 1], timeStamped=clock)
            if selection is None:
                response = 'No answer'
                return [wait_time, response]
            if selection[0][0] == 'q':
                window.close()
                core.quit()
            for i in range(1, num_options + 1):
                if selection[0][0] == keys[i]:
                    response = i - 1
            return selection[0][1] - start_time, response


def record_procedure(procedure, response_time, response, accuracy, confidence):
    '''Records the results for each phase, which are the parameters to the function, in the appropriate CSV file.'''
    result_row = procedure
    result_row.extend((response_time, response, accuracy, confidence))
    with open(SUBJECT_ID + "result.csv", 'a', newline='') as procedure_file:
        procedure_csv_writer = csv.writer(procedure_file, delimiter=',')
        procedure_csv_writer.writerow(result_row)

def display_incorrect_message(window):
    window.flip()
    window.flip()
    incorrect_message = visual.TextStim(window, pos = (0, 0), text = "You missed the alien. Respond faster next time", color = 'black', height = 0.1)
    incorrect_message.draw()
    window.flip(clearBuffer=False)

def post_procedure(window, procedure, response_time, response, accuracy, confidence):
    record_procedure(procedure, response_time, response, accuracy, confidence)
    window.flip()
    window.flip()
    core.wait(0.5)

def delay(clock, delay_time):
    clock.reset()
    while clock.getTime() < delay_time:
        continue

def draw_buttons_and_text(button_array, text_array, num_buttons):
    for i in range(num_buttons):
        button_array[i].draw()
        text_array[i].draw()


def study_procedure(window, mouse, clock, procedure, study_buttons, context_list, alien_list, feature_list, button_text):
    '''In the study phase, the user sees the context for 1 second, before seeing the alien in the context for another second, and must
    answer which side the alien is on using the buttons. If they are correct, they will study the alien in its context for 4 more seconds.
    Otherwise, nothing happens.'''
    
    alien_path = procedure[2]
    context_path = procedure[10]

    '''Draws context'''
    draw_context(window, CONTEXT_ALIGN_CENTER_POS, context_path, CONTEXT_SIZE)
    window.flip(clearBuffer=False)
    
    '''1 second delay'''
    delay(clock, 1)
    
    '''Draws alien in context, along with buttons.'''
    alien_position = ALIEN_ALIGN_RIGHT_POS if (int(procedure[12]) == 1) else ALIEN_ALIGN_LEFT_POS
    draw_context(window, CONTEXT_ALIGN_CENTER_POS, context_path, CONTEXT_SIZE)
    draw_alien(window, alien_position, alien_path)
    draw_buttons_and_text(study_buttons, button_text, NUM_STUDY_BUTTONS)
    window.flip(clearBuffer=False)

    
    possible_answers = ["Left", "Right"]
    response_time, response = get_response(window, mouse, study_buttons, clock, 5, 2)
    accuracy = 0
    '''Response is correct if user answers the correct side the alien is on.'''
    if response == "No answer" or procedure[13] != possible_answers[int(response)]:
        accuracy = 0
        display_incorrect_message(window)
        delay(clock, 2)
    else:
        '''If the user answers correctly, display the alien and context for 4 more seconds.'''
        accuracy = 1
        draw_context(window, CONTEXT_ALIGN_CENTER_POS, context_path, CONTEXT_SIZE)
        draw_alien(window, ALIEN_ALIGN_CENTER_POS, alien_path)
        window.flip(clearBuffer=False)
        delay(clock, 4)
    
    post_procedure(window,procedure, response_time, response, accuracy, "NA")
    

def memory_procedure(window, mouse, clock, procedure, memory_buttons, alien_list, button_text):
    '''In this phase, the user is tested on his memory by being presented with an alien, and then answering whether or not that alien was
    encountered in the study phase. Additionally, he also answers whether or not he is sure or unsure about his answer.'''

    '''Draws alien and buttons on screen.'''
    alien_path = procedure[2]
    draw_alien(window, ALIEN_ALIGN_CENTER_POS, alien_path)
    draw_buttons_and_text(memory_buttons, button_text, NUM_MEMORY_BUTTONS)
    window.flip(clearBuffer=False)
    response_time, response = get_response(window, mouse, memory_buttons, clock, -1, 4)

    accuracy = 1 if (response < 2 and procedure[13] == "New") or (response >= 2 and procedure[13] == "Old") else 0
    confidence = 1 if (response == 0 or response == 2) else 0
    post_procedure(window, procedure, response_time, response, accuracy, confidence)
    


def draw_feature(window, feature_position, feature_path):
    feature = visual.ImageStim(window, image = FILEPATH + feature_path, size = FEATURE_SIZE, position = feature_position)
    feature.draw()

def get_feature(procedure):
    feature_index = 0
    gender = procedure[3]
    for i in range(4, 10):
        if procedure[i] != "NA":
            feature_index = i
            break
    feature_path = 'Features/f' + str(gender) + str(feature_index) + procedure[feature_index] + '.jpg'
    return feature_path
    
def feature_procedure(window, mouse, clock, procedure, feature_buttons, feature_list, button_text):
    '''Gets feature to be tested.'''
    feature_path = get_feature(procedure)
    '''Draws feature tested along with buttons.'''
    draw_feature(window, FEATURE_ALIGN_CENTER_POS, feature_path)
    draw_buttons_and_text(feature_buttons, button_text, NUM_FEATURE_BUTTONS)
    '''Gets response and records it.'''
    possible_answers = ["Studied, Tested, New"]
    response_time, response = get_response(window, mouse, feature_buttons, clock, -1, 3)
    accuracy = 1 if procedure[13] == int(response) else 0
    
    post_procedure(window, procedure, response_time, response, accuracy, "NA")
  


def general_procedure(window, mouse, clock, procedure, general_buttons, alien_list, context_list, button_text, new_context_list):
    '''In this phase, the user is tested on his ability to generalize his knowledge of aliens and contexts by being presented with an alien and
    2 contexts, and determining which context the alien is most likely to belong in, or neither.'''
    '''Draws alien and buttons.'''
    alien_path = procedure[2]
    draw_alien(window, ALIEN_ALIGN_CENTER_POS, alien_path)
    draw_buttons_and_text(general_buttons, button_text, NUM_GENERAL_BUTTONS)
    
    '''Picks contexts to be used from the file.'''
    context_path_1 = procedure[10]
    context_path_2 = procedure[11]
    
    chosen_context = new_context_list[random.randint(0, len(new_context_list) - 1)]
    
    possible_answers = ["Left", "Middle", "Right"]
    draw_context(window, GENERAL_CONTEXT_ALIGN_LEFT, context_path_1, REDUCED_CONTEXT_SIZE)
    draw_context(window, GENERAL_CONTEXT_ALIGN_CENTER, context_path_2, REDUCED_CONTEXT_SIZE)
    draw_context(window, GENERAL_CONTEXT_ALIGN_RIGHT, chosen_context, REDUCED_CONTEXT_SIZE)

    window.flip(clearBuffer=False)

    response_time, response = get_response(window, mouse, general_buttons, clock, -1, 3)
    accuracy = 1 if procedure[13] == possible_answers[int(response)] else 0
    
    post_procedure(window, procedure, response_time, response, accuracy, "NA")

def import_non_studied_contexts():
    '''For the general test, the program pulls contexts that haven't been studied by the user to be tested.'''
    new_context_list = ["fire", "grassland", "desert"]
    context_path_list = []
    for context in new_context_list:
        context_path_list.append("Images/Contexts/" + context + ".jpg")
    return context_path_list


def main():


    '''First, we read information from CSV files to get images in each trial'''
    '''Then, we get the images and store them for each trial type'''
    '''We run the experiment and get the response time + accuracy'''
    '''Write the results to a file'''
    window = create_window()
    '''Determines visibility of mouse based on input mode'''
    is_visible = False if (INPUT_MODE != 0) else True
    mouse = event.Mouse(visible=is_visible,  newPos = None, win=window)
    
    '''Starts the clock'''
    clock = core.Clock()

    procedural_file_list = read_procedural_csv()

    new_session = create_results_file()

    new_contexts = import_non_studied_contexts()

    
    context_list = {}

    alien_list = {}

    feature_list = [{} for i in range(NUM_FEATURES)]

    
    study_buttons, memory_buttons, feature_buttons, general_buttons = create_buttons(window)

    study_button_text, memory_button_text, feature_button_text, general_button_text = create_buttons_text(window)

    for procedure in procedural_file_list:
        if procedure[1] == 'Instruct':
            instruction_procedure(window, mouse, procedure, "")
        elif procedure[1] == 'Study':
            study_procedure(window, mouse, clock,  procedure, study_buttons, context_list, alien_list, feature_list, study_button_text)
        elif procedure[1] == 'MemoryTest':
            memory_procedure(window, mouse, clock, procedure, memory_buttons, alien_list, memory_button_text)
        elif procedure[1] == 'FeatureTest':
            feature_procedure(window, mouse, clock, procedure, feature_buttons, feature_list, feature_button_text)
        elif procedure[1] == 'GeneralTest':
            general_procedure(window, mouse, clock, procedure, general_buttons, alien_list, context_list, general_button_text, new_contexts)




if __name__ == '__main__':
    main()