
#module import
try:
    import gtk
except:
    print "Gtk not found."
    sys.exit(0)

try:
    import pygtk
    pygtk.require('2.0')
except:
    print "PyGtk not found."
    sys.exit(0)

import numpy as np
import matplotlib.pyplot as plt

import Waveform_PresetAmp as Wav
reload(Wav)
import qt

if 'AWG' in locals():
    AWG._ins._visainstrument.close()   # Trying to close previous AWG session. 

       
AWG = qt.instruments.create('AWG', 'Tektronix_AWG5014', address="10.21.64.191")


class Window:
    def __init__(self):
        #initializing the variables
        #default values
        #also change the set_active values to make change in GUI if changing the default values
        self.num_seg = 3
        self.time_units = "ms"
        self.amp_units = "mV"
        self.awg_clock = 1e8
        self.max_amp = 1   # Maximum amplitude in Volts
        
        #gui initialization from the glade file
        self.gladefile = "awg_gui.glade"
        self.builder = gtk.Builder()
        self.builder.add_from_file(self.gladefile)
        
        self.window = self.builder.get_object("window1")
        self.statusbar = self.builder.get_object("statusbar1")
        self.context_id = self.statusbar.get_context_id("status")
        self.treeview = self.builder.get_object("treeview1")
        self.window.show()

        self.builder.connect_signals(self)


        AWG.set_ch1_amplitude(self.max_amp)  # Setting maximum needed amp on all AWG channels
        AWG.set_ch2_amplitude(self.max_amp) 
        AWG.set_ch3_amplitude(self.max_amp) 
        AWG.set_ch4_amplitude(self.max_amp) 
   
        
        AWG.del_waveform_all()  # Clear all waveforms in waveform list
        AWG.set_clock(self.awg_clock)  # Set AWG clock
        
        #create a waveform object
        self.wav_obj = Wav.Waveform(waveform_name = 'WAV1', AWG_clock = self.awg_clock, TimeUnits = self.time_units , AmpUnits = self.amp_units)
  


        #treeview model
        self.treeview_list = gtk.ListStore(str,str,str,str,str,str,str,str,str,str,str,str,str,str)
        self.treeview.set_model(self.treeview_list)
        #note that this has only 13 columns, the first column since depends on the segment number has to inserted at the first position manually
        self.default_treeview_list = [0.001,0,'L','L',0,'L','L',0,'L','L',0,'L','L']
        for i in range(self.num_seg):
            self.treeview_list.append([i+1] + self.default_treeview_list)
        
        self.renderer_text = gtk.CellRendererText()
        self.column_text = gtk.TreeViewColumn("Segment",self.renderer_text,text=0)
        self.column_text.set_expand(True)
        self.treeview.append_column(self.column_text)

        self.renderer_time = gtk.CellRendererText()
        self.renderer_time.set_property("editable",True)
        self.column_time = gtk.TreeViewColumn("Time",self.renderer_time,text=1)
        self.column_time.set_expand(True)
        self.treeview.append_column(self.column_time)
        
        self.renderer_ch1_a = gtk.CellRendererText()
        self.renderer_ch1_a.set_property("editable",True)
        self.renderer_ch1_a.set_property("background","red")
        self.column_ch1_a = gtk.TreeViewColumn("Analog",self.renderer_ch1_a,text=2)
        self.column_ch1_a.set_expand(True)
        self.treeview.append_column(self.column_ch1_a)
        
        self.renderer_ch1_m1 = gtk.CellRendererText()
        self.renderer_ch1_m1.set_property("editable",True)
        self.renderer_ch1_m1.set_property("background","red")
        self.column_ch1_m1 = gtk.TreeViewColumn("M1",self.renderer_ch1_m1,text=3)
        self.column_ch1_m1.set_expand(True)
        self.treeview.append_column(self.column_ch1_m1)

        self.renderer_ch1_m2 = gtk.CellRendererText()
        self.renderer_ch1_m2.set_property("editable",True)
        self.renderer_ch1_m2.set_property("background","red")
        self.column_ch1_m2 = gtk.TreeViewColumn("M2",self.renderer_ch1_m2,text=4)
        self.column_ch1_m2.set_expand(True)
        self.treeview.append_column(self.column_ch1_m2)

        self.renderer_ch2_a = gtk.CellRendererText()
        self.renderer_ch2_a.set_property("editable",True)
        self.renderer_ch2_a.set_property("background","green")
        self.column_ch2_a = gtk.TreeViewColumn("Analog",self.renderer_ch2_a,text=5)
        self.column_ch2_a.set_expand(True)
        self.treeview.append_column(self.column_ch2_a)
        
        self.renderer_ch2_m1 = gtk.CellRendererText()
        self.renderer_ch2_m1.set_property("editable",True)
        self.renderer_ch2_m1.set_property("background","green")
        self.column_ch2_m1 = gtk.TreeViewColumn("M1",self.renderer_ch2_m1,text=6)
        self.column_ch2_m1.set_expand(True)
        self.treeview.append_column(self.column_ch2_m1)

        self.renderer_ch2_m2 = gtk.CellRendererText()
        self.renderer_ch2_m2.set_property("editable",True)
        self.renderer_ch2_m2.set_property("background","green")
        self.column_ch2_m2 = gtk.TreeViewColumn("M2",self.renderer_ch2_m2,text=7)
        self.column_ch2_m2.set_expand(True)
        self.treeview.append_column(self.column_ch2_m2)
        
        self.renderer_ch3_a = gtk.CellRendererText()
        self.renderer_ch3_a.set_property("editable",True)
        self.renderer_ch3_a.set_property("background","blue")
        self.column_ch3_a = gtk.TreeViewColumn("Analog",self.renderer_ch3_a,text=8)
        self.column_ch3_a.set_expand(True)
        self.treeview.append_column(self.column_ch3_a)
        
        self.renderer_ch3_m1 = gtk.CellRendererText()
        self.renderer_ch3_m1.set_property("editable",True)
        self.renderer_ch3_m1.set_property("background","blue")
        self.column_ch3_m1 = gtk.TreeViewColumn("M1",self.renderer_ch3_m1,text=9)
        self.column_ch3_m1.set_expand(True)
        self.treeview.append_column(self.column_ch3_m1)

        self.renderer_ch3_m2 = gtk.CellRendererText()
        self.renderer_ch3_m2.set_property("editable",True)
        self.renderer_ch3_m2.set_property("background","blue")
        self.column_ch3_m2 = gtk.TreeViewColumn("M2",self.renderer_ch3_m2,text=10)
        self.column_ch3_m2.set_expand(True)
        self.treeview.append_column(self.column_ch3_m2)

        self.renderer_ch4_a = gtk.CellRendererText()
        self.renderer_ch4_a.set_property("editable",True)
        self.renderer_ch4_a.set_property("background","cyan")
        self.column_ch4_a = gtk.TreeViewColumn("Analog",self.renderer_ch4_a,text=11)
        self.column_ch4_a.set_expand(True)
        self.treeview.append_column(self.column_ch4_a)
        
        self.renderer_ch4_m1 = gtk.CellRendererText()
        self.renderer_ch4_m1.set_property("editable",True)
        self.renderer_ch4_m1.set_property("background","cyan")
        self.column_ch4_m1 = gtk.TreeViewColumn("M1",self.renderer_ch4_m1,text=12)
        self.column_ch4_m1.set_expand(True)
        self.treeview.append_column(self.column_ch4_m1)

        self.renderer_ch4_m2 = gtk.CellRendererText()
        self.renderer_ch4_m2.set_property("editable",True)
        self.renderer_ch4_m2.set_property("background","cyan")
        self.column_ch4_m2 = gtk.TreeViewColumn("M2",self.renderer_ch4_m2,text=13)
        self.column_ch4_m2.set_expand(True)
        self.treeview.append_column(self.column_ch4_m2)

        self.renderer_time.connect("edited",self.text_edited,1)
        self.renderer_ch1_a.connect("edited",self.text_edited,2)
        self.renderer_ch1_m1.connect("edited",self.text_edited,3)
        self.renderer_ch1_m2.connect("edited",self.text_edited,4)
        self.renderer_ch2_a.connect("edited",self.text_edited,5)
        self.renderer_ch2_m1.connect("edited",self.text_edited,6)
        self.renderer_ch2_m2.connect("edited",self.text_edited,7)
        self.renderer_ch3_a.connect("edited",self.text_edited,8)
        self.renderer_ch3_m1.connect("edited",self.text_edited,9)
        self.renderer_ch3_m2.connect("edited",self.text_edited,10)
        self.renderer_ch4_a.connect("edited",self.text_edited,11)
        self.renderer_ch4_m1.connect("edited",self.text_edited,12)
        self.renderer_ch4_m2.connect("edited",self.text_edited,13)


        #initialization of the list for time and amplitude units
        self.time_units_list = gtk.ListStore(int,str)
        self.time_units_list.append([0,"s"])
        self.time_units_list.append([1,"ms"])
        self.time_units_list.append([2,"us"])
    

        self.amp_units_list = gtk.ListStore(int,str)
        self.amp_units_list.append([0,"V"])
        self.amp_units_list.append([1,"mV"])
        self.amp_units_list.append([2,"uV"])

        #initialization of the comboboxes for time and amplitude units
        self.time_units_box = self.builder.get_object("time_units_box")
        self.time_units_box.set_model(self.time_units_list)
        self.amp_units_box = self.builder.get_object("amp_units_box")
        self.amp_units_box.set_model(self.amp_units_list)
        self.cell = gtk.CellRendererText()
        self.time_units_box.pack_start(self.cell,True)
        self.time_units_box.add_attribute(self.cell, 'text', 1)
        #set_active sets the default value
        self.time_units_box.set_active(1)
        self.amp_units_box.pack_start(self.cell,True)
        self.amp_units_box.add_attribute(self.cell, 'text', 1)
        self.amp_units_box.set_active(1)

        self.statusbar.push(self.context_id, "No. of Segments: " + str(self.num_seg) + " | Time Units: " + str(self.time_units) +  " | Amplitude Units: " + str(self.amp_units) + " | AWG Clock: " + str(self.awg_clock) + " | Max. Amplitude: " + str(self.max_amp)) 


    def on_window1_destroy(self, object, data=None):
        print "AWG GUI quit with cancel button."
        gtk.main_quit()

    def on_num_seg_set_clicked(self, button, data=None):
        self.num_seg_entry = self.builder.get_object("num_seg_entry")
        self.num_seg = int(self.num_seg_entry.get_text())
        print "Number of segments set to",self.num_seg
        self.statusbar.push(self.context_id, "No. of Segments: " + str(self.num_seg) + " | Time Units: " + str(self.time_units) +  " | Amplitude Units: " + str(self.amp_units) + " | AWG Clock: " + str(self.awg_clock) + " | Max. Amplitude: " + str(self.max_amp)) 
        self.treeview_list.clear()
        for i in range(self.num_seg):
            self.treeview_list.append([i+1] + self.default_treeview_list)

    def on_time_units_box_changed(self,widget,data=None):
        self.index = widget.get_active()
        self.model = widget.get_model()
        self.time_units = self.model[self.index][1]
        print "Time units set to",self.time_units
        self.statusbar.push(self.context_id, "No. of Segments: " + str(self.num_seg) + " | Time Units: " + str(self.time_units) +  " | Amplitude Units: " + str(self.amp_units) + " | AWG Clock: " + str(self.awg_clock) + " | Max. Amplitude: " + str(self.max_amp)) 
        self.wav_obj.Change_time_units(self.time_units)
       

    def on_amp_units_box_changed(self,widget,data=None):
        self.index = widget.get_active()
        self.model = widget.get_model()
        self.amp_units = self.model[self.index][1]
        print "Amplitide units units set to",self.amp_units
        self.statusbar.push(self.context_id, "No. of Segments: " + str(self.num_seg) + " | Time Units: " + str(self.time_units) +  " | Amplitude Units: " + str(self.amp_units) + " | AWG Clock: " + str(self.awg_clock) + " | Max. Amplitude: " + str(self.max_amp)) 
        self.wav_obj.Change_amp_units(self.amp_units) 


    def on_awg_clock_set_clicked(self,button,data=None):
        self.awg_clock_entry = self.builder.get_object("awg_clock_entry")
        self.awg_clock = float(self.awg_clock_entry.get_text())
        print "AWG Clock set to",self.awg_clock
        self.statusbar.push(self.context_id, "No. of Segments: " + str(self.num_seg) + " | Time Units: " + str(self.time_units) +  " | Amplitude Units: " + str(self.amp_units) + " | AWG Clock: " + str(self.awg_clock) + " | Max. Amplitude: " + str(self.max_amp)) 
        AWG.set_clock(self.AWG_clock)  # Set AWG clock
    
    def on_max_amp_set_clicked(self,button,data=None):
        self.max_amp_entry = self.builder.get_object("max_amp_entry")
        self.max_amp = float(self.max_amp_entry.get_text())
        print "Maximum Amplitude set to",self.max_amp
        self.statusbar.push(self.context_id, "No. of Segments: " + str(self.num_seg) + " | Time Units: " + str(self.time_units) +  " | Amplitude Units: " + str(self.amp_units) + " | AWG Clock: " + str(self.awg_clock) + " | Max. Amplitude: " + str(self.max_amp)) 
        AWG.set_ch1_amplitude(self.max_amp)  # Setting maximum needed amp on all AWG channels
        AWG.set_ch2_amplitude(self.max_amp) 
        AWG.set_ch3_amplitude(self.max_amp) 
        AWG.set_ch4_amplitude(self.max_amp) 
        

        
    
    def set_marker_from_input_m1(self,i,index):
        #i is the segment index along column
        #index is index along the row
        if self.treeview_list[i][index] == 'L':
            self.seg_list_m1 += [0.0]
        elif self.treeview_list[i][index] == 'H':
            self.seg_list_m1 += [1.0]
        else:
            raise Exception('Error in setting markers - input value must be L or H')

    def set_marker_from_input_m2(self,i,index):
        #i is the segment index along column
        #index is index along the row
        if self.treeview_list[i][index] == 'L':
            self.seg_list_m2 += [0.0]
        elif self.treeview_list[i][index] == 'H':
            self.seg_list_m2 += [1.0]
        else:
            raise Exception('Error in setting markers - input value must be L or H')

    def text_edited(self,widget,path,text,index):

        self.treeview_list[path][index] = text
        if 2 <=index <= 4:
            self.seg_list_a = []
            self.seg_list_m1 = []
            self.seg_list_m2 = []
            for i in range(self.num_seg):
                self.seg_list_a += [[float(self.treeview_list[i][1]),float(self.treeview_list[i][2])]]
                self.set_marker_from_input_m1(i,3)
                self.set_marker_from_input_m2(i,4)

            self.wav_obj.setValuesCH1(*self.seg_list_a)
            self.wav_obj.setMarkersCH1(self.seg_list_m1,self.seg_list_m2)

        elif 5 <=index <= 7:
            self.seg_list_a = []
            self.seg_list_m1 = []
            self.seg_list_m2 = []
            for i in range(self.num_seg):
                self.seg_list_a += [[float(self.treeview_list[i][1]),float(self.treeview_list[i][5])]]
                self.set_marker_from_input_m1(i,6)
                self.set_marker_from_input_m2(i,7)

            self.wav_obj.setValuesCH2(*self.seg_list_a)
            self.wav_obj.setMarkersCH2(self.seg_list_m1,self.seg_list_m2)
        elif 8 <=index <= 10:
            self.seg_list_a = []
            self.seg_list_m1 = []
            self.seg_list_m2 = []
            for i in range(self.num_seg):
                self.seg_list_a += [[float(self.treeview_list[i][1]),float(self.treeview_list[i][8])]]
                self.set_marker_from_input_m1(i,9)
                self.set_marker_from_input_m2(i,10)
            
            self.wav_obj.setValuesCH3(*self.seg_list_a)
            self.wav_obj.setMarkersCH3(self.seg_list_m1,self.seg_list_m2)
        elif 11 <=index <= 13:
            self.seg_list_a = []
            self.seg_list_m1 = []
            self.seg_list_m2 = []
            for i in range(self.num_seg):
                self.seg_list_a += [[float(self.treeview_list[i][1]),float(self.treeview_list[i][11])]]
                self.set_marker_from_input_m1(i,12)
                self.set_marker_from_input_m2(i,13)
              
            self.wav_obj.setValuesCH4(*self.seg_list_a)
            self.wav_obj.setMarkersCH4(self.seg_list_m1,self.seg_list_m2)
        #user only changes the time
        else:
            self.seg_list_a = []
            #channel 1
            for i in range(self.num_seg):
                self.seg_list_a += [[float(self.treeview_list[i][1]),float(self.treeview_list[i][2])]]
            self.wav_obj.setValuesCH1(*self.seg_list_a)
            #channel 2
            self.seg_list_a = []
            for i in range(self.num_seg):
                self.seg_list_a += [[float(self.treeview_list[i][1]),float(self.treeview_list[i][5])]]
            self.wav_obj.setValuesCH2(*self.seg_list_a)
            #channel 3
            self.seg_list_a = []
            for i in range(self.num_seg):
                self.seg_list_a += [[float(self.treeview_list[i][1]),float(self.treeview_list[i][8])]]
            self.wav_obj.setValuesCH3(*self.seg_list_a)
            #channel 4
            self.seg_list_a = []
            for i in range(self.num_seg):
                self.seg_list_a += [[float(self.treeview_list[i][1]),float(self.treeview_list[i][11])]]
            self.wav_obj.setValuesCH4(*self.seg_list_a)

    def convert_marker_to_float(self,val):
        if val == 'H':
            return 1.0
        else:
            return 0.0 

    def on_plot1_clicked(self,widget,data=None):

        points_list_a = [(0,float(self.treeview_list[0][2]))]
        points_list_m1 = [(0,self.convert_marker_to_float(self.treeview_list[0][3]))]
        points_list_m2 = [(0,self.convert_marker_to_float(self.treeview_list[0][4]))]
        t = 0
        for i in range(self.num_seg-1):
            t = t + float(self.treeview_list[i][1])
            points_list_a.append((t,float(self.treeview_list[i][2])))
            points_list_a.append((t,float(self.treeview_list[i+1][2])))
            points_list_m1.append((t,self.convert_marker_to_float(self.treeview_list[i][3])))
            points_list_m1.append((t,self.convert_marker_to_float(self.treeview_list[i+1][3])))
            points_list_m2.append((t,self.convert_marker_to_float(self.treeview_list[i][4])))
            points_list_m2.append((t,self.convert_marker_to_float(self.treeview_list[i+1][4])))
        t = t + float(self.treeview_list[self.num_seg - 1][1])
        points_list_a.append((t,float(self.treeview_list[self.num_seg - 1][2])))
        points_list_m1.append((t,self.convert_marker_to_float(self.treeview_list[self.num_seg - 1][3])))
        points_list_m2.append((t,self.convert_marker_to_float(self.treeview_list[self.num_seg - 1][4])))


        f, axarr = plt.subplots(3, sharex=True)
        for item in axarr:
            item.spines['top'].set_visible(False)
            item.spines['bottom'].set_visible(False)
        axarr[0].set_title("Channel 1")
        axarr[0].plot(*zip(*points_list_a),color='r',linewidth=1.0,label="Analog")
        axarr[0].legend()
        axarr[0].set_ylabel("Amplitide[" + self.amp_units + "]")
        axarr[1].plot(*zip(*points_list_m1),color='r',linewidth=1.0,label="Marker 1")
        axarr[1].legend()
        axarr[1].set_ylim([-0.1,1.1])
        axarr[2].plot(*zip(*points_list_m2),color='r',linewidth=1.0,label="Marker 2")
        axarr[2].set_ylim([-0.1,1.1])
        axarr[2].legend()
        axarr[2].set_xlabel("Time[" + self.time_units + "]")
        plt.show()

    def on_plot2_clicked(self,widget,data=None):
        points_list_a = [(0,float(self.treeview_list[0][5]))]
        points_list_m1 = [(0,self.convert_marker_to_float(self.treeview_list[0][6]))]
        points_list_m2 = [(0,self.convert_marker_to_float(self.treeview_list[0][7]))]
        t = 0
        for i in range(self.num_seg-1):
            t = t + float(self.treeview_list[i][1])
            points_list_a.append((t,float(self.treeview_list[i][5])))
            points_list_a.append((t,float(self.treeview_list[i+1][5])))
            points_list_m1.append((t,self.convert_marker_to_float(self.treeview_list[i][6])))
            points_list_m1.append((t,self.convert_marker_to_float(self.treeview_list[i+1][6])))
            points_list_m2.append((t,self.convert_marker_to_float(self.treeview_list[i][7])))
            points_list_m2.append((t,self.convert_marker_to_float(self.treeview_list[i+1][7])))
        t = t + float(self.treeview_list[self.num_seg - 1][1])
        points_list_a.append((t,float(self.treeview_list[self.num_seg - 1][5])))
        points_list_m1.append((t,self.convert_marker_to_float(self.treeview_list[self.num_seg - 1][6])))
        points_list_m2.append((t,self.convert_marker_to_float(self.treeview_list[self.num_seg - 1][7])))


        f, axarr = plt.subplots(3, sharex=True)
        for item in axarr:
            item.spines['top'].set_visible(False)
        axarr[0].set_title("Channel 2")
        axarr[0].plot(*zip(*points_list_a),color='g',linewidth=1.0,label="Analog")
        axarr[0].legend()
        axarr[0].set_ylabel("Amplitide[" + self.amp_units + "]")
        axarr[1].plot(*zip(*points_list_m1),color='g',linewidth=1.0,label="Marker 1")
        axarr[1].legend()
        axarr[1].set_ylim([-0.1,1.1])
        axarr[2].plot(*zip(*points_list_m2),color='g',linewidth=1.0,label="Marker 2")
        axarr[2].set_ylim([-0.1,1.1])
        axarr[2].legend()
        axarr[2].set_xlabel("Time[" + self.time_units + "]")
        plt.show()

    def on_plot3_clicked(self,widget,data=None):
        points_list_a = [(0,float(self.treeview_list[0][8]))]
        points_list_m1 = [(0,self.convert_marker_to_float(self.treeview_list[0][9]))]
        points_list_m2 = [(0,self.convert_marker_to_float(self.treeview_list[0][10]))]
        t = 0
        for i in range(self.num_seg-1):
            t = t + float(self.treeview_list[i][1])
            points_list_a.append((t,float(self.treeview_list[i][8])))
            points_list_a.append((t,float(self.treeview_list[i+1][8])))
            points_list_m1.append((t,self.convert_marker_to_float(self.treeview_list[i][9])))
            points_list_m1.append((t,self.convert_marker_to_float(self.treeview_list[i+1][9])))
            points_list_m2.append((t,self.convert_marker_to_float(self.treeview_list[i][10])))
            points_list_m2.append((t,self.convert_marker_to_float(self.treeview_list[i+1][10])))
        t = t + float(self.treeview_list[self.num_seg - 1][1])
        points_list_a.append((t,float(self.treeview_list[self.num_seg - 1][8])))
        points_list_m1.append((t,self.convert_marker_to_float(self.treeview_list[self.num_seg - 1][9])))
        points_list_m2.append((t,self.convert_marker_to_float(self.treeview_list[self.num_seg - 1][10])))


        f, axarr = plt.subplots(3, sharex=True)
        for item in axarr:
            item.spines['top'].set_visible(False)
        axarr[0].set_title("Channel 3")
        axarr[0].plot(*zip(*points_list_a),color='b',linewidth=1.0,label="Analog")
        axarr[0].legend()
        axarr[0].set_ylabel("Amplitide[" + self.amp_units + "]")
        axarr[1].plot(*zip(*points_list_m1),color='b',linewidth=1.0,label="Marker 1")
        axarr[1].legend()
        axarr[1].set_ylim([-0.1,1.1])
        axarr[2].plot(*zip(*points_list_m2),color='b',linewidth=1.0,label="Marker 2")
        axarr[2].set_ylim([-0.1,1.1])
        axarr[2].legend()
        axarr[2].set_xlabel("Time[" + self.time_units + "]")
        plt.show()

    def on_plot4_clicked(self,widget,data=None):
        points_list_a = [(0,float(self.treeview_list[0][11]))]
        points_list_m1 = [(0,self.convert_marker_to_float(self.treeview_list[0][12]))]
        points_list_m2 = [(0,self.convert_marker_to_float(self.treeview_list[0][13]))]
        t = 0
        for i in range(self.num_seg-1):
            t = t + float(self.treeview_list[i][1])
            points_list_a.append((t,float(self.treeview_list[i][11])))
            points_list_a.append((t,float(self.treeview_list[i+1][11])))
            points_list_m1.append((t,self.convert_marker_to_float(self.treeview_list[i][12])))
            points_list_m1.append((t,self.convert_marker_to_float(self.treeview_list[i+1][12])))
            points_list_m2.append((t,self.convert_marker_to_float(self.treeview_list[i][13])))
            points_list_m2.append((t,self.convert_marker_to_float(self.treeview_list[i+1][13])))
        t = t + float(self.treeview_list[self.num_seg - 1][1])
        points_list_a.append((t,float(self.treeview_list[self.num_seg - 1][11])))
        points_list_m1.append((t,self.convert_marker_to_float(self.treeview_list[self.num_seg - 1][12])))
        points_list_m2.append((t,self.convert_marker_to_float(self.treeview_list[self.num_seg - 1][13])))


        f, axarr = plt.subplots(3, sharex=True)
        for item in axarr:
            item.spines['top'].set_visible(False)
        axarr[0].set_title("Channel 4")
        axarr[0].plot(*zip(*points_list_a),color='c',linewidth=1.0,label="Analog")
        axarr[0].legend()
        axarr[0].set_ylabel("Amplitide[" + self.amp_units + "]")
        axarr[1].plot(*zip(*points_list_m1),color='c',linewidth=1.0,label="Marker 1")
        axarr[1].legend()
        axarr[1].set_ylim([-0.1,1.1])
        axarr[2].plot(*zip(*points_list_m2),color='c',linewidth=1.0,label="Marker 2")
        axarr[2].set_ylim([-0.1,1.1])
        axarr[2].legend()
        axarr[2].set_xlabel("Time[" + self.time_units + "]")
        plt.show()

    def on_awg_upload_clicked(self,button,data=None):
        self.wav_obj.CH4.rescaleAmplitude(self.AWGMax_amp)

        AWG.send_waveform_object(Wav = self.wav_obj.CH4, path = 'C:\SEQwav\\')
        AWG.import_waveform_object(Wav = self.wav_obj.CH4, path = 'C:\SEQwav\\')
        AWG.import_waveform_object(Wav = self.wav_obj.CH4, path = 'C:\SEQwav\\')
        AWG.load_waveform(3, self.wav_obj.CH4.waveform_name, drive='C:', path='C:\SEQwav\\')

    def on_save_waveform_clicked(self,widget,data=None):
        dialog = gtk.FileChooserDialog("Save waveform",self.window,gtk.FILE_CHOOSER_ACTION_SAVE,(gtk.STOCK_SAVE,gtk.RESPONSE_ACCEPT,gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL))
        dialog.set_property("do-overwrite-confirmation",True)
        dialog.set_current_folder("~/")

        response = dialog.run()

        if response == gtk.RESPONSE_ACCEPT:
            #note that filename also contains the path
            filename = dialog.get_filename()
            #safety first
            if not filename.endswith(".txt"):
                filename += ".txt"
            f = open(filename,'w')
            #write the settings
            f.write("num_seg " + str(self.num_seg) + "\n")
            f.write("time_units " + str(self.time_units) + "\n")
            f.write("amp_units " + str(self.amp_units) + "\n")
            f.write("awg_clock " + str(self.awg_clock) + "\n")
            f.write("max_amp " +  str(self.max_amp) + "\n")
            
            #write the segments in the same format it is visible on the GUI
            for i in range(self.num_seg):
                line = ""
                for j in range(len(self.treeview_list[0])):
                    line += str(self.treeview_list[i][j])
                line += "\n"
                f.write(line)
            f.close()
        dialog.destroy()
    def on_load_waveform_clicked(self,widget,data=None):
        dialog = gtk.FileChooserDialog("Open waveform",self.window,gtk.FILE_CHOOSER_ACTION_OPEN,(gtk.STOCK_OPEN,gtk.RESPONSE_OK,gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL))
        dialog.set_current_folder("~/")

        response = dialog.run()
        if response == gtk.RESPONSE_OK:
            filepath = dialog.get_filename()
            f = open(filepath)
            wav_label = self.builder.get_object("load_waveform_label")
            wav_label.set_text(filepath.split('//')[-1])
            print f
            f.close()
        dialog.destroy()

    def on_open_waveform1_clicked(self,widget,data=None):
        dialog = gtk.FileChooserDialog("Open waveform",self.window,gtk.FILE_CHOOSER_ACTION_OPEN,(gtk.STOCK_OPEN,gtk.RESPONSE_OK,gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL))
        dialog.set_current_folder("~/")

        response = dialog.run()
        if response == gtk.RESPONSE_OK:
            filepath = dialog.get_filename()
            f = open(filepath)
            wav1_label = self.builder.get_object("wav1_label")
            wav1_label.set_text(filepath)
            print f
            f.close()
        dialog.destroy()

    def on_open_waveform2_clicked(self,widget,data=None):
        dialog = gtk.FileChooserDialog("Open waveform",self.window,gtk.FILE_CHOOSER_ACTION_OPEN,(gtk.STOCK_OPEN,gtk.RESPONSE_OK,gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL))
        dialog.set_current_folder("~/")

        response = dialog.run()
        if response == gtk.RESPONSE_OK:
            filepath = dialog.get_filename()
            f = open(filepath)
            wav2_label = self.builder.get_object("wav2_label")
            wav2_label.set_text(filepath)
            print f
            f.close()
        dialog.destroy()


    #helper function
    #load a waveform from a txt file and returns a waveform  object
    #def load_waveform(self,filepath):
    #    f = open(filepath,"r")
    #    for



win = Window()
gtk.main()
        
