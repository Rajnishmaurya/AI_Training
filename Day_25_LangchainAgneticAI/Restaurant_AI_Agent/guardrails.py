import re 

MAX_INPUT_LENGTH=1000

#Email detection 
EMAIL_PATTERN=re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")
#phone number detection
PHONE_PATTERN=re.compile(r"(?<!\w)(?:\+?\d[\d\s().-]{7,}\d)(?!\w)")

#Restaurants related keywords

RESTAURANT_KEYWORDS={
    "restuarant","reatusrants","food","dining","dinner","lunch","breakfast","cuisine","indian","italian",
    "chinese","mexican","japanese","thai","pizza","burger","cafe","seat","seats","table","tables",
    "guest","guests","people","person","cost","price","bill","spice","garden","reserve","reservation",
    "available","availability"
}

def validate_input(text):
    if not text or not text.strip():
        return False, "Question can not be empty."
    if len(text)>MAX_INPUT_LENGTH:
        return False, "Question is too long."
    return True,""

def is_restaurant_related(text):
    text=text.lower() 
    return any(keyword in text for keyword in RESTAURANT_KEYWORDS)

def redact_pii(text):
    original=text 
    text=EMAIL_PATTERN.sub("[REDACTED EMAIL]",text)
    text=PHONE_PATTERN.sub("[REDACTED PHONE]",text)

    pii_found=original!=text

    return text,pii_found

def redacted_output(text):
    text=EMAIL_PATTERN.sub("[REDACTED EMAIL]",text)
    text=PHONE_PATTERN.sub("[REDACTED PHONE]",text)

    return text
