from transformers import DistilBertTokenizer, DistilBertForQuestionAnswering
import torch
from query_chunk import find_k_most_similar_chunk
from database_handling import init_database, get_chunks_by_ids

def build_context(text_chunks):
    with open("prompt_template.txt") as f:
        context = f.read()
    for i,chunks in enumerate(text_chunks):
        context= context + f"context{i+1}\n" + chunks + "\n"
    return context

def main():

    tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased-distilled-squad')
    model = DistilBertForQuestionAnswering.from_pretrained('distilbert-base-uncased-distilled-squad')
    conn=init_database("chunck_database.db")
    print("How can I help you ? (type 'exit' to end)")

    while True:
        # Prendre l'entrée de l'utilisateur
        user_input = input("You: ")
        
        if user_input.lower() == "exit":
            break
        
        chunk_ids=find_k_most_similar_chunk(user_input, conn, k=3, batch_size=15)
        text_chunks = get_chunks_by_ids(conn,chunk_ids)
        context=build_context(text_chunks)
        print(context)
        question = user_input

        inputs = tokenizer(question, context, return_tensors="pt")
        with torch.no_grad():
            outputs = model(**inputs)

        answer_start_index = torch.argmax(outputs.start_logits)
        answer_end_index = torch.argmax(outputs.end_logits)

        predict_answer_tokens = inputs.input_ids[0, answer_start_index : answer_end_index + 1]
        print("Assistant:\n",tokenizer.decode(predict_answer_tokens))


main()