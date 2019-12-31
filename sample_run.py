import main

# send review data here
review_text = "This is a good branch. Friendly staff and good service. However, the line up was very very long and slow. I had to wait 30 minutes in line to get my service."
pos, neg = main.main(review_text=review_text)

print("Done")