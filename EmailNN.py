import multiprocessing
from multiprocessing import Process
import time
import threading
import NN_Train
import EmailTool


def nn(params):
    train,test = NN_Train.GetDate()
    msg = NN_Train.NN_Train(
        NN_Train.GetNN(),
        train,test,
        epochs=int(params['ep']),
        batch_size=int(params['bs']),
        learning_rate=params['lr'],
        weight_decay=params['wd'])
    print(msg)
def run(msg):
    
    params = {'ep':10,'lr':0.002,'bs':128,'wd':0.0}
    xx = msg.split('\r\n')
    for k in xx:
        ks = k.split(' ')
        if len(ks) >1:
            params[ks[0]] = float(ks[1])
    print(params)

    p = Process(target=nn,args=(params,))
    print('strart')
    global trunnn
    trunnn = True
    p.start()
    p.join()
    trunnn = False


if __name__ == '__main__':
    global trunnn
    trunnn = False
    print('bbb')
    a = 1
    #p.join()
    while(True):
        time.sleep(10)
        print('aaa',trunnn)
        try:
            msg,sub,date = EmailTool.ReEmail()
        except TimeoutError as e:
            print('TimeoutError')
        
        if sub == 'train':
            print('train')
            if trunnn == False:
                t1 = threading.Thread(target=run,args=(msg,))
                t1.start()
        if sub == 'print':
            print('print')
            print(msg)