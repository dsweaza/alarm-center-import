import pyodbc
import csv

server = "HOST_ADDR"
database = "SUBSCRIBER"
input_file = 'zones.csv'
output_file = 'out.csv'

"""CONNECTS VIA TRUSTED CONNECTION / MUST BE LOGGED INTO COMPUTER WITH ACCOUNT THAT HAS ACCESS TO DATABASE"""
conn = pyodbc.connect('DRIVER={SQL Server};SERVER=' + server + ';DATABASE=' + database + ';Trusted_Connection=yes;')
cursor = conn.cursor()  

def main():
    processedZones = processCSV()
    countSuccess = insertZones(processedZones)
    
    print(f"\nSuccessfully added {countSuccess} rows to the database!")
    
def processCSV():
    with open(input_file, newline='') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',')
        
        zones = []
        
        linecount = -1
        current_account_num = ''
        current_account_id = 0
        
        for row in csv_reader:
            if linecount == -1:
                print(f'Column names are {", ".join(row)} \n')
                linecount += 1
            else:
                
                if current_account_num != row[0]:
                    current_account_num = row[0]
                    parsedAccountNumber = parseAccountNumber(current_account_num)
                    line_code = parsedAccountNumber[0]
                    account_number = parsedAccountNumber[1]
                    current_account_id = getAccountId(line_code, account_number)
                    if current_account_id == None:
                        print(f"FAILED! Unable to locate {current_account_num} in the system. Logged to {output_file}")
                        addOutput(False, 'Account Number not found in database', row)
                        continue
                
                currentZoneDict = {
                    'AccountID': current_account_id,
                    'Number': row[1].rjust(10), #Must be 10 digits long with space padding to front
                    'Description': row[2],
                    'Code': row[3],
                    'EmerListNum': 1,
                    'Picture': '',
                    'Note': '',
                    'RestCode': '',
                    'RestWait': 0,
                    'RestFlag': '',
                    'AutoShowGraphic': 0,
                    'ProcedureID': 0,
                    'AllowSMSPage': 1,
                }
                linecount += 1
                
                print(f"Processed zone for {current_account_num} (ID: {current_account_id})")
                
                zones.append(currentZoneDict)
    return zones
    
def insertZones(zones):
    count = 0
    for zone in zones:
        sql = f"INSERT INTO dbo.[Zone Lists] \
        (AccountID, \
        Number, \
        Description, \
        Code, \
        EmerListNum, \
        Picture, \
        Note, \
        RestCode, \
        RestWait, \
        RestFlag, \
        AutoShowGraphic, \
        ProcedureID, \
        AllowSMSPage \
        ) VALUES ( \
        '{zone['AccountID']}', \
        '{zone['Number']}', \
        '{zone['Description']}', \
        '{zone['Code']}', \
        '{zone['EmerListNum']}', \
        '{zone['Picture']}', \
        '{zone['Note']}', \
        '{zone['RestCode']}', \
        '{zone['RestWait']}', \
        '{zone['RestFlag']}', \
        '{zone['AutoShowGraphic']}', \
        '{zone['ProcedureID']}', \
        '{zone['AllowSMSPage']}' \
        )"
        cursor.execute(sql)
        count += 1
        
    conn.commit()
    return count

def getAccountId(line_code, account_number):
    cursor.execute("SELECT AccountId FROM dbo.[Subscriber Data] WHERE AcctLineCode = '" + line_code + "' AND AcctNum = '" + account_number + "'")
    for row in cursor:
        return row[0]

""" ACCOUNT NUMBER IS FORMATTED AS 'CSF-1234'. LINE CODE IS FIRST HALF, ACCOUNT NUMBER SECOND HALF """
def parseAccountNumber(full_account_number):
    split_account_number = full_account_number.split('-')
    line_code = split_account_number[0]
    account_number = split_account_number[1]
    account_number = account_number.rjust(10)
    
    return line_code, account_number
    
def addOutput(success, message, row):
    if success:
        status = 'Success'
    else:
        status = 'FAILED!'
        
    row.append(status)
    row.append(message)
    
    with open(output_file, mode='a') as out_file:
        out_writer = csv.writer(out_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        out_writer.writerow(row)

if __name__ == '__main__':
    main()