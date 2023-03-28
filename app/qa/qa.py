from transformers import AutoTokenizer, AutoModelForQuestionAnswering
import torch


class QuestionAnswerer(object):

    def __init__(self):
        self.tokenizer = self.load_tokenizer()
        self.model = self.load_model()

    def load_tokenizer(self):
        return AutoTokenizer.from_pretrained("mrm8488/bert-italian-finedtuned-squadv1-it-alfa")

    def load_model(self):
        return AutoModelForQuestionAnswering.from_pretrained("mrm8488/bert-italian-finedtuned-squadv1-it-alfa")

    def answer_question(self, context, question):
        inputs = self.tokenizer(question, context, return_tensors="pt")

        with torch.no_grad():
            outputs = self.model(**inputs)

        answer_start_index = outputs.start_logits.argmax()
        answer_end_index = outputs.end_logits.argmax()

        predict_answer_tokens = inputs.input_ids[0, answer_start_index : answer_end_index + 1]
        return self.tokenizer.decode(predict_answer_tokens)

