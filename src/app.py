import gui_template.template as tmpl
import nav_alg as na
import wx
import re

class MainWindow(tmpl.MainFrame): 


    def __init__(self,parent): 
        tmpl.MainFrame.__init__(self,parent)  
        self.nav_alg = na.nav_alg()
        self.is_input_invalid = False

    def input_check_float(self, obj):
        
        result = re.search(r'[^0-9\.]',obj.GetValue(),flags=re.IGNORECASE)
        obj.SetBackgroundColour("white")

        if result != None:
            obj.SetBackgroundColour("red")
            self.is_input_invalid = True
    
    def input_check_int(self, obj):
        
        result = re.search(r'[^0-9]',obj.GetValue(),flags=re.IGNORECASE)
        obj.SetBackgroundColour("white")

        if result != None:
            obj.SetBackgroundColour("red")
            self.is_input_invalid = True

    def run_analysis(self, event):
        
        self.input_check_int(self.m_enter_freq)
        self.input_check_int(self.m_enter_points_num)
        self.input_check_float(self.m_enter_lat)
        self.input_check_float(self.m_enter_lon)
        self.input_check_float(self.m_enter_gyr_offset)
        self.input_check_float(self.m_enter_acc_offset)
        self.input_check_float(self.m_enter_gyr_drift)
        self.input_check_float(self.m_enter_acc_drift)

        if self.is_input_invalid:
            wx.MessageBox("Введен некорректный символ")
            self.is_input_invalid = False
            return
        

        selection = self.m_analysis_type.GetSelection()
        self.nav_alg = na.nav_alg(
            frequency=int(self.m_enter_freq.GetValue()),
            points_count=int(self.m_enter_points_num.GetValue())
        )

        self.nav_alg.set_coordinates(
            lat = float(self.m_enter_lat.GetValue()),
            lon = float(self.m_enter_lon.GetValue())
        )
        
        if selection == 0: # offset analysis
            g_offset = float(self.m_enter_gyr_offset.GetValue())
            a_offset = float(self.m_enter_acc_offset.GetValue())
            self.nav_alg.set_a_body(a_offset, a_offset, a_offset)
            self.nav_alg.set_w_body(g_offset, g_offset, g_offset)
        elif selection == 1: # drift analisis
            g_drift = float(self.m_enter_gyr_drift.GetValue())
            a_drift = float(self.m_enter_acc_drift.GetValue())
            self.nav_alg.set_a_body(a_drift, a_drift, a_drift)
            self.nav_alg.set_w_body(g_drift, g_drift, g_drift)

        wx.MessageBox("Running")
        self.nav_alg.analysis()
        self.nav_alg.plots()
        wx.MessageBox("All done")
        
app = wx.App(False) 
frame = MainWindow(None) 
frame.Show(True) 
#start the applications 
app.MainLoop() 