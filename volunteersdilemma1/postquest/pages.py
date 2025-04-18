from ._builtin import Page


class Questionnaire1(Page):
    form_model = 'player'
    form_fields = ['mpc1', 'mpc2', 'mpc3', 'mpc4', 'mpc5', 'mpc6', 'mpc7']
    
    def vars_for_template(self):
        oppdict = {
            'cat': 'dog',
            'dog': 'cat'
        }

        pet_choice = self.player.participant.vars.get('pet_choice')

        questions = {
            "mpc1": f"As a {pet_choice} lover, I felt I was on my own within my 3-person group.",
            "mpc2": "I felt I had something in common with the 2 other members of my group.",
            "mpc3": "I feel positively about people with my animal preference.",
            "mpc4": f"I feel negatively about people with {oppdict[pet_choice]} preference.",
            "mpc5": "I believe the preference for cats/dogs reveals something meaningful about people.",
            "mpc6": f"As a {pet_choice} lover, I felt I had a high status within my 3-person group.",
            "mpc7": f"As a {pet_choice} lover, I felt I had a low status within my 3-person group."
        }
        return {"questions": questions}

class Questionnaire2(Page):
    form_model = 'player'
    form_fields = [
        'stq1', 'stq2', 'stq3', 'stq4', 'stq5', 'stq6', 'stq7', 'stq8', 'stq9', 'stq10',
        'stq11', 'stq12', 'stq13', 'stq14', 'stq15', 'stq16', 'stq17', 'stq18', 'stq19', 'stq20',
        'stq21', 'stq22', 'stq23', 'stq24'
    ]
    
    def vars_for_template(self):
        questions = {
            "stq1": "I often put other people's needs before my own.",
            "stq2": "I find it difficult to be separated from people I love.",
            "stq3": "I am very sensitive to the effects I have on the feelings of other people.",
            "stq4": "I am very sensitive to criticism by others.",
            "stq5": "I worry a lot about hurting or offending other people.",
            "stq6": "It is hard for me to break off a relationship even if it is making me unhappy.",
            "stq7": "I am easily persuaded by others.",
            "stq8": "I try to please other people too much.",
            "stq9": "I find it difficult if I have to be alone all day.",
            "stq10": "I often feel responsible for solving other people's problems.",
            "stq11": "It is very hard for me to get over the feeling of loss when a relationship has ended.",
            "stq12": "It is very important to me to be liked or admired by others.",
            "stq13": "I feel I have to be nice to other people.",
            "stq14": "I like to be certain that there is somebody close I can contact in case something unpleasant happens to me.",
            "stq15": "I am too apologetic to other people.",
            "stq16": "I am very concerned with how people react to me.",
            "stq17": "I get very uncomfortable when I'm not sure whether or not someone likes me.",
            "stq18": "It is hard for me to say 'no' to other people's requests.",
            "stq19": "I become upset when something happens to me and there's nobody around to talk to.",
            "stq20": "I am most comfortable when I know my behavior is what others expect of me.",
            "stq21": "I often let people take advantage of me.",
            "stq22": "I become very upset when a friend breaks a date or forgets to call me as planned.",
            "stq23": "I judge myself based on how I think others feel about me.",
            "stq24": "It is hard for me to let people know when I am angry with them."
        }
        return {"questions": questions}

class Questionnaire3(Page):
    form_model = 'player'
    form_fields = ['bfp1', 'bfp2', 'bfp3', 'bfp4', 'bfp5', 'bfp6', 'bfp7', 'bfp8', 'bfp9', 'bfp10', 'bfp11']
    
    def vars_for_template(self):
        questions = {
            "bfp1": "...is reserved.",
            "bfp2": "...is generally trusting.",
            "bfp3": "...tends to be lazy.",
            "bfp4": "...is relaxed, handles stress well.",
            "bfp5": "...has few artistic interests.",
            "bfp6": "...is outgoing, sociable.",
            "bfp7": "...tends to find fault with others.",
            "bfp8": "...does a thorough job.",
            "bfp9": "...gets nervous easily.",
            "bfp10": "...has an active imagination.",
            "bfp11": "...is sometimes rude to others."
        }
        return {"questions": questions}
    
class Debrief(Page):
    pass

page_sequence = [
    Questionnaire1,
    Questionnaire2,
    Questionnaire3,
    Debrief
]
