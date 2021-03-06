#!/usr/bin/env python3
# -*- coding:utf-8 -*-


from tkinter import *
from tkinter import ttk
from tkinter.filedialog import (askdirectory,askopenfilename,asksaveasfilename)
from tkinter import scrolledtext
import os
import time
import subprocess
import tkinter.messagebox
import pandas as pd
import shutil

class A1:

    def __init__(self, root, frame):
        # 設定變數
        self.root = root            #本體
        self.frame = frame          #畫面
        self.label_inputfile = None #顯示input資訊的label
        self.Text_BarcodeFile =None #存放inputfile的路徑
        self.label_output = None    #顯示output資訊的label
        self.label_guppy = None     #存放Guppy版本
        self.label_flowcell =None   #存放folcell版本
        #self.barcodesCombo = None
        #self.modelCombo = None
        #self.tWindowCombo = None
        self.baseCallProcessText = None #顯示輸出的黑色區塊
        self.p = None               #線程變數
        self.p2 = None              #線程變數

        #self.check_barcode=None
        self.coli = []              #用來存放container name
        self.dirPath = None         #放input的資料夾路徑
        self.command = None         #線程指令變數
        self.command2 = None        #線程指令變數
        self.Checkbutton =None      #勾選有沒有要額外使用barcodefile
        self.Checkbutton_Nanoplot =None     #勾選有沒有要額外使用Nanoplot
        self.Checkbutton_Flongle = None  # 勾選是不是用Flongle晶片
        self.inputDirButton = None  #可以選擇inputfile的按鈕

        self.dic = {}               #存放container狀態的字典
        self.var1 = IntVar()        #判斷有沒有要額外使用barcodefile
        self.var2 = IntVar()        #判斷有沒有要額外使用Nanoplot
        self.var3 = IntVar()        # 判斷有沒有要額外使用Flongle

 #       self.name=[]                #用來存放container name
 #       self.stats=[]               #用來存放container stats

    # 建立主體頁面
    def createTab(self):
        #查詢container狀態
        def docekr_stat(self):
            comm2 = 'docker ps --all --format \"{{.Names}}\t{{.Status}}\"'
            trr = subprocess.getoutput(comm2)
            stats_list = trr.split('\n')
            #n = 0
            for i in stats_list:
                #print(i)
                self.coli.append(i.split('\t')[0])
#                self.stats.append(i.split('\t')[1].split(' ')[0])
                self.dic.setdefault(i.split('\t')[0], i.split('\t')[1].split(' ')[0])

        docekr_stat(self)

        # padx 前置空白， pady 上置空白
        # process text
