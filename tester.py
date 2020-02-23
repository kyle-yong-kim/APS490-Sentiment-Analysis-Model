import pandas as pd
import pickle

def main():
    fileLoc = '.\prediction.pickle'
    test_res = pickle.load(open(fileLoc, 'rb'))

    fileLoc = '.\Test_Validation Data.xlsx'
    df = pd.concat(pd.read_excel(fileLoc, sheet_name=[0,1]), ignore_index=True)
    sentiment_corr = 0
    service_corr = 0
    queue_corr = 0
    friendliness_corr = 0

    service_found = False
    queue_found = False
    friendliness_found = False

    for i, item in test_res.items():
        review = item[0]
        sentiment_avg = item[1]
        aspect_performance = item[4]
        row = df.iloc[i]

        # pre-rprocess star rating into binary output
        if row['Star'] > 2.5:
            score = 1
        else:
            score = -1

        if (sentiment_avg>0 and score>0) or (sentiment_avg<0 and score<0):
            sentiment_corr += 1

        # aspect performance evaluation
        service_val_pos = aspect_performance.get('service_pos', 0)
        service_val_neg = aspect_performance.get('service_neg', 0)
        queue_val_pos = aspect_performance.get('queue_pos', 0)
        queue_val_neg = aspect_performance.get('queue_neg', 0)
        friendliness_val_pos = aspect_performance.get('friendliness_pos', 0)
        friendliness_val_neg = aspect_performance.get('friendliness_neg', 0)

        if service_val_pos != 0 or service_val_neg != 0:
            service_found = True
        if queue_val_pos != 0 or queue_val_neg != 0:
            queue_found = True
        if friendliness_val_pos != 0 or friendliness_val_neg != 0:
            friendliness_found = True

        # correct service
        if (not service_found and row['Service Quality '] == 0) or (service_found and row['Service Quality '] != 0):
            service_corr += 1
        if (not queue_found and row['Queue'] == 0) or (queue_found and row['Queue'] != 0):
            queue_corr += 1
        if (not friendliness_found and row['Friendliness'] == 0) or (friendliness_found and row['Friendliness'] != 0):
            friendliness_corr += 1

    res = sentiment_corr/df.shape[0]
    service_acc = service_corr/df.shape[0]
    queue_acc = queue_corr/df.shape[0]
    friendliness_acc = friendliness_corr/df.shape[0]

    print(res, service_acc, queue_acc, friendliness_acc)

if __name__ == '__main__':
    main()