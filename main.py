import pandas as pd
import os
from dotenv import load_dotenv
import requests
import schedule
import time

load_dotenv()

sheet_id = os.environ.get('SHEET_ID')
refresh = float(os.environ.get('REFRESH'))
apiToken = os.environ.get('TELEGRAM_API_TOKEN')
chat_id = os.environ.get('TELEGRAM_CHAT_ID')
chat_id = chat_id.split(',')

print(refresh)
print(chat_id)

#Creates a new "before_update.csv" file if not exists
if not os.path.exists("before_update.csv"):
    with open("before_update.csv", "w") as file:
        file.write("Reserva,Entrada,Salida,Personas,Precio\n")
        file.write("Test,2024-04-14,2024-04-16,4,100.50\n")

print("Starting program!")

def check_update():

    print("checking updates...")
    df = pd.read_csv(f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv")
    df_b = pd.read_csv('before_update.csv')

    if not df.equals(df_b):
        report(df, df_b)
    else:
        print('nothing to report')
 
def report(df, df_b):
    #Save df as csv
    print(df)
    print(df_b)
    df.to_csv('before_update.csv', index=False)

    # Convert format
    df['Entrada'] = pd.to_datetime(df['Entrada'], format='%d/%m/%Y')
    df['Salida'] = pd.to_datetime(df['Salida'], format='%d/%m/%Y')
    df['Personas'] = pd.to_numeric(df['Personas'])
    df['Precio'] = pd.to_numeric(df['Precio'])

    df_b['Entrada'] = pd.to_datetime(df_b['Entrada'])
    df_b['Salida'] = pd.to_datetime(df_b['Salida'])
    df_b['Personas'] = pd.to_numeric(df_b['Personas'])
    df_b['Precio'] = pd.to_numeric(df_b['Precio'])


    #Detect new rows
    merged_df = pd.merge(df, df_b, how='outer', indicator=True)
    new_rows = merged_df[merged_df['_merge'] == 'left_only']
    print(new_rows)

    #Indicate the new row
    df1 = df
    indexes = new_rows.index
    df1['Estado'] = ''
    try:
        df1.loc[indexes, 'Estado'] = '<-'
    except:
        print("Se ha eliminado alguna entrada")
    #Sort by 'Entrada'
    df1 = df1.sort_values(by='Entrada')

    #Create text
    text=''
    for index, row in df1.iterrows():
        entrada = pd.to_datetime(row['Entrada']).strftime('%d/%m/%Y')
        salida = pd.to_datetime(row['Salida']).strftime('%d/%m/%Y')
        line = f"{row['Reserva']} {entrada} - {salida} ({row['Personas']}) ({row['Precio']}) {row['Estado']}\n"
        text += line

    #Send message
    for chat in chat_id:
        send_to_telegram(text, apiToken, chat)
        print("message sent")
    


def send_to_telegram(message, apiToken, chatID):
    apiURL = f'https://api.telegram.org/bot{apiToken}/sendMessage'
    try:
        resp = requests.post(apiURL, json={'chat_id': chatID, 'text': message})
        return resp
    except Exception as e:
        print(e)

schedule.every(refresh).minutes.do(check_update)

while True:
    schedule.run_pending()
    time.sleep(1)