#        self.baseCallProcessText = scrolledtext.ScrolledText(self.frame, height=30, width=60, font=("Courier", 14), background="black",foreground="white")
    # 放UI元件
        # 執行按鈕
        runButton = Button(self.frame, text="Run", font=("Courier", 16), width=10, height=1, fg="blue",
                           command=(lambda: self.runBasicQC()))
        runButton.grid(row=20, column=0, pady=5, padx=5, sticky="W")
        # 離開按鈕
        quitButton = Button(self.frame, text="Quit", font=("Courier", 16), width=10, height=1, fg="red",
                            command=(lambda: self.quitToolkit()))
        quitButton.grid(row=20, column=1, pady=5, padx=5, sticky="W")

        # process text
        # #顯示執行狀態
        self.baseCallProcessText = scrolledtext.ScrolledText(self.frame, height=15, width=81,font=("Courier", 14), background="black", foreground="white")
        self.baseCallProcessText.grid(row=21, column=0, columnspan=9, padx=5, sticky="W")
        self.baseCallProcessText.insert(1.0, "!----Ready----!\n")

        # input file text
        Label(self.frame, text="Input Sequencing Summary file:", font=('Courier', 12)).grid(row=1, column=0, padx=5, pady=5)
        self.label_inputfile = Text(self.frame, height=2, width=50, state="normal", font=("Courier", 16))
        self.label_inputfile.insert(1.0, "Input Sequencing Summary file")
        self.label_inputfile.configure(state='disabled')  # normal/disabled -> 可編輯/不可編輯
            #input file button
        inputDirButton = Button(self.frame, text="Browse", font=("Courier", 16), width=12, height=1,
                                command=(lambda: self.selectInputfile(self.label_inputfile, "/")))
        inputDirButton.grid(row=1, column=1, sticky="W")
        self.label_inputfile.grid(row=1, column=2, columnspan=5, padx=5, sticky="W")

        #out file text
        Label(self.frame, text="Output file:", font=('Courier', 12)).grid(row=2, column=0, padx=5, pady=5)
        self.label_output = Text(self.frame, height=2, width=50, state="normal", font=("Courier", 16))
        self.label_output.insert(1.0, "Outputfile")
        self.label_output.configure(state='normal')  # normal/disabled -> 可編輯/不可編輯
        self.label_output.grid(row=2, column=2, columnspan=5, padx=5, sticky="W")

        # 判斷有沒有要用barcode file
        def check_barcode_buttion():
            checkButton = self.var1.get()
            if checkButton ==1 :

                self.Text_BarcodeFile = Text(self.frame, height=2, width=50, state="normal", font=("Courier", 16))
                self.Text_BarcodeFile.configure(state='disabled')
                self.Text_BarcodeFile.grid(row=4, column=2, columnspan=5, padx=5, sticky="W")
                #input file button #如果勾選要使用，就顯示可輸入的欄位
                self.inputDirButton = Button(self.frame, text="Browse", font=("Courier", 16), width=12, height=1,
                                    command=(lambda: self.selectfile(self.Text_BarcodeFile, "/")))
                self.inputDirButton.grid(row=4, column=1, sticky="W")
            elif checkButton ==0:
                self.Text_BarcodeFile.grid_remove()
                self.inputDirButton.grid_remove()


    # setup check_barcode
        #
        self.Checkbutton=Checkbutton(self.frame,text= "--Use barcode file",onvalue = 1, offvalue = 0,variable=self.var1, height=2, width=20, state="normal", font=("Courier", 16),command=check_barcode_buttion)
        self.Checkbutton.grid(row=4, column=0, sticky="W", padx=5, pady=5)

    # setup check_Nanoplot
        #
        self.Checkbutton_Nanoplot = Checkbutton(self.frame, text="--Use Nanoplot    ", onvalue=0, offvalue=1, variable=self.var2,
                                       height=2, width=20, state="normal", font=("Courier", 16)               )
        self.Checkbutton_Nanoplot.grid(row=5, column=0, sticky="W", padx=5, pady=5)

    #setup check_Flongle
        #
        self.Checkbutton_Flongle = Checkbutton(self.frame, text="--Use Flongle    ", onvalue=1, offvalue=0,
                                                variable=self.var3,
                                                height=2, width=20, state="normal", font=("Courier", 16))
        self.Checkbutton_Flongle.grid(row=5, column=1, sticky="W", padx=5, pady=5)



    #setup label_guppy
        Label(self.frame, text="Guppy Version:",font=('Courier',16)).grid(row=10, column=0, padx=5, pady=5)
        self.label_guppy = Text(self.frame, height=1, width=10, state="normal",font=("Courier", 16))
        self.label_guppy.insert(1.0,"")
        self.label_guppy.grid(row=10,column=1,sticky="W")

    #setup label_flowcell
        Label(self.frame, text="flowcell name:",font=('Courier',16)).grid(row=11, column=0, padx=5, pady=5)
        self.label_flowcell = Text(self.frame, height=1, width=10, state="normal",font=("Courier", 16))
        self.label_flowcell.insert(1.0,"")
        self.label_flowcell.grid(row=11,column=1,sticky="W")
        #check

    #show Container ID & stats
        Label(self.frame, text="Container Name:", font=('Courier', 12)).grid(row=0, column=0, padx=5, pady=5)

        def bs(*args):
            # print(self.combo.get())
            containerID = self.combo.get()
            check = self.dic[containerID]
            # print(check)
            if 'Exited' in check:
                self.mx = tkinter.messagebox.askquestion('Warning',
                                                         'This container ' + containerID + ' is closed ,do  you want to open it?')

                if self.mx == 'yes':
                    comm = 'docker start ' + containerID + ''
                    subprocess.getoutput(comm)
                    print('open', containerID)
                    self.dic[containerID]='Up'
                else:
                    print('cancel')
            docekr_stat(self)


        self.combo = ttk.Combobox(self.frame, values=self.coli,
                                  state="readonly")  # 設定顯示在哪個視窗/設定選單的選項/設定選單中的選項是否能修改或是只能讀取
        self.combo.grid(row=0, column=1, sticky="W")  # 調整下拉選單元件的位置
