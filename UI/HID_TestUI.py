#! /usr/bin/env python
# -*- coding: utf-8 -*-

'''
USB设备主界面
'''
__author__ = "jakey.chen"
__version__ = "v2.0"


import tkinter as tk
import tkinter.ttk
import UI.PyTkinter as pytk


g_font = ('Monaco', 12)


class HIDTestUI(object):

    def __init__(self, master=None):
        self.root = master
        self.create_frame()

    def create_frame(self):
        '''
        新建窗口，分为上下2个部分，下半部分为状态栏
        '''
        self.frm = pytk.PyLabelFrame(self.root)
        self.frm_status = pytk.PyLabelFrame(self.root)

        self.frm.pack(fill="both", expand=1)
        self.frm_status.pack(fill="both", expand=0)

        self.create_frm()
        self.create_frm_status()

    def create_frm(self):
        '''
        上半部分窗口分为左右2个部分
        '''
        self.frm_left = pytk.PyLabelFrame(self.frm)
        self.frm_right = pytk.PyLabelFrame(self.frm)

        self.frm_left.pack(fill="both", expand=1, padx=5, pady=5, side=tk.LEFT)
        self.frm_right.pack(fill="both", expand=1, padx=5, pady=5, side=tk.RIGHT)

        self.create_frm_left()
        self.create_frm_right()

    def create_frm_left(self):
        '''
        上半部分左边窗口：
        Listbox显示连接的USB设备
        Button按钮点击连接设备
        '''
        self.frm_left_label = pytk.PyLabel(self.frm_left,
                                           text="HID Devices",
                                           font=g_font,
                                           anchor="w")
        self.frm_left_listbox = pytk.PyListbox(self.frm_left,
                                               font=g_font)
        self.frm_left_btn = pytk.PyButton(self.frm_left,
                                          text="Open",
                                          font=g_font,
                                          command=self.Toggle)

        self.frm_left_label.pack(fill="both", expand=0, padx=5, pady=5)
        self.frm_left_listbox.pack(fill="both", expand=1, padx=5, pady=5)
        self.frm_left_btn.pack(fill="both", expand=0, padx=5, pady=5)

        self.frm_left_listbox.bind("<Double-Button-1>", self.Open)

    def create_frm_right(self):
        '''
        上半部分右边窗口：
        分为4个部分：
        1、Label显示和重置按钮和发送按钮
        2、Entry显示（发送的数据）
        3、Label显示和十进制选择显示和清除接收信息按钮
        4、Text显示接收到的信息
        '''
        self.frm_right_reset = pytk.PyLabelFrame(self.frm_right)
        self.frm_right_send = pytk.PyLabelFrame(self.frm_right)
        self.frm_right_clear = pytk.PyLabelFrame(self.frm_right)
        self.frm_right_receive = pytk.PyText(self.frm_right,
                                             font=("Monaco", 8))

        self.frm_right_reset.pack(fill="both", expand=0, padx=1)
        self.frm_right_send.pack(fill="both", expand=1, padx=1)
        self.frm_right_clear.pack(fill="both", expand=0, padx=1)
        self.frm_right_receive.pack(fill="both", expand=1, padx=1)

        self.frm_right_receive.tag_config("green", foreground="#228B22")

        self.create_frm_right_reset()
        self.create_frm_right_send()
        self.create_frm_right_clear()

    def create_frm_right_reset(self):
        '''
        1、Label显示和重置按钮和发送按钮
        '''
        self.frm_right_reset_label = pytk.PyLabel(self.frm_right_reset,
                                                  text="Hex Bytes",
                                                  font=g_font,
                                                  anchor="w")
        self.frm_right_reset_btn = pytk.PyButton(self.frm_right_reset,
                                                 text="Reset",
                                                 width=10,
                                                 font=g_font,
                                                 command=self.Reset)
        self.frm_right_send_btn = pytk.PyButton(self.frm_right_reset,
                                                text="Send",
                                                width=10,
                                                font=g_font,
                                                command=self.Send)

        self.frm_right_reset_label.pack(fill="both", expand=1, padx=5, pady=5, side=tk.LEFT)
        self.frm_right_reset_btn.pack(fill="both", expand=0, padx=5, pady=5, side=tk.LEFT)
        self.frm_right_send_btn.pack(fill="both", expand=0, padx=5, pady=5, side=tk.RIGHT)

    def create_frm_right_send(self):
        '''
        2、Entry显示（发送的数据）用64个Entry来显示
        '''
        self.entry_list = list()
        line_frm_1 = pytk.PyFrame(self.frm_right_send)
        line_frm_2 = pytk.PyFrame(self.frm_right_send)
        line_frm_3 = pytk.PyFrame(self.frm_right_send)
        line_frm_4 = pytk.PyFrame(self.frm_right_send)
        line_frm_1.pack(fill="both", expand=1, pady=1)
        line_frm_2.pack(fill="both", expand=1, pady=1)
        line_frm_3.pack(fill="both", expand=1, pady=1)
        line_frm_4.pack(fill="both", expand=1, pady=1)
        for i in range(64):
            temp_str = tk.StringVar()
            if i//16 == 0:
                master = line_frm_1
            elif i//16 == 1:
                master = line_frm_2
            elif i//16 == 2:
                master = line_frm_3
            elif i//16 == 3:
                master = line_frm_4

            temp_entry = pytk.PyEntry(master,
                                      textvariable=temp_str,
                                      width=3,
                                      fg="#1E90FF",
                                      font=g_font)
            temp_str.set("00")
            temp_entry.pack(fill="both", expand=1, padx=1, side=tk.LEFT)
            self.entry_list.append(temp_str)

    def create_frm_right_clear(self):
        '''
        3、Label显示和清除接收信息按钮
        '''
        self.checkValue = tk.IntVar()
        self.frm_right_clear_label = pytk.PyLabel(self.frm_right_clear,
                                                  text="Data Received",
                                                  anchor="w",
                                                  font=g_font)
        self.frm_right_decimal_checkbtn = pytk.PyCheckbutton(self.frm_right_clear,
                                                             text="Decimal",
                                                             variable=self.checkValue,
                                                             relief="flat",
                                                             font=g_font)
        self.frm_right_clear_btn = pytk.PyButton(self.frm_right_clear,
                                                 text="Clear",
                                                 width=10,
                                                 font=g_font,
                                                 command=self.Clear)

        self.frm_right_clear_label.pack(fill="both", expand=1, padx=5, pady=5, side=tk.LEFT)
        self.frm_right_decimal_checkbtn.pack(fill="both", expand=0, padx=5, pady=5, side=tk.LEFT)
        self.frm_right_clear_btn.pack(fill="both", expand=0, padx=5, pady=5, side=tk.RIGHT)

    def create_frm_status(self):
        '''
        下半部分状态栏窗口
        '''
        self.frm_status_label = pytk.PyLabel(self.frm_status,
                                             text="Ready",
                                             font=g_font)
        self.frm_status_label.grid(
            row=0, column=0, padx=5, pady=5, sticky="wesn")

    def Toggle(self):
        pass

    def Open(self, event):
        pass

    def Reset(self):
        for entry in self.entry_list:
            entry.set("00")

    def Send(self):
        pass

    def Clear(self):
        self.frm_right_receive.delete("0.0", "end")


if __name__ == '__main__':
    '''
    main loop
    '''
    root = tk.Tk()
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    root.title(r"HID-Test")

    HIDTestUI(root)
    root.mainloop()
