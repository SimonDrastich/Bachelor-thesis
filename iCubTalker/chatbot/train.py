from rasa_nlu.training_data import load_data
from rasa_nlu.model import Trainer
from rasa_nlu import config
from rasa_nlu.model import Interpreter
import spacy 

nlp = spacy.load('en')
def train_nlu(data_json, config_file, model_dir):
 training_data = load_data(data_json)
 trainer = Trainer(config.load(config_file))
 trainer.train(training_data)
 model_directory = trainer.persist(model_dir, fixed_model_name =
'iCubbot')
    
def predict_intent(text):
 interpreter = Interpreter.load('../models/nlu/default/iCubbot')
 print(interpreter.parse(text))
    
train_nlu('./data/data.json', 'config.json', '../models/nlu')
