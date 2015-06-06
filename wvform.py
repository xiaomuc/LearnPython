#coding:utf-8
import wave
import numpy as np
import matplotlib.pyplot as plt

def printWaveInfo(wf):
    """waveファイルの情報を取得"""
#  print("def add(3,5)=%d" % add(3,5))
#    print("チャンネル数:%d" % wf.getnchannels())
    print("チャンネル数:", wf.getnchannels())
    print("サンプル幅:", wf.getsampwidth())
    print("サンプリング周波数:", wf.getframerate())
    print("フレーム数:", wf.getnframes())
    print("パラメータ:", wf.getparams())
    print("長さ(秒):", float(wf.getnframes()) / wf.getframerate())

if __name__ == '__main__':
    import sys
    wf = wave.open(sys.argv[1],'rb')
    printWaveInfo(wf)

    buffer = wf.readframes(wf.getnframes())
    print("バッファ長:", len(buffer))    # バイト数=１フレーム２バイト　×　フレーム数

    # bufferはバイナリなので2バイトずつ整数（-32768～32767）にまとめる
    data = np.frombuffer(buffer,dtype="int64")
    if wf.getnchannels()==2:
        #左チャネル
        left = data[::2]
        #右チャネル
        right = data[1::2]
    else:
        left=data
        right=[]

    print("左バッファ長:", len(left))
    print("右バッファ長:", len(right))

    winlen = 512
    vol = []
    tm=[]
    for i in range(0,len(left),winlen):
        if i+winlen<len(left):
            v=0
            for j in range(i,i+winlen):
                vleft= left[j] ** 2
                vright=right[j] ** 2
                v += (vleft + vright) / winlen
            vol += [v]
            tm +=[i]

    print("音量長:", len(vol))



    # プロット
    plt.subplot(3,1,1)
    plt.plot(left)
    plt.subplot(3,1,2)
    plt.plot(right)
    plt.subplot(3,1,3)
    plt.plot(tm,vol)
    plt.show()
