import os
import email
from bs4 import BeautifulSoup
import re

BASE_DIR = os.path.dirname(__file__)

path_to_data_files = os.environ.get(
    "TREC07P_DATA_DIR",
    os.path.join(BASE_DIR, "trec07p", "data")
)
path_to_index_file = os.environ.get(
    "TREC07P_INDEX_FILE",
    os.path.join(BASE_DIR, "trec07p", "full", "index")
)

OUTPUT_DIR = os.path.join(BASE_DIR, "Files")
url = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!\*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', re.I)


def spamHam():
    labelDict = {}
    with open(path_to_index_file, 'r', encoding="utf-8", errors="ignore") as indexFile:
        for line in indexFile.readlines():
            lineStr = line.split(' ')
            id = lineStr[1].rsplit('.', 1)[1].strip()
            label = lineStr[0]
            labelDict[id] = label
    indexFile.close()
    return labelDict

def getBody(parts):
    ret = []
    if type(parts) == str:
        ret.append(parts)
    elif type(parts) == list:
        for part in parts:
            if part.is_multipart():
                ret += getBody(part.get_payload())
            else:
                ret += getBody(part)
    elif parts.get_content_type().split(' ')[0] == 'text/plain':
        ret.append(parts.get_payload())
    elif parts.get_content_type().split(' ')[0] == 'text/html':
        soup = BeautifulSoup(parts.get_payload(), 'html.parser')
        email_content_string = soup.get_text()
        ret.append(email_content_string)
    return ret

def clean_string(input_string):

    cleaned_string = input_string.replace('-', ' ').replace('.', ' ').replace('?', ' ') \
        .replace('/', ' ').replace('!', ' ').replace('@', ' ').replace('#', ' ').replace(',', ' ') \
        .replace('%', ' ').replace(':', ' ').replace(';', ' ').replace('<', ' ').replace('>', ' ').replace('$', ' ')\
    .replace('*', ' ').replace('&', ' ').replace('_', ' ').replace('~', ' ').replace('[', ' ').replace(']', ' ')\
    .replace('(', ' ').replace(')', ' '). replace('\\', ' ').replace('{', ' ').replace('}', ' ').replace('^', ' ')\
    .replace('"', ' ').replace('\n', ' ').replace('=', ' ').replace('+', ' ')

    cleaned_string = ' '.join(cleaned_string.split())
    return cleaned_string

def load_trec_spam_files():
    if not os.path.isfile(path_to_index_file):
        raise FileNotFoundError(
            "TREC index file not found. Set TREC07P_INDEX_FILE env var or place it at: "
            + path_to_index_file
        )
    if not os.path.isdir(path_to_data_files):
        raise FileNotFoundError(
            "TREC data directory not found. Set TREC07P_DATA_DIR env var or place it at: "
            + path_to_data_files
        )

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    labelDict = spamHam()
    total_files = os.listdir(path_to_data_files)
    for each_file in total_files:
        file_path = os.path.join(path_to_data_files, each_file)
        with open(file_path, 'r', encoding="ISO-8859-1") as Email_File:
            emailID = each_file.split('.')[1]
            msg = email.message_from_file(Email_File)
            subject = msg['Subject']
            body = '\n'.join(
                p for p in getBody(msg.get_payload())
                if type(p) == str
            )
            emailText =''
            if not subject:
                emailText += body
            elif not body:
                emailText += subject
            else:
                emailText = subject + '\n' + body

            emailText = url.sub(' ', emailText)
            emailText = clean_string(emailText)
            label = labelDict[emailID]
            with open(os.path.join(OUTPUT_DIR, '%s.txt' % emailID), 'w', encoding="utf-8", errors="ignore") as eFile:
                content = "<EMAILID>%s</EMAILID>\n<TEXT>%s</TEXT>\n<LABEL>%s</LABEL>" %(emailID, emailText, label)
                eFile.write(content)
            eFile.close()
        Email_File.close()

if __name__ == "__main__":
    load_trec_spam_files()