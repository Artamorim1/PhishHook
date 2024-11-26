import pandas as pd
import requests
from urllib.parse import urlparse
import ipaddress
import re
from bs4 import BeautifulSoup
from datetime import datetime
import whois
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

# The 17 features from the original research

def havingIP(url):
    try:
        ipaddress.ip_address(url)
        return 1
    except:
        return 0

def haveAtSign(url):
    return 1 if "@" in url else 0

def getLength(url):
    return 1 if len(url) >= 54 else 0

def getDepth(url):
    path_segments = urlparse(url).path.split('/')
    return sum(1 for segment in path_segments if segment)

def redirection(url):
    pos = url.rfind('//')
    return 1 if pos > 6 else 0

def httpDomain(url):
    return 1 if 'https' in urlparse(url).netloc else 0

shortening_services = r"bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|" \
                      r"yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|" \
                      r"short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|loopt\.us|" \
                      r"doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|t\.co|lnkd\.in|db\.tt|" \
                      r"qr\.ae|adf\.ly|goo\.gl|bitly\.com|cur\.lv|tinyurl\.com|ow\.ly|bit\.ly|ity\.im|q\.gs|is\.gd|" \
                      r"po\.st|bc\.vc|twitthis\.com|u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|yourls\.org|x\.co|" \
                      r"prettylinkpro\.com|scrnch\.me|filoops\.info|vzturl\.com|qr\.net|1url\.com|tweez\.me|v\.gd|" \
                      r"tr\.im|link\.zip\.net"

def tinyURL(url):
    return 1 if re.search(shortening_services, url) else 0

def prefixSuffix(url):
    return 1 if '-' in urlparse(url).netloc else 0

def web_traffic(url, timeout=5):
    try:
        response = requests.get(f"http://data.alexa.com/data?cli=10&dat=s&url={url}", timeout=timeout)
        rank = BeautifulSoup(response.text, "xml").find("REACH")['RANK']
        return 1 if int(rank) >= 100000 else 0
    except (requests.exceptions.RequestException, TypeError):
        return 1  # Had to add a time out process older datasets.

def domainAge(domain_name):
    try:
        creation_date = domain_name.creation_date
        expiration_date = domain_name.expiration_date
        age_days = (expiration_date - creation_date).days
        return 1 if (age_days / 30) < 6 else 0
    except:
        return 1

def domainEnd(domain_name):
    try:
        expiration_date = domain_name.expiration_date
        end_days = (expiration_date - datetime.now()).days
        return 1 if (end_days / 30) < 6 else 0
    except:
        return 1

def iframe(response):
    return 1 if re.search(r"<iframe>|<frameBorder>", response.text) else 0

def mouseOver(response):
    return 1 if re.search(r"onmouseover", response.text) else 0

def rightClick(response):
    return 1 if re.search(r"event.button==2", response.text) else 0

def forwarding(response):
    return 1 if len(response.history) > 2 else 0

def featureExtraction(url, timeout=5):
    features = [
        havingIP(url),
        haveAtSign(url),
        getLength(url),
        getDepth(url),
        redirection(url),
        httpDomain(url),
        tinyURL(url),
        prefixSuffix(url)
    ]
    
    # Domain-based features
    try:
        domain_name = whois.whois(urlparse(url).netloc)
        dns = 0
        features.append(dns)
        features.append(web_traffic(url, timeout=timeout))
        features.append(domainAge(domain_name))
        features.append(domainEnd(domain_name))
    except:
        dns = 1
        features.extend([dns, 1, 1, 1])

    # HTML/JS-based features
    try:
        response = requests.get(url, timeout=timeout)
        features.extend([
            iframe(response),
            mouseOver(response),
            rightClick(response),
            forwarding(response)
        ])
    except requests.exceptions.RequestException:
        features.extend([1, 1, 1, 1])  # May fail so I have set defaults

    return features

# Feature names
feature_names = [
    'Have_IP', 'Have_At', 'URL_Length', 'URL_Depth', 'Redirection',
    'https_Domain', 'TinyURL', 'Prefix/Suffix', 'DNS_Record', 'Web_Traffic', 
    'Domain_Age', 'Domain_End', 'iFrame', 'Mouse_Over', 'Right_Click', 'Web_Forwards'
]

# Load dataset 
df = pd.read_csv('dataset3.csv')

if 'URL' not in df.columns:
    raise ValueError("The CSV file must contain a 'URL' column.")

features = []

# ThreadPoolExecutor helps me speed up the trainning by splitting queries. (it also adds a progress counter with tqdm) 
with ThreadPoolExecutor(max_workers=10) as executor:
    futures = {executor.submit(featureExtraction, url): url for url in df['URL']}
    for future in tqdm(as_completed(futures), total=len(df), desc="Extracting features"):
        features.append(future.result())

features_df = pd.DataFrame(features, columns=feature_names)

features_df.insert(0, 'Domain', df['URL'])

if 'Label' in df.columns:
    features_df['label'] = df['Label']

# Save to CSV
features_df.to_csv('extracted3.csv', index=False)

print("Feature extraction complete. The extracted features are saved in 'extracted3.csv'.")
