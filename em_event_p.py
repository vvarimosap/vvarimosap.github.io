import http.client
import base64, requests, hashlib, uuid, json
from datetime import datetime

def pretty(d, indent=0):
   for key, value in d.items():
      print('\t' * indent + str(key))
      if isinstance(value, dict):
         pretty(value, indent+1)
      else:
         print('\t' * (indent+1) + str(value))
            
conn = http.client.HTTPSConnection("api.emarsys.net")
# The current timestamp in ISO8601 format.
timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')


# NOTE TRIGGER ID needs to be different for every invocation with intearction programs, otherwise it will execute only once
payload = "{\"key_id\":3," \
          "\"contacts\":" \
          "[{\"trigger_id\": 1000030001333,\"external_id\":\"v.varimo@sap.com\"}]}"

        

    
nonce = uuid.uuid4().hex
print (payload)


username = "Public_GDM_EMEA008"
secret = "yoursercretkey"
raw_password_digest = nonce + timestamp + secret

encrypted_password_digest = hashlib.sha1()
encrypted_password_digest.update(raw_password_digest.encode())
pass_sha1 = encrypted_password_digest.hexdigest()

# Computes the Password Digest
pass_digest = base64.b64encode(pass_sha1.encode()).decode()

headers= {
    'Content-Type': 'application/json',
    'X-WSSE': 'UsernameToken Username="{}", PasswordDigest="{}", Nonce="{}", Created="{}"'.format(
        username,
        pass_digest,
        nonce,
        timestamp)}


pretty(headers)
conn.request("POST", "/api/v2/event/100003000/trigger", payload, headers)

res = conn.getresponse()
data = res.read()

print(res.headers)
print(data.decode("utf-8"))