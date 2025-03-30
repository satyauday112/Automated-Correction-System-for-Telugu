import pickle
import argparse
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer,TfidfVectorizer
import sys

stop_words = ['ఇది', 'ఇవన్నీ', 'వచ్చ', 'వెనుక', 'మేరే', 'అయితే మరియు', 'ఒక', 'ఒకసారి', 'టి', 'దయచేసి', 'అంటుంది', 'మరల', 'ఆతని', 'లో', 'ఉందారు', 'అయన', 'అందుకు', 'ఇప్పుడు', 'అదే', 'అయితే', 'చేస్తున్నాడు', 'పైన', 'సారీ', 'బాట', 'ఏడు', 'అందరి', 'తొమ్మిది', 'ఇవి', 'సాయంత్రం', 'ఆగని', 'మీరు', 'మూడు', 'కాదను', 'పని', 'ఎవరి', 'ఉండదు', 'ఉందా', 'పడను', 'ధన్యవాదాలు', 'మీరు ధన్యవాదాలు చెప్పాలి', 'పది', 'దయచేసి చేయండి', 'అయితే కానీ', 'సాధ్యమైతే', 'కంపు', 'కదలు', 'అందరూ', 'కింద', 'ఇతర', 'అప్పటికీ', 'కానీ అయితే', 'ఎడమ', 'సంవత్సరంలో', 'పొద్దున', 'నాకు', 'మనం', 'ఎనిమిది', 'లోపల', 'చాలా', 'నాలుగు', 'గురించి', 'కానీ', 'అప్పుడు', 'అలాంటి', 'మాఫ్ చేయండి', 'ముందు', 'నుంచి', 'మరియు', 'కొనుగుట', 'ఈరోజు', 'అటు', 'మాకు', 'కాకపోవడం', 'మీరు క్షమించాలి', 'క్షమించండి', 'అందులో', 'అందువల్ల', 'అది', 'వారంలో', 'ఆయన', 'మీద', 'అయినా', 'ఉన్నది', 'ఆరు', 'మరియు అయితే', 'నెలలో', 'ప్రతి', 'చేస్తుంది', 'ఉందాము', 'మాట', 'లేదా', 'ఉందాం', 'తన', 'రేపు', 'ఉందుకు', 'రెండు', 'ఉంది', 'ఆయి', 'ఒకవేళ', 'మొన్న', 'ఒ', 'అందు', 'అవసరంగా', 'ఉంటుంది', 'కాబట్టి', 'ఎందుకంటే', 'ఐదు', 'ఉండగల', 'ఇటు', 'అక్కడ', 'కుడి', 'ఇక్కడ', 'రాత్రి', 'ఉందాను', 'మిరులేదు', 'అదను', 'ఏది', 'మధ్యాహ్నం', 'వచ్చే', 'బయట', 'ఉండగలము', 'ఈ', 'వారి', 'అతను']

def cvtBase(word):   #function to remove otthulu and guninthalu
    new_word = ''
    for i in word:
        if i == ' ':
            new_word += i
            continue
        if ord(i) in range(ord('\u0C05'),ord('\u0C40')):
            new_word += i
    return new_word             #Ex: అప్పటికీ -> అపపటిక


def cosine_similarity(a,b):
    dot = np.dot(a,b)
    mag_a = np.sqrt(np.sum(a**2))
    mag_b = np.sqrt(np.sum(b**2))
    return dot/(mag_a*mag_b)


# parser = argparse.ArgumentParser() # To take input from command line, input are two text files

# parser.add_argument('--teacherans')
# parser.add_argument('--studentans')

# args = parser.parse_args()

if len(sys.argv) != 3:
    print("Usage: python my_script.py <input_data>")
    sys.exit(1)

teacherans = [sys.argv[1]]
studentans = [sys.argv[2]]

# with open(args.teacherans,'r',encoding='utf-8') as f:
#     teacherans = f.readlines()                          #Reading Teacher Answer


# with open(args.studentans,'r',encoding='utf-8') as f:
#     studentans = f.readlines()                          #Reading Student Answer



with open('models/pos_model.pkl', 'rb') as f:
    model = pickle.load(f)                             #Loading Pos Tagging model


with open('models/vecto.pkl','rb') as f:
    vectorizer = pickle.load(f)                        #Loading TfidfVectorizer Model


X = vectorizer.transform(teacherans)                    #Converting teacherans into tfidf vectors

teacher_predicted = model.predict(X)           #Predicting Pos tags

X = vectorizer.transform(teacherans)                     #Converting teacherans into tfidf vectors

student_predicted = model.predict(X)           #Predicting Pos tags


'''Sample Output
    Test String: అందుకే అతడు తోకను తిప్పితే , అక్కడి చెట్లు అన్నీ కూలిపోయి బయళ్ళు ఏర్పడ్డాయి
    Predicted POS: NN PRP NN NN , NN NN NN NN NN NN 
'''

t_ans = teacherans[0].split(' ')            #Splitting ans into words
t_tags = teacher_predicted[0].split(' ')    #Spliting all tags in individual words

s_ans = studentans[0].split(' ')
s_tags = student_predicted[0].split(' ')

feature_words = []
for i in range(min(len(t_ans),len(t_tags))):        #Loop to get words tagged with NN and PRP (Pronoun)
    if t_tags[i] == 'NN' or t_tags[i] == 'PRP':
        feature_words.append(t_ans[i])

for i in range(min(len(s_ans),len(s_tags))):
    if s_tags[i] == 'NN' or s_tags[i] == 'PRP':
        feature_words.append(s_ans[i])



t_sent_tokens = teacherans[0].split('.')
final_teacher = ''
for i in feature_words:                         #Loop to get sentences with the pos words
    for j in t_sent_tokens:
        if i in j:
            tokens = j.split(' ')
            tokens_removed = [i for i in tokens if i not in stop_words]
            final = ' '.join(tokens_removed)
            final_teacher += final

s_sent_tokens = studentans[0].split('.')
final_student = ''
for i in feature_words:
    for j in s_sent_tokens:
        if i in j:
            tokens = j.split(' ')
            tokens_removed = [i for i in tokens if  i not in stop_words]
            final = ' '.join(tokens_removed)
            final_student += final

if final_student == '' or final_teacher == '':
    print("Entered Text is not in telugu",end='')
    sys.exit(0)

final_teacher = cvtBase(final_teacher)          #convert to base form
final_student = cvtBase(final_student)          #convert to base form

vec = TfidfVectorizer().fit_transform([final_teacher,final_student]).toarray()
print((f'{cosine_similarity(vec[0],vec[1])*100:.2f}')+ " mark(s)",end='')