from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from ast import literal_eval as make_tuple
from speak import speak
from rasa_core_sdk import Action

import simplejson as json
import os
import yarp
import re
import time
import robot
import joints

yarp.Network.init()
icub = robot.iCub()
moves_to_save = {
    "head": [],
    "torso": [],
    "left_leg": [],
    "right_leg": [],
    "left_arm": [],
    "right_arm": []
}
greeted = False

with open('moves.json', "r+") as moves_file:
    complex_moves_json = json.loads(moves_file.read())


class Mimika(Action):
    def name(self):
        return "mimika"

    def run(self, dispatcher, tracker, domain):
        if len(tracker.latest_message['entities']) > 0:
            entity = tracker.latest_message['entities'][0]['entity']
            icub.emotions.set(entity)


class Pozdrav(Action):
    def name(self):
        return "pozdrav"

    def run(self, dispatcher, tracker, domain):
        global greeted
        if greeted:
            dispatcher.utter_template("utter_rozlucenie", tracker)
        else:
            dispatcher.utter_template("utter_stretnutie", tracker)

        greeted = not greeted
        icub.emotions.set('hap')
        icub.left_leg.set((0, 0, 0, 0, 0, 0))
        icub.right_leg.set((0, 0, 0, 0, 0, 0))
        icub.head.set((0, 0, 0, 0, 0, 0))
        icub.torso.set((0, 0, 0))
        icub.left_arm.set((0, 17, 0, 50, 0, 0, 0, 59, 20, 20, 20, 10, 10, 10, 10, 10))

        for i in range(0, 2):
            icub.right_arm.set((-85, 92, 0, 105, 0, 0, 0, 59, 20, 20, 20, 10, 10, 10, 10, 10))
            time.sleep(1.5)
            icub.right_arm.set((-85, 92, 0, 66, 0, 0, 0, 59, 20, 20, 20, 10, 10, 10, 10, 10))
            time.sleep(1.5)
        icub.right_arm.set((0, 17, 0, 50, 0, 0, 0, 59, 20, 20, 20, 10, 10, 10, 10, 10))


class Pohyb_telom(Action):
    def name(self):
        return "pohyb_telom"

    def run(self, dispatcher, tracker, domain):
        message = tracker.latest_message["text"]
        torso = list(icub.torso.get())
        parsed = joints.find_joint(message, 'torso', [tuple(torso)], dispatcher)

        if parsed:
            joint = parsed[0]
            direction = parsed[1]
            overangle = parsed[3]
        else:
            return

        if overangle:
            dispatcher.utter_template("utter_limit", tracker)

        torso[joint] = direction
        icub.torso.set(tuple(torso))


class Pohyb_hlavou(Action):
    def name(self):
        return "pohyb_hlavou"

    def run(self, dispatcher, tracker, domain):
        message = tracker.latest_message["text"]
        head = list(icub.head.get())
        parsed = joints.find_joint(message, 'head', [tuple(head)], dispatcher)
        if parsed:
            joint = parsed[0]
            direction = parsed[1]
            overangle = parsed[3]
        else:
            return

        if overangle:
            dispatcher.utter_template("utter_limit", tracker)

        head[joint] = direction
        icub.head.set(tuple(head))


class Pohyb_nohami(Action):
    def name(self):
        return "pohyb_nohami"

    def run(self, dispatcher, tracker, domain):
        message = tracker.latest_message["text"]
        left_leg = list(icub.left_leg.get())
        right_leg = list(icub.right_leg.get())
        vektor_limb = [tuple(left_leg), tuple(right_leg)]
        parsed = joints.find_joint(message, 'legs', vektor_limb, dispatcher)
        if parsed:
            joint, direction, side_to_move, overangle = parsed
        else:
            return
        if overangle:
            dispatcher.utter_template("utter_limit", tracker)

        left_leg[joint] = direction
        right_leg[joint] = direction

        if side_to_move == 'left':
            icub.left_leg.set(tuple(left_leg))
        elif side_to_move == 'both':
            icub.left_leg.set(tuple(left_leg))
            icub.right_leg.set(tuple(right_leg))
        else:
            icub.right_leg.set(tuple(right_leg))


