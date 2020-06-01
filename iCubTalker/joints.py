import re


def find_joint(message, limb, vektor_limb, dispatcher):
    torso_directions = {"X-left": -50, "X-right": 50, "Y-left": 30, "Y-right": -30, "Z-backward": -10, "Z-forward": 68}
    head_directions = {"X-left": 55, "X-right": -55, "Y-left": -60, "Y-right": 60, "Z-backward": 30, "Z-forward": -40}
    legs_directions = {"X-leg-outside": 77, "X-leg-inside": -79, "Y-leg-outside": 90, "Y-leg-inside": -1,
                       "Z-leg-backward": -30, "Z-leg-forward": 90,
                       "Z-knee-forward": 14, "Z-knee-backward": -120, "Z-tiptoe-forward": -19, "Z-tiptoe-backward": 43,
                       "Y-tiptoe-outside": 22, "Y-tiptoe-inside": -22}
    arms_directions = {"Z-arm-forward": -94, "Z-arm-backward": 10, "Y-arm-outside": 160, "Y-arm-inside": -1,
                       "X-arm-outside": -36, "X-arm-inside": 79, "Z-elbow-forward": 105, "Z-elbow-backward": 18,
                       'Z-wrist-backward': -1, 'Z-wrist-forward': -87, 'Y-wrist-inside': -18, 'Y-wrist-outside': 37}
    directions = {'torso': torso_directions, 'head': head_directions, "legs": legs_directions, "arms": arms_directions}

    torso_joints = {"X": 0, "Y": 1, "Z": 2}
    head_joints = {"X": 2, "Y": 1, "Z": 0}
    legs_joints = {"X-leg": 2, "Y-leg": 1, "Z-leg": 0, "Z-knee": 3, "Y-tiptoe": 5, "Z-tiptoe": 4}
    arms_joints = {"X-arm": 2, "Y-arm": 1, "Z-arm": 0, "Y-elbow": 4, "Z-elbow": 3, "Y-wrist": 6, 'Z-wrist': 5}
    joints = {'torso': torso_joints, 'head': head_joints, "legs": legs_joints, "arms": arms_joints}

    regex = {"X-torso": 'otoc sa|otoc', "Y-torso": 'nahni sa|natiahni|natiahnut|naklon|nahni',
             "Z-torso": 'predklon sa|predklon|zaklon sa|zaklonit|zaklon',
             "X-head": 'otoc sa|otoc', "Y-head": 'nahni sa|natiahni|natiahnut|naklon|nahni',
             "Z-head": 'predklon sa|predklon|zaklon sa|zaklonit|zaklon',
             "X-legs": 'otoc|vytoc', "Y-legs": 'strany|bok|boku', "Z-legs": 'zdvihni|vystri|ohni|zohni|prepni',
             "X-arms": "otoc", "Y-arms": 'strany|bok|vytoc', "Z-arms": "zdvihni|zohni|vystri"}

    forward_limb = {'head': 'dopredu|predklon|predklon sa', 'torso': 'dopredu|predklon|predklon sa',
                    'legs': 'vystri|zdvihni', 'arms': 'dopredu|hore|pred seba|k sebe|predseba|hora|nahor'}
    backward_limb = {'head': 'dozadu|zaklon|zaklon sa', 'torso': 'dozadu|zaklon|zaklon sa',
                     'legs': 'dozadu|zohni|ohni|prepni', 'arms': 'dozadu|dole|naspat|od seba|vystri'}

    axis = None
    for ax in "XYZ":
        r = re.compile(regex[ax + '-' + limb])
        if r.search(message):
            axis = ax
            break

    if not axis:
        dispatcher.utter_message('Ospravedlň ma, ale neporozumel som tomuto príkazu')
        return

    direction = 1
    axis += specific_joint(message, limb)
    joint = joints[limb][axis]

    if 'Z' not in axis:
        left = re.compile('dolava|vlavo|lava')
        right = re.compile('doprava|vpravo|prava')
        inside = re.compile('dnu|k telu|k sebe')
        outside = re.compile('von|bok|strany|od tela')

        if left.search(message):
            direction = directions[limb][axis + "-left"]
        elif right.search(message):
            direction = directions[limb][axis + "-right"]
        elif inside.search(message):
            direction = directions[limb][axis + "-inside"]
        elif outside.search(message):
            direction = directions[limb][axis + "-outside"]
    else:
        forward = re.compile(forward_limb[limb])
        backward = re.compile(backward_limb[limb])

        if forward.search(message):
            direction = directions[limb][axis + "-forward"]
        elif backward.search(message):
            direction = directions[limb][axis + "-backward"]

    side = True
    if limb == 'arms' or limb == 'legs':
        side = side_to_set(message)

    direction, overangle = angle_specified(message, direction, vektor_limb, joint)
    return joint, direction, side, overangle


