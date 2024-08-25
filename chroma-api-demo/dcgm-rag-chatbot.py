import sys
sys.path.append('..')

import dclib_py.ai.gemini as dcgm

def main():
    ragchatbot = dcgm.RAGChatBot()
    
    DOCUMENT1 = "Gemini is the result of large-scale collaborative efforts by teams across Google, including our colleagues at Google Research. It was built from the ground up to be multimodal, which means it can generalize and seamlessly understand, operate across and combine different types of information including text, code, audio, image and video."
    DOCUMENT2 = "We designed Gemini to be natively multimodal, pre-trained from the start on different modalities. Then we fine-tuned it with additional multimodal data to further refine its effectiveness. This helps Gemini seamlessly understand and reason about all kinds of inputs from the ground up, far better than existing multimodal models — and its capabilities are state of the art in nearly every domain."
    DOCUMENT3 = "Gemini has the most comprehensive safety evaluations of any Google AI model to date, including for bias and toxicity. We’ve conducted novel research into potential risk areas like cyber-offense, persuasion and autonomy, and have applied Google Research’s best-in-class adversarial testing techniques to help identify critical safety issues in advance of Gemini’s deployment."
    ragchatbot.documents = [DOCUMENT1, DOCUMENT2, DOCUMENT3]
    ragchatbot.subject = 'Gemini intro'

    ragchatbot.ragchat()

if __name__ == '__main__':
    main()