class Pohyb_rukami(Action):
    def name(self):
        return "pohyb_rukami"

    def run(self, dispatcher, tracker, domain):
        message = tracker.latest_message["text"]
        left_arm = list(icub.left_arm.get())
        right_arm = list(icub.right_arm.get())
        vektor_limb = [tuple(left_arm), tuple(right_arm)]
        parsed = joints.find_joint(message, 'arms', vektor_limb, dispatcher)
        if parsed:
            joint, direction, side_to_move, overangle = parsed
        else:
            return
        if overangle:
            dispatcher.utter_template("utter_limit", tracker)

        left_arm[joint] = direction
        right_arm[joint] = direction

        if side_to_move == 'left':
            icub.left_arm.set(tuple(left_arm))
        elif side_to_move == 'both':
            icub.left_arm.set(tuple(left_arm))
            icub.right_arm.set(tuple(right_arm))
        else:
            icub.right_arm.set(tuple(right_arm))


class Povedz(Action):
    def name(self):
        return "povedz"

    def match(self, pattern, text):
        search = re.search(pattern, text)
        if search is None:
            self.groups = []
            return False
        else:
            self.groups = search.groups()
            return True

    def matched(self):
        return self.groups

    def run(self, dispatcher, tracker, domain):
        message = tracker.latest_message["text"]
        if self.match(r'povedz (.*)', message):
            speak(self.matched()[0])


class Krok(Action):
    def name(self):
        return "krok"

    def roundTuple(self, vector):
        return tuple([round(i, 2) for i in vector])

    def run(self, dispatcher, tracker, domain):
        moves_to_save['head'].append(str(self.roundTuple(icub.head.get())))
        moves_to_save['torso'].append(str(self.roundTuple(icub.torso.get())))
        moves_to_save['left_leg'].append(str(self.roundTuple(icub.left_leg.get())))
        moves_to_save['right_leg'].append(str(self.roundTuple(icub.right_leg.get())))
        moves_to_save['left_arm'].append(str(self.roundTuple(icub.left_arm.get())))
        moves_to_save['right_arm'].append(str(self.roundTuple(icub.right_arm.get())))
        dispatcher.utter_template("utter_krok", tracker)


class Preucenie(Action):
    def name(self):
        return "preucenie"

    def run(self, dispatcher, tracker, domain):
        global complex_moves_json

        message = tracker.latest_message["text"]
        parsed_text = message[message.find('ako') + 4:]
        new_training_data = {'text': parsed_text, 'intent': 'komplexny_pohyb', 'entities': []}

        with open('./chatbot/Data/data.json', "r+") as json_file:
            training_data = json.loads(json_file.read())
            training_data['rasa_nlu_data']['common_examples'].append(new_training_data)
            json_file.seek(0)
            json_file.truncate()
            json.dump(training_data, json_file)

        with open('moves.json', "r+") as moves_to_save_file:
            complex_moves_json['moves'][parsed_text] = moves_to_save
            moves_to_save_file.seek(0)
            moves_to_save_file.truncate()
            json.dump(complex_moves_json, moves_to_save_file)

        with open('moves.json', "r+") as new_moves_file:
            new_json = json.loads(new_moves_file.read())
        complex_moves_json = new_json

        os.chdir("C:/Users/Arliasis/Desktop/Bakalarka/iCubTalker/chatbot")
        os.startfile("run-nlu-training.bat")
        os.chdir("C:/Users/Arliasis/Desktop/Bakalarka/iCubTalker")
        dispatcher.utter_template("utter_preucenie", tracker)

        for i in moves_to_save.keys():
            moves_to_save[i].clear()


class Komplexny_pohyb(Action):
    def name(self):
        return "komplexny_pohyb"

    def run(self, dispatcher, tracker, domain):
        message = tracker.latest_message["text"]
        moves = None
        repeat = joints.repetition_specified(message)
        limbs = ['head', 'torso', 'left_leg', 'right_leg', 'left_arm', 'right_arm']

        for command in complex_moves_json['moves'].keys():
            parser = re.compile(command)
            if parser.search(message):
                moves = complex_moves_json['moves'][command]
                break

        if not moves:
            dispatcher.utter_template("utter_komplexne_pohyby", tracker)
            return

        for repetitions in range(0, repeat):
            for i in range(len(moves['head'])):
                is_moving = True
                icub.head.set(tuple(make_tuple(moves['head'][i])))
                icub.torso.set(tuple(make_tuple(moves['torso'][i])))
                icub.left_leg.set(tuple(make_tuple(moves['left_leg'][i])))
                icub.right_leg.set(tuple(make_tuple(moves['right_leg'][i])))
                icub.left_arm.set(tuple(make_tuple(moves['left_arm'][i])))
                icub.right_arm.set(tuple(make_tuple(moves['right_arm'][i])))
                timer = 3
                while is_moving and timer:
                    is_moving = False
                    for limb in limbs:
                        if icub.is_moving(moves[limb][i], limb):
                            is_moving = True
                    time.sleep(1)
                    timer -= 1
