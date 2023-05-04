from transformers import pipeline


model = pipeline("text-generation", model="gpt2")

if __name__ == '__main__':
    sentence = model("Gum in my hair.",
                     do_sample=True, top_k=50,
                     temperature=0.9, max_length=100)
    for i in sentence:
        print(i["generated_text"])

