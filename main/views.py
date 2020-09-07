from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import InputForm, ResultForm, SaveForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView,DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Summarized

#Text Summarization Tools
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
import string
from heapq import nlargest

# Create your views here.
class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('main:homepage')

def homepage(request):
	try:
		request.session['edit']
		inp = request.session['input']
		del request.session['edit']
	except:
		try:
			inp = ""
			del request.session['input']
			del request.session['output']
		except:
			pass
	if request.method == "POST":
		form = InputForm(request.POST)
		if form.is_valid():
			input_field = form.cleaned_data.get('text_input')
			request.session['output'] = text_summ(input_field)
			request.session['input'] = request.POST.get('text_input')
			return redirect('main:result')

	form = InputForm
	return render(request = request,
                  template_name='home.html',
                  context={"form":form,"inp":inp,}
                  )

def result(request):
	return render(request = request,
                  template_name='result.html')

def edit_input(request):
	request.session['edit'] = "true"
	return homepage(request)

def text_summ(text):
	#Store stopwords in list
	stopwords = list(STOP_WORDS)

	#Load spacy's pre-trained model
	nlp = spacy.load('en_core_web_sm')

	#Breaks para into tokens using spacy
	doc = nlp(text)

	#Convert each token from spacy.tokens.token.Token to str and store in a list
	tokens = [token.text for token in doc]

	#Add \n to exiating punctuation to identify new lines
	punctuation = string.punctuation
	punctuation = punctuation + '\n'

	#Store each word and its respective frequencies
	word_frequencies = {}
	for word in doc:
	    if word.text.lower() not in stopwords:
	        if word.text.lower() not in punctuation:
	            if word.text not in word_frequencies.keys():
	                word_frequencies[word.text] = 1
	            else:
	                word_frequencies[word.text] += 1

	#Compute max freq among all words
	max_frequency = max(word_frequencies.values())

	#Associate each word with its freq ratio by dividing with max freq
	for word in word_frequencies.keys():
	    word_frequencies[word] = word_frequencies[word]/max_frequency

	#Store each sentence 
	sentence_tokens = [sent for sent in doc.sents]

	#Store each sentence along with the score computed by adding the frequencies of all the words in that particular sentence
	sentence_scores = {}
	for sent in sentence_tokens:
	    for word in sent:
	        if word.text.lower() in word_frequencies.keys():
	            if sent not in sentence_scores.keys():
	                sentence_scores[sent] = word_frequencies[word.text.lower()]
	            else:
	                sentence_scores[sent] += word_frequencies[word.text.lower()]

	#Considering only 30% of sentences and converting to integer value to consider whole sentences
	select_length = int(len(sentence_tokens)*0.3)

	#Storing top 30% sentences based on their scores
	#key = sentence_scores.get ==> Dictionary keys ordered by their values
	summary = nlargest(select_length, sentence_scores, key = sentence_scores.get)

	#Converting each sentence type from spacy.tokens.span.Span to str and store in a list
	final_summary = [word.text for word in summary]

	#Joining each sentence with ' '
	summary = ' '.join(final_summary)

	#Return Result
	return summary

class SaveResult(LoginRequiredMixin,CreateView):
    form_class = SaveForm
    template_name = 'save_result.html'
    success_url = '/'

    def form_valid(self, form): #To save manager as logged in user which was not displayed in form
        instance = form.save(commit=False)
        instance.user = self.request.user
        instance.text_input = self.request.session['input']
        instance.text_output = self.request.session['output']
        instance.create()
        instance.save()
        messages.success(self.request, 'Your Summarization has been successfully saved!')
        return redirect('main:homepage')

class PrevSummarizations(LoginRequiredMixin,ListView):
    template_name = 'Summarizations.html'
    model = Summarized
    context_object_name = 'summ' #Context name used in template

    def get_queryset(self): #To show summarizations associated to logged in user only and not all
        summ = super().get_queryset()
        return summ.filter(user=self.request.user)

class DelSummarization(LoginRequiredMixin,DeleteView):
    model = Summarized
    template_name = 'delete.html'
    context_object_name = 'summarized'
    success_url = reverse_lazy('main:your_summarizations')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Your selected Summarization has been successfully deleted!')
        return super().delete(self, request, *args, **kwargs)

class DetailSummarization(LoginRequiredMixin,DetailView):
    template_name = 'detail.html'
    model = Summarized
    context_object_name = 'summarized' #Context name used in template