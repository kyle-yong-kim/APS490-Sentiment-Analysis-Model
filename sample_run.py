import main
import pandas as pd
import pickle

# send review data here
review_text = "This is a good branch. Friendly staff and good service. However, the line up was very very long and slow. I had to wait 30 minutes in line to get my service."
review_text = "This is a good branch. The line is very fast and efficient. The staffs were not friendly towards the customers and provided bad service, however."
review_text = "I had an issue with my accounts that TD could not resolve for me for years. I went to this branch & Ayush, who was the branch manager came to help me. Not only did he help me with what I came in for, but helped resolve my issue after asking for my banking experience with TD. He was very professionally dressed & was always smiling. He's a keeper. I'll be banking with TD for a very long time. Thank you"
review_text = "Staff was very rude and unwelcoming. The only reason I went there was the location."
review_text = "Service can be spotty at times, depending on the time of day. They no longer have a coin counter machine. They do have 30 minute parking spots around the building for your convenience."
#review_text = "When this branch first opened, it was wonderful! Friendly, intelligent staff who recognized me in the bank and walking on the street. I always went to a teller and not to an ATM. Then something changed. Tellers were autonomous and their actions were completely scripted. I guess someone thought that longer operating hours and online banking can take the place of good service. So I stopped going in. I went in for the first time in a long time last month and received surprisingly efficient service. I'm going in again in a few minutes. I'll let you know............."
#review_text = "no precise information on credit history, no clear answers to direct questions. different places tell you different things. Wish there was a place you could get reliable info from this bank"
#review_text = "Service can be spotty at times, depending on the time of day. They no longer have a coin counter machine. They do have 30 minute parking spots around the building for your convenience."
review_text = "I had an issue with my accounts that TD could not resolve for me for years. Never had a good experience with TD. I went to this branch & Ayush, who was the branch manager came to help me. Not only did he help me with what I came in for, but helped resolve my issue after asking for my banking experience with TD. He was very professionally dressed & was always smiling. He's a keeper. I'll be banking with TD for a very long time. Thank you"
review_text = "Nice place with friendly staff. Quite busy at times and TDs fees are a bit high but otherwise very convenient."
review_text = "Asked to get change for $100 dollars the lady ask me for my idea I didn't have it on my she refused to give me change."

# positive
review_text = "Great customer service from Kathleen Le! People like her deserve a shout out for excellent service. Thanks again!"

# negative
review_text = "Waited in line and finally reached to the counter. Nobody helped me. One of the lady told me to wait and never returned. They just called people behind me and helped them first. It's almost 20 minutes now."

# neutral
review_text = "This is a good branch. Friendly staff and good service. However, the line up was very very long and slow. I had to wait 30 minutes in line to get my service."

# client demo
review_text = ""
review_text_list = ["Great customer service from Kathleen Le! People like her deserve a shout out for excellent service. Thanks again!", "this is a", "test!"]

# label performance 
review_text_list = ["Waited in line and finally reached to the counter. Nobody helped me. One of the lady told me to wait and never returned. They just called people behind me and helped them first. It's almost 20 minutes now.", "Great customer service from Kathleen Le! People like her deserve a shout out for excellent service. Thanks again!"]
review_text_list = ["Waited in line and finally reached to the counter. Nobody helped me. One of the lady told me to wait and never returned. They just called people behind me and helped them first. However, great customer service from Kathleen Le! People like her deserve a shout out for excellent service. Thanks again!"]
# review_text = "I gave them a call, they didn't pick up so i left a message. Never called back. Edit: I gave this 1 star before but now it's 3 stars because I went and got the business done right away thanks to Zahen even though they never called."
# load the text

fileLoc = '.\Test_Validation Data.xlsx'
df_1 = pd.read_excel(fileLoc, sheet_name=None)
df = pd.concat(pd.read_excel(fileLoc, sheet_name=[0,1]), ignore_index=True)
res = main.main(df = df)

with open('prediction.pickle', 'wb') as f:
    pickle.dump(res, f)

print("Done")