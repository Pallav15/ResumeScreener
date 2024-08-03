from fastapi import FastAPI, File, UploadFile
from typing import List
import warnings
import os
from pyresparser import ResumeParser
from collections import Counter
import PyPDF2
import re
import joblib
import job_description as jd


warnings.filterwarnings("ignore")

def process_resumes(jd_path, res_path):

    def clean_text(txt):
        clean_text = re.sub('http\S+\s', ' ', txt)
        clean_text = re.sub('RT|cc', ' ', clean_text)
        clean_text = re.sub('#\S+\s', ' ', clean_text)
        clean_text = re.sub('@\S+', '  ', clean_text)
        clean_text = re.sub('[%s]' % re.escape("""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""), ' ', clean_text)
        clean_text = re.sub(r'[^\x00-\x7f]', ' ', clean_text)
        clean_text = re.sub('\s+', ' ', clean_text)
        return clean_text

    model = joblib.load('knn_model.joblib')
    le = joblib.load('label_encoder.joblib')
    tfidf_vectorizer = joblib.load('tfidf_vectorizer.joblib')

    def resume_opener(resume_dir):
        resume_category = []
        for filename in os.listdir(resume_dir):
            if filename.endswith('.pdf'):
                resume_path = os.path.join(resume_dir, filename)
                with open(resume_path, 'rb') as pdf_file:
                    pdf_reader = PyPDF2.PdfReader(pdf_file)
                    pdf_text = [clean_text(pdf_reader.pages[page_num].extract_text()) for page_num in range(len(pdf_reader.pages))]
                # Preprocess text extracted from resume.pdf
                cleaned_text = " ".join(pdf_text)
                # Transform the preprocessed text using the TF-IDF vectorizer
                text_features = tfidf_vectorizer.transform([cleaned_text])
                # Make predictions using the trained KNN model
                resume_category.append(le.inverse_transform(model.predict(text_features)))
        return resume_category

    # job_description_keywords = ['Java', 'J2EE', 'Spring', 'Hibernate','Python', 'data science', 'etl developer']
    job_description_keywords= jd.reader(jd_path)


    resume_directory = 'Resume Shortlisting/' + os.path.dirname(res_path)
    # Function to parse resumes in a given directory
    def parse_resumes(resume_dir):
        print(resume_directory)
        resume_data_list = []
        for filename in os.listdir(resume_dir):
            if filename.endswith('.pdf'):
                resume_path = os.path.join(resume_dir, filename)
                try:
                    data = ResumeParser(resume_path).get_extracted_data()
                    resume_data_list.append((filename, data))
                except Exception as e:
                    print(f"Error parsing {filename}: {e}")
        return resume_data_list

    # Function to predict category
    def predicted_category(resume_category, job_description_keywords):
        resume_cat = []
        for i in resume_category:
            if i[0].lower() not in job_description_keywords:
                resume_cat.append(0)
            else:
                resume_cat.append(1)
        return resume_cat

    # Function to match resume to job description
    def match_resume_to_job_description(resume_data, job_description_keywords):
        skills = set(skill.lower() for skill in resume_data.get('skills', []))
        experience = set(exp.lower() for exp in resume_data.get('experience', []))
        matched_skills = [keyword for keyword in job_description_keywords if keyword.lower() in skills]
        matched_experience = [keyword for keyword in job_description_keywords if keyword.lower() in experience]
        relevance_score = len(matched_skills) + len(matched_experience)
        return relevance_score

    resume_dir = 'data/test'
    resume_category = resume_opener(resume_directory)
    resume_cat = predicted_category(resume_category, job_description_keywords)
    parsed_resumes = parse_resumes(resume_directory)  # Assuming this function returns parsed resumes in a dictionary
    
    matched_resumes = []
    count =0
    for filename, resume_data in parsed_resumes:
        if resume_data:  # Ensure resume data is not None
            relevance_score = match_resume_to_job_description(resume_data, job_description_keywords)+5*resume_cat[count]
            matched_resumes.append({
                'name': filename,
                'score': relevance_score,
            })
        count +=1

    matched_resumes.sort(key=lambda x: x['score'], reverse=True)
    return matched_resumes
