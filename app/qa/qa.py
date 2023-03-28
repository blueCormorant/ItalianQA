from transformers import AutoTokenizer, AutoModelForQuestionAnswering
import torch

DEFAULT_CONTEXT = """Mentre era ospite ad Angera nella casa dell'amica Teresa Castiglioni, Volta scoprì il metano nella palude dell'isolino Partegora. Provando a smuovere il fondo con l'aiuto di un bastone vide che risalivano delle bolle di gas e le raccolse in bottiglie. Diede a questo gas il nome di "aria infiammabile di palude" e scoprì che poteva essere incendiato sia per mezzo di una candela accesa sia mediante una scarica elettrica: dedusse che il gas si formava nella decomposizione di sostanze animali e vegetali."""

DEFAULT_QUESTION = """Dove ha scoperto il gas metano Volta?"""


class QuestionAnswerer(object):

    def __init__(self):
        self.tokenizer = self.load_tokenizer()
        self.model = self.load_model()
        self.default_question = DEFAULT_QUESTION
        self.default_context = DEFAULT_CONTEXT
      
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

