from pydantic import BaseModel, ValidationError, Field
import logging
from typing import Literal
import json

# 1. Create Pydantic Model
class Registration(BaseModel):
    registration_id: str
    name: str
    email: str
    age:int=Field(gt=18)
    ticket_type:Literal["Standard","Premium","VIP"]
    amount:float=Field(gt=0)

with open("registrations.json","r") as file:
    records=json.load(file)

valid_records=[]

for record in records:
    try:
        registration=Registration.model_validate(record)
        valid_records.append(registration)
    except ValidationError as e:
        print(e)

# 7. Print only valid registrations
for registration in valid_records:
    print(registration)

# 8. Catch Pydantic validation errors and print a simple message showing: registration ID field with error message

for record in records:
    try:
        registration=Registration.model_validate(record)
        print(registration)
    except ValidationError as e:
        registration_id=record.get("registration_id")
        for error in e.errors():
            field=error["loc"][0]
            message=error["msg"]

            print(f"Registration ID: {registration_id}," " Field: {field}, Message: {message}")

# 9. Serialize one valid Pydantic object into a Python dictionary.
if valid_records:
    print(valid_records[0].model_dump())

# 10. Serialize one valid object into JSON
if valid_records:
    print(valid_records[0].model_dump_json(indent=4))


# 11. Save all valid registration to valid_registrations.json
with open("registration.json","w") as file:
    json.dump([r.model_dump() for r in valid_records],file)

#12. Configure logging with INFO,WARNING,ERROR levels
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("registration.log"),
        logging.StreamHandler()
    ]
)

logger=logging.getLogger(__name__)

# 13. Log and INFO message for successful validation

logger.info(
    "Registration %s validated successfully",
    registration.registration_id
)

# 14. Log an ERROR message when validation fails
logger.error(
    "Registation %s failed validation",
    registration_id
)

#15. Log a WARNING when ticket_type is VIP

if registration.ticket_type=="VIP":
    logger.warning(
        "Registration %s has a VIP ticket",
        registration.registration_id
    )
# 16. Save logs to registration.log

logging.FileHandler("registration.log")

# 17 Add error handling for missing files,invalid JSON, and validation failures

try:
    with open("registration.json","r") as file:
        record=json.load(file)
except FileNotFoundError:
    logger.error("registration.json file not found")
except json.JSONDecodeError as e:
    logger.error("Invalid JSON: %s",e)

except ValidationError as e:
    logger.error("Validation Error: %s",e)

# 18. Prevent the program from crashing if the json file does not exist
# 19. Change age to text and observe Pydantic validation
# 20. Print the summary
print("Total records: ", len(records))
print("Valid records: ", len(valid_records))
print("Invalid records: ", len(records) - len(valid_records))