#        self.combo.bind("<<ComboboxSelected>>", bs)  # 偵測選單選項執行函數功能
        #print (self.coli)
        # set container defult
        if 'basicQC' in self.coli:
            #set defult
            self.combo.current(self.coli.index('basicQC'))

    # not use
    def showStdOut(self, pipe, mask):
        oData = os.read(pipe.fileno(), 1 << 20)  # fileno, file descriptor for the stream

        self.baseCallProcessText.insert(END, oData.strip(b'\n').decode())
        self.baseCallProcessText.see(END)
        self.baseCallProcessText.update_idletasks()
    # shutdown UI
    def quitToolkit(self):
        if self.p is None:
            # exit GUI
            self.root.destroy()
            return

        # exit subprocess
        self.p.terminate()

        # force kill subprocess, if subprocess is alive
        def kill_after(countdown):
            if self.p.poll() is None:  # subprocess still exist
                countdown -= 1
                if countdown < 0:  # force kill
                    self.p.kill()
                else:
                    self.root.after(1000, kill_after, countdown)
                    return

            self.p.stdout.close()  # close p
            self.p.wait()  # wait for the p exit
            self.root.destroy()  # exit GUI

        kill_after(countdown=5)

    # find function for inputfile
    def selectInputfile(self, textObject, targetDirectory):
        #print (targetDirectory)  #放的是 要從哪個目錄開始找
        fileName = askopenfilename(initialdir=targetDirectory, title="Select Input sequencing_summary")
        dirPath_index = fileName.rfind('/')
        self.dirPath=fileName[:dirPath_index]+'/'
        self.FN = fileName      #FN ,我猜是fileName的縮寫,然後給一些資訊
        if fileName:
            textObject.configure(state='normal', font=("Courier", 14))
            textObject.delete(1.0, END)
            textObject.insert(1.0, fileName)
            textObject.configure(state='disabled')

            self.label_output.delete(1.0, END)
            if 'sequencing_summary_' in fileName:
                outputName=fileName.split('sequencing_summary_')[1].replace('.txt','')
                self.label_output.insert(1.0, '{}{}.html'.format(self.dirPath,outputName))
    # 這上下兩個應該是一樣的,只是我不小心多複製,且都引用了
    def selectfile(self, textObject, targetDirectory):
        #print (targetDirectory)  #放的是 要從哪個目錄開始找
        fileName = askopenfilename(initialdir=targetDirectory, title="Select Input sequencing_summary")
        dirPath_index = fileName.rfind('/')
        self.dirPath=fileName[:dirPath_index]+'/'
        self.FN = fileName      #FN ,我猜是fileName的縮寫,然後給一些資訊
        if fileName:
            textObject.configure(state='normal', font=("Courier", 14))
            textObject.delete(1.0, END)
            textObject.insert(1.0, fileName)
            textObject.configure(state='disabled')

    # find function for outputfile
    def selectoutfile(self, textObject, targetDirectory):
        #print (targetDirectory)  #放的是 要從哪個目錄開始找
        outputFileName = asksaveasfilename(initialdir=targetDirectory, title="Select outputfile" )
        self.outputFN = outputFileName      #FN ,我猜是fileName的縮寫,然後給一些資訊
        if outputFileName:
            textObject.configure(state='normal', font=("Courier", 14))
            textObject.delete(1.0, END)
            textObject.insert(1.0, outputFileName)
            textObject.configure(state='disabled')

    # Run function
    def runBasicQC(self):
        print(
"""
# **inputFile** - this should be the sequencing_summary.txt from Guppy etc\n
# move your own sequence_summary.txt file (or concatenation thereof) to the\n
# RawData folder to run analysis on your own sequence collection\n\n
# **barcodeFile** - if Guppy_barcoder has been used to demultiplex library,\n
# move the barcoding_summary.txt file to the RawData folder and update variable\n\n
# **basecaller** and **flowcellId** - are used for presentation in report\n
# please update to correspond to your sequence analysis\n\n
# change the **tutorialText** value to FALSE to mask  tutorial instructions(base) \n
    
===========================================================
# -b [barcodeFile]     : \t if you have barcodeFile ,you can use -b option. input barcodeFile
# -o [outputFile name] : \t If you want to change the output file name, you cat give output filename. (default:  partial inputFile information)
==========================================================
""")


        inputFile = self.label_inputfile.get(1.0, END).strip()
        dockername = self.combo.get()
        Text_BarcodeFile =None
        label_flowcell=self.label_flowcell.get(1.0,END).strip()
        label_guppy=self.label_guppy.get(1.0,END).strip()
        outputFile=self.label_output.get(1.0,END).strip()
        tutorialText="FALSE"
        if not outputFile.endswith('.html'):
            outputFile=outputFile+'.html'
        checkButton = self.var1.get()

        checkButton_Nanoplot = self.var2.get()
        Checkbutton_Flongle = self.var3.get()
        f=open(inputFile)
        line1=f.readline()
        line2=f.readline()
        line3=f.readline()
        line4=f.readline()
        f.close()

        #判斷continer有沒有開啟
        print('=')
        if self.dic[dockername] =='Exited':

            self.mx = tkinter.messagebox.askquestion('Warning',
                                                         'This container ' + dockername + ' is closed ,do  you want to open it?')

            if self.mx == 'yes':
                comm = 'docker start {} '.format(dockername)
                subprocess.getoutput(comm)
                print('start \t {}'.format(dockername))
                self.dic[dockername] = 'Up'
            else:
                print('cancel')
                return 0
        # 判斷有沒有寫的權限
        outputdir_num=outputFile.rfind('/')
        output_path=outputFile[:outputdir_num]
        if not os.access( output_path, os.W_OK)  or  not os.access( '/tmp', os.W_OK):
            self.mx = tkinter.messagebox.showerror('Error' , 'you don\'t have  permission to write in \n[ {} ]\n or \n[ /tmp ]'.format(output_path) )
            return 0



        #print (self.dic)
        #print (self.coli)
        print('==')

        if checkButton ==0:
            Text_BarcodeFile=''
        elif Text_BarcodeFile ==1 :
            Text_BarcodeFile=self.Text_BarcodeFile.get(1.0,END).strip()
        if 'barcode_arrangement' in line1 or 'barcode_arrangement' in line2 or 'barcode_arrangement' in line3 or 'barcode_arrangement' in line4:
            Text_BarcodeFile=inputFile
        #elif self.
        print ('===')
