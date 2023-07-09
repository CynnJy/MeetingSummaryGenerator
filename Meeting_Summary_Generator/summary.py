# Summary file
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import nltk
import torch

class Sumarizer:

    def summary(file):
        text = file.strip()

        checkpoint = "facebook/bart-large-cnn"

        # If Detect CUDA, System Run in Cuda
        # Else System Run in CPU
        touch_device = 'cuda' if torch.cuda.is_available() else 'cpu'

        tokenizer = AutoTokenizer.from_pretrained(checkpoint)
        model = AutoModelForSeq2SeqLM.from_pretrained(checkpoint)

        tokenizer.model_max_length
        tokenizer.max_len_single_sentence
        tokenizer.num_special_tokens_to_add()

        nltk.download('punkt')

        # Split The Text Data into list of Sentence
        sentences = nltk.tokenize.sent_tokenize(text)

        max([len(tokenizer.tokenize(sentence)) for sentence in sentences])
        
        # Declare Variable for the coming progress
        length = 0
        chunk = ""
        chunks = []
        count = -1

        for sentence in sentences:
            count += 1
            # Add the no. of sentence tokens to the length counter
            combined_length = len(tokenizer.tokenize(sentence * 5)) + length

            # If it doesn't exceed
            if combined_length <= tokenizer.max_len_single_sentence:
                chunk += sentence + " "     # add the sentence to the chunk
                length = combined_length    # update the length counter

                # If it is the last sentece
                if count == len(sentences) - 1:
                    chunks.append(chunk.strip())    # save the chunk
            else:
                chunks.append(chunk.strip())        # save the chunk

                # Reset
                length = 0
                chunk = ""

                # Take Care of the overflow sentence
                chunk += sentence + " "
                length = len(tokenizer.tokenize(sentence))

        [len(tokenizer.tokenize(c)) for c in chunks]
        [len(tokenizer(c).input_ids) for c in chunks]
        sum([len(tokenizer(c).input_ids) for c in chunks])
        len(tokenizer(text).input_ids)
        
        inputs = [tokenizer(chunk, return_tensors="pt") for chunk in chunks]

        # Declare a final summary result
        summaryResult = ' '

        # Generate Summary
        # Each of summary will add into summaryResult
        for input in inputs:
            output = model.generate(**input)
            summary = tokenizer.decode(*output, skip_special_tokens=True)
            summaryResult += " " + summary

        return summaryResult