def angle_specified(message, direction, vektor_limb, joint):
    specified = re.search('o [1-9]+[0-9]* stupnov', message)
    ninety_degree = re.search('pravy|praveho', message)
    if ninety_degree:
        angle = 90
        if direction < 0:
            angle = -90
        if abs(direction) > 90:
            return angle, False
        else:
            return direction, True

    if specified:
        angle = int(re.search(r'\d+', message).group())

        if len(vektor_limb) == 2:
            side = side_to_set(message)
            left_overangle = right_overangle = False

            if (0 < direction < angle + vektor_limb[0][joint]) or (0 > direction > -angle + vektor_limb[0][joint]):
                left_overangle = True
            if (0 < direction < angle + vektor_limb[1][joint]) or (0 > direction > -angle + vektor_limb[1][joint]):
                right_overangle = True


            if (side == 'left' and left_overangle) or (side == 'right' and right_overangle) or (side == 'both' and (left_overangle or right_overangle)):
                return direction, True


            else:
                if side == 'left':
                    return vektor_limb[0][joint] + direction / abs(direction) * abs(angle), False
                elif side =='right':
                    return vektor_limb[1][joint] + direction / abs(direction) * abs(angle), False
                elif side == 'both':
                    return vektor_limb[0][joint] + direction / abs(direction) * abs(angle), False


        if len(vektor_limb) == 1:
            limb_overangle = False
            if (direction > 0 and angle + vektor_limb[0][joint] > direction) or (direction < 0 and -angle + vektor_limb[0][joint] < direction):
                limb_overangle = True
            if limb_overangle:
                return direction, True
            else:
                return vektor_limb[0][joint] + direction / abs(direction) * abs(angle), False

    return direction, False


def specific_joint(message, limb):
    if limb == 'legs':
        tiptoe = re.compile('spicka|chodidlo|spicke|spicku|chodidla')
        knee = re.compile('koleno|kolene|kolena')

        if tiptoe.search(message):
            return '-tiptoe'
        elif knee.search(message):
            return '-knee'
        else:
            return '-leg'

    if limb == 'arms':
        elbow = re.compile('laktom|laket|loket|lakti|lakt')
        wrist = re.compile('zapastie|zapas|predlaktie|predlaktim')

        if elbow.search(message):
            return '-elbow'
        elif wrist.search(message):
            return '-wrist'
        else:
            return '-arm'

    return ''


def repetition_specified(message):
    repetition = re.search('[1-9]+[0-9]* krat', message)
    if repetition:
        count = int(re.search(r'\d+', message).group())
        return count
    return 1


def side_to_set(message):
    sides = {'left': 'lava|lavacka|lavou|lavu', 'right': 'pravou|pravacka|prava',
             'both': 'oboma|oboje|dvoma|obidve|spolu|obe|ruky|nohy|nohami|rukami|chodidlami|spickami|kolenami|laktami|kolena'}
    for side in sides.keys():
        r = re.compile(sides[side])
        if r.search(message):
            return side
    return 'right'