#        print (inputFile)
#        print (outputFile)
#        print (Text_BarcodeFile)
#        print (dockername)
#        print (label_flowcell)
#        print (label_guppy)
#        print ('checkButton \t{}'.format(checkButton))
#        print('checkButton_Nanoplot \t{}'.format(checkButton_Nanoplot))

        w = open('config.yaml', 'w')
        w.write('inputFile:   \"{}\" \n'.format(inputFile.split('/')[-1]))
        w.write('barcodeFile: \"{}\" \n'.format(Text_BarcodeFile.split('/')[-1]))
        w.write('basecaller:  \"Guppy {}\" \n'.format(label_guppy))
        w.write('flowcellId:  \"{}\" \n'.format(label_flowcell))
        w.write('tutorialText: \"{}\" \n'.format(tutorialText))
        w.write("""\n\n
        # **inputFile** - this should be the sequencing_summary.txt from Guppy etc
        # move your own sequence_summary.txt file (or concatenation thereof) to the
        # RawData folder to run analysis on your own sequence collection\n
        # **barcodeFile** - if Guppy_barcoder has been used to demultiplex library,
        # move the barcoding_summary.txt file to the RawData folder and update variable\n
        # **basecaller** and **flowcellId** - are used for presentation in report
        # please update to correspond to your sequence analysis\n
        # change the **tutorialText** value to FALSE to mask  tutorial instructions(base)\n 
        """)
        w.close()

        com = 'docker cp {} {}:/Run/QCTutorial/'.format(inputFile, dockername)
    #    print(com)
        subprocess.call(com, shell=True)


        if Text_BarcodeFile:
            com = 'docker cp {}  {}:/Run/QCTutorial/'.format(Text_BarcodeFile, dockername)
    #        print(com)
            subprocess.call(com, shell=True)

        com = "docker cp config.yaml {}:/Run/QCTutorial".format(dockername)
    #    print(com)
        subprocess.call(com, shell=True)

        if Checkbutton_Flongle :
            com = "docker exec {}  bash -c \"/Run/QCTutorial/RunTutorialQC_flongle.sh\"".format(dockername)
            self.command=com
        else:
            com = "docker exec {}  bash -c \"/Run/QCTutorial/RunTutorialQC.sh\"".format(dockername)
            self.command=com
        print(com)
        #subprocess.call(com, shell=True)

        self.p=subprocess.Popen(self.command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True,shell=True)
        #self.root.createfilehandler(self.p.stdout, READABLE, self.showStdOut)

        self.baseCallProcessText.insert(END, "Run QCTutorial \n")
        self.baseCallProcessText.update_idletasks()



    # wait self.p (RunTutorialQC) finish
        print ('Running')
        self.baseCallProcessText.insert(END, "Running....BasicQC\n")
        self.baseCallProcessText.update_idletasks()
