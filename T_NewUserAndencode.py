import cv2
import numpy as np
import face_recognition
import os
import glob
import mysql.connector
import csv
from datetime import datetime

class User:
    def __init__(self):
        self.name = input("please Enter your Name:")
        self.encode = []
        self.path = "./images"
    def NewUser(self): 
        # Running & Connect MySQL
        # Username = self.name
        # Curdate = datetime.today()
        # connection = mysql.connector.connect(host='localhost',
        #                                     database='lets_dance',
        #                                     user='dba',
        #                                     password='dbaMySQL80')
        # my_cursor = connection.cursor()  # Create object to update table
        # # Ready to Insert value in table
        try:
        #     insert_commit = "INSERT INTO player(p_name,p_date) VALUES (%s, %s)"
        #     data = (Username, Curdate)
        #     my_cursor.execute(insert_commit, data)
        #     connection.commit()
            # get image of New user
            cap = cv2.VideoCapture(0)
            flag = cap.isOpened()
            while flag:
                ret, frame = cap.read()
                cv2.imshow("Capture_Webcam", frame)
                k = cv2.waitKey(1) & 0xFF
                if k == ord('s'):  # put s key and save pic web came shot
                    cv2.imwrite(f'{self.path}/{self.name}.jpg', frame)  # 先存檔，再抓圖片 (應有簡單的語法)
                    print("encoding...")
                    curImg = cv2.imread(f'{self.path}/{self.name}.jpg')
                    img = cv2.cvtColor(curImg, cv2.COLOR_BGR2RGB)  # type which is ready to encoding
                    self.encode = list(face_recognition.face_encodings(img)[0])  # 單人encoding並放在list中
                    print("encoding completed!")
                elif k == ord('q'):
                    break
            cap.release()
            cv2.destroyAllWindows()
            return True
        except:
            print('Name has been used! Try another Name!')
            return False

    def markAttendance(self, result):  # record attendance name and time
        if result:
            with open('facecode.csv', mode='r+', newline='', encoding="utf-8") as f:  # read and write mode in same time
                myDataList = f.readlines()   # read all imformation in file # 運行不好
                nameList = []
                for line in myDataList:  # read every line in myDataList
                    entry = line.split(',')  # split line into several elements with ',' and put them into list
                    nameList.append(entry[0])  # record name in nameList
                if self.name not in nameList:  # check wether name is in nameList or not
                    writer = csv.writer(f)  # 新物件 : 專門撰寫csv資料
                    writer.writerow([f"{self.name}", self.encode])
                    # f.writelines(f'\n{self.name},{self.encode}')
        else:
            pass

    def PutEncodesql(self):
        connection = mysql.connector.connect(host='localhost',
                                             database='lets_dance',
                                             user='dba',
                                             password='dbaMySQL80')
        my_cursor = connection.cursor(prepared=True)
        try:
            # insert_face = '%'+','.join('s%')*len(self.encode)+'s'
            # print(len(self.encode))
            # print(insert_face)
            # a="INSERT INTO player(p_face) VALUES (%s)" % insert_face
            # print(a)
            # print(len('%s'))
            insert_face = "INSERT INTO player(p_name,p_face,p_date) VALUES (%s,%s,%s)"
            # data_list = [str(i) for i in self.encode]  #list[str]
            data_list = (self.name, str(self.encode), str(datetime.today()))  # list
            # data_list = ','.join(data_list1)  #str
            # data_list3 = data_list2.strip(' ').split(',')
            # data_list = map(str, data_list)
            # data_list = np.array(data_list_a)
            # print(data_list)
            # print((type(data_list)))
            my_cursor.executemany(insert_face, (data_list,))
            # my_cursor.executemany(insert_face, map(list,data_list1))
            # my_cursor.execute("INSERT INTO player(p_face) VALUES (%s)" % insert_face ,tuple(self.encode))
            connection.commit()
        except Exception as err:
            print(err)
            connection.rollback()


if __name__ == '__main__':  # 當執行主程式腳本時才執行下列程式
    Newuser = User()  # 建立新的實體物件
    Result = Newuser.NewUser()
    Newuser.PutEncodesql()
    Newuser.markAttendance(Result)

