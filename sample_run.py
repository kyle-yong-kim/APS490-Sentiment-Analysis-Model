import main

# send review data here
review_text = "This is a good branch. Friendly staff and good service. However, the line up was very very long and slow. I had to wait 30 minutes in line to get my service."
review_text = "This is a good branch. The line is very fast and efficient. The staffs were not friendly towards the customers and provided bad service, however."
review_text = "I had an issue with my accounts that TD could not resolve for me for years. I went to this branch & Ayush, who was the branch manager came to help me. Not only did he help me with what I came in for, but helped resolve my issue after asking for my banking experience with TD. He was very professionally dressed & was always smiling. He's a keeper. I'll be banking with TD for a very long time. Thank you"
review_text = "Staff was very rude and unwelcoming. The only reason I went there was the location."
review_text = "Service can be spotty at times, depending on the time of day. They no longer have a coin counter machine. They do have 30 minute parking spots around the building for your convenience."
#review_text = "When this branch first opened, it was wonderful! Friendly, intelligent staff who recognized me in the bank and walking on the street. I always went to a teller and not to an ATM. Then something changed. Tellers were autonomous and their actions were completely scripted. I guess someone thought that longer operating hours and online banking can take the place of good service. So I stopped going in. I went in for the first time in a long time last month and received surprisingly efficient service. I'm going in again in a few minutes. I'll let you know............."
#review_text = "no precise information on credit history, no clear answers to direct questions. different places tell you different things. Wish there was a place you could get reliable info from this bank"
#review_text = "Service can be spotty at times, depending on the time of day. They no longer have a coin counter machine. They do have 30 minute parking spots around the building for your convenience."

pos, neg = main.main(review_text=review_text)

print("Done")