#        time.sleep(10)
        try :
            stdoutput_p1, erroutput_p1 = self.p.communicate(timeout=600)
        except self.p.TimeoutExpired:
            self.baseCallProcessText.insert(END, "BasicQC time out ,please check proxy or inputfile....\n")
            self.baseCallProcessText.update_idletasks()
            return 0
        #print('####')
        #print ('RunTutorialQC out:\t {}\n'.format(stdoutput_p1))
        #print ('---')
        #print('RunTutorialQC error:\t {}\n'.format(erroutput_p1))
        #print('####')

#        while  self.p.poll() !=0  :
        #    print (self.p.poll())
#            print ('Running')
#            self.baseCallProcessText.insert(END, "Running....\n")
#            self.baseCallProcessText.update_idletasks()
#            time.sleep(10)

        # Run NanoPlot
        if checkButton_Nanoplot == 0:
            com = "docker exec {}  bash  -c \"/Run/QCTutorial/RunNanoplot.sh\"".format(dockername)
            self.command2 = com
            #    print(com)
            self.p2 = subprocess.Popen(self.command2, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                       universal_newlines=True, shell=True)

            self.baseCallProcessText.insert(END, "Run Nanoplot \n")
            self.baseCallProcessText.update_idletasks()

        #if checkButton_Nanoplot == 0:
            print('Running_Nanoplot')
        # set timeout
        try:
            stdoutput_p2, erroutput_p2 = self.p2.communicate(timeout=600)
            self.baseCallProcessText.insert(END, "Running....Nanoplot\n")
            self.baseCallProcessText.update_idletasks()
        except self.p2.TimeoutExpired:
            self.baseCallProcessText.insert(END, "Nanoplot time out ,please check proxy or inputfile....\n")
            self.baseCallProcessText.update_idletasks()
            return 0
        #print('####')
        #print ('RunNanoplot out:\t {}\n'.format(stdoutput_p2))
        #print ('---')
        #print('RunNanoplot error:\t {}\n'.format(erroutput_p2))
        #print('####')


        #self.p.wait()

        if Checkbutton_Flongle  :
            self.command = "docker cp {}:/Run/QCTutorial/Nanopore_SumStatQC_Tutorial_flongle.html {}".format(dockername, outputFile)
            #print(self.command)
            self.p = subprocess.Popen(self.command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,universal_newlines=True, shell=True)


            self.command = "docker exec {} rm /Run/QCTutorial/Nanopore_SumStatQC_Tutorial_flongle.html".format(dockername)
            #print(self.command)
            self.p = subprocess.Popen(self.command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,universal_newlines=True, shell=True)
        else:
            self.command = "docker cp {}:/Run/QCTutorial/Nanopore_SumStatQC_Tutorial.html {}".format(dockername, outputFile)
            #print(self.command)
            self.p = subprocess.Popen(self.command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,universal_newlines=True, shell=True)


            self.command = "docker exec {} rm /Run/QCTutorial/Nanopore_SumStatQC_Tutorial.html".format(dockername)
            #print(self.command)
            self.p = subprocess.Popen(self.command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,universal_newlines=True, shell=True)

        self.command = "docker exec {} rm /Run/QCTutorial/{}".format(dockername, inputFile.split('/')[-1])
        #print(self.command)
        self.p = subprocess.Popen(self.command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,universal_newlines=True, shell=True)





        if Text_BarcodeFile != inputFile:
            self.command = "docker exec {} rm /Run/QCTutorial/{}".format(dockername, Text_BarcodeFile,inputFile.split('/')[-1])
            #print(self.command)
            self.p = subprocess.Popen(self.command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,universal_newlines=True, shell=True)




        if checkButton_Nanoplot == 0:
            # wait self.p2 (RunNanoplot.sh) finish
            while self.p2.poll() != 0:
                #        print (self.p.poll())
                print('Running')
                self.baseCallProcessText.insert(END, "Running....\n")
                self.baseCallProcessText.update_idletasks()
                time.sleep(10)

            if os.path.isdir("/tmp/NanoPlot"):
                shutil.rmtree("/tmp/NanoPlot")
            if os.path.isdir("{}_NanoPlot".format(outputFile.replace('.html', ''))):
                shutil.rmtree("{}_NanoPlot".format(outputFile.replace('.html', '')))  #rmdir

            self.command2 = "docker cp {}:/Run/QCTutorial/NanoPlot /tmp/NanoPlot".format(dockername)
            print(self.command2)
            self.p2 = subprocess.Popen(self.command2, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                       universal_newlines=True, shell=True)


            while self.p2.poll() != 0:
                #        print (self.p.poll())
                print('Running')
                self.baseCallProcessText.insert(END, "Running....\n")
                self.baseCallProcessText.update_idletasks()
                time.sleep(10)


            self.command2 = "mv /tmp/NanoPlot {}_NanoPlot".format(outputFile.replace('.html', ''))
            print(self.command2)
            self.p2 = subprocess.Popen(self.command2, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                       universal_newlines=True, shell=True)



            self.command2 = "docker exec {} rm /Run/QCTutorial/NanoPlot -r".format(dockername)
            print(self.command2)
            self.p2 = subprocess.Popen(self.command2, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                       universal_newlines=True, shell=True)

            if 'ERROR:' in stdoutput_p2 :
                self.baseCallProcessText.insert(END, "###ERROR!!!!\nCan't create NanoPlot outputDir:\nlease check input file.\n\nlogfile_dir:\t{}_NanoPlot\n".format(outputFile.replace('.html', '')))
            else:
                self.baseCallProcessText.insert(END, "NanoPlot outputdir:\t{}_NanoPlot\n".format(outputFile.replace('.html', '')))
        if 'Nanopore_SumStatQC_Tutorial.html' in stdoutput_p1 or 'Nanopore_SumStatQC_Tutorial_flongle.html' in  stdoutput_p1:
            self.baseCallProcessText.insert(END, "QCTutorial outputFIle:\t{}\nFinish!!!!\n======================\n".format(outputFile))
        elif 'Error' in stdoutput_p1 or 'Execution halted' in stdoutput_p1:
            self.baseCallProcessText.insert(END,
                                            "###ERROR!!!!\nCan't create QCTutorial outputFIle:\nPlease check input file.\n======================\n")
        else:
            self.baseCallProcessText.insert(END,
                                            "###ERROR!!!!\nCan't create QCTutorial outputFIle:\nPlease check input file!!!\n======================\n")
        self.baseCallProcessText.see(END)
        self.baseCallProcessText.update_idletasks()



