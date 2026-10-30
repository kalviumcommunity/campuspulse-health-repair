"""Print HTTP status/body, including expected 503 failures. Transport errors fail."""
import urllib.request,urllib.error,sys
try:
    with urllib.request.urlopen(sys.argv[1],timeout=4) as response:
        print("HTTP",response.status,response.read().decode())
except urllib.error.HTTPError as response:
    print("HTTP",response.code,response.read().decode())
