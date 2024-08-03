import PyPDF2
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import Counter
import os
# nltk.download('punkt')

# Resume Shortlisting/uploads
def reader(jd_path):
    # print(os.path.dirname(jd_path))
    job_dir = 'Resume Shortlisting/'+ os.path.dirname(jd_path)
    for file_name in os.listdir(job_dir):
        job_desc_path = os.path.join(job_dir, file_name)
        with open(job_desc_path, 'rb') as file:
        # Create a PDF reader object
            pdf_reader = PyPDF2.PdfReader(file)
            # Initialize an empty string to store the extracted text
            text = ''
            # Iterate through each page of the PDF
            for page_num in range(len(pdf_reader.pages)):
                # Extract text from the current page
                text += pdf_reader.pages[page_num].extract_text()
    
    # Tokenize the extracted text
    tokens = word_tokenize(text)
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [word.lower() for word in tokens if word.lower() not in stop_words]
    # Define a list of words related to a software engineer
    software_engineer_words = [
        'software', 'engineer', 'java', 'python', 'c++', 'programming', 'coding', 'development',
        'algorithms', 'data structures', 'database', 'operating systems', 'computer science',
        'machine learning', 'artificial intelligence', 'web development', 'software development',
        'frontend', 'backend', 'full-stack', 'version control', 'git', 'debugging', 'testing',
        'agile', 'scrum', 'kanban', 'requirements', 'design patterns', 'object-oriented programming',
        'cloud computing', 'docker', 'microservices', 'security', 'networking', 'mobile development',
        'android', 'ios', 'linux', 'windows'
    ]
    # Filter tokens to include only those related to a software engineer
    filtered_tokens = [word for word in filtered_tokens if word in software_engineer_words]
    # Count the frequency of each word
    word_freq = Counter(filtered_tokens)
    # Sort the words by frequency in decreasing order
    sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
    job_description= []
    for word, freq in sorted_words:
        job_description.append(word)
    
    return job_description

