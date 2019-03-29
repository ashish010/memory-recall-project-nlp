# memory-recall-project-nlp
The program needs a google service account json file that needs to be in the project folder to run the Sentiment analysis
The steps to create a service account are:

a. Create a Google Service Client account :\n
b. Goto: https://console.cloud.google.com/iam-admin/serviceaccounts?project=memoryproject-234423\n
c. Click “Create service account” button on the top.
d. Fill the details (Service account name, and description)
e. Click “Create”
f. Select a role to give permissions and click “Continue”
g. Click “+ Create Key” and select the key type as “JSON
h. Keep the file in the project folder and keep a copy of the file in a secure location
i. Use the name of the json file in the “gc_sentiment” function in the python file
