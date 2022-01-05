#!python3

from tkinter import *
import time
import math
from tkinter import font


# ------------------- Launch Window ---------------
class Splash(Toplevel):
    def __init__(self, parent):
        Toplevel.__init__(self, parent)
        self.title("Splash")
        self.launch_bg = PhotoImage(file="includes/launch_bg.gif")
        self.w = self.launch_bg.width()
        self.h = self.launch_bg.height()
        self.canvasl = Canvas(self, height=self.h, width=self.w, bd=-2)
        self.bgl_label = self.canvasl.create_image((0, 0), image=self.launch_bg, anchor=N + W)
        self.canvasl.pack()
        self.wm_overrideredirect(True)
        self.resizable(False, False)
        # -----Center Align ----------------------
        self.update_idletasks()
        self.x = (self.winfo_screenwidth() // 2) - (self.w // 2)
        self.y = (self.winfo_screenheight() // 2) - (self.h // 2)
        self.geometry('{}x{}+{}+{}'.format(self.w, self.h, self.x, self.y))
        # ------------- required to make window show before the program gets to the mainloop
        self.update()


# ------------------- Result Window ---------------
class Results():
    # -------- Minimise Window ----
    def minim(self, event):
        self.r_window.overrideredirect(False)
        self.r_window.wm_state("iconic")

    def frame_mapped(self, e):
        self.r_window.update_idletasks()
        self.r_window.overrideredirect(True)
        self.r_window.state('normal')

    # ------- Move Window -------
    def move_window_results(self, event):
        self.r_window.geometry('+{0}+{1}'.format(event.x_root, event.y_root))

    # ------- Close Button ------
    def close(self, event):
        self.r_window.destroy()

    # ------- Mouse Hovering Effects --
    def on_enter_close(self, event):
        self.close_button_results_hover = PhotoImage(file="includes/close_button_enter.gif")
        self.close_button_results_hover_label = self.canvasl.create_image((437.00, 11.00),
                                                                          image=self.close_button_results_hover)
        self.canvasl.tag_bind(self.close_button_results_hover_label, "<Button-1>", self.close)
        self.canvasl.tag_bind(self.close_button_results_hover_label, "<Leave>", self.on_leave_close)

    def on_leave_close(self, event):
        self.close_button_results_leave = PhotoImage(file="includes/close_button_leave.gif")
        self.close_button_results_leave_label = self.canvasl.create_image((437.00, 11.00),
                                                                          image=self.close_button_results_leave)
        self.canvasl.tag_bind(self.close_button_results_leave_label, "<Enter>", self.on_enter_close)

    def on_enter_min(self, event):
        self.min_button_hover = PhotoImage(file="includes/min_button_enter.gif")
        self.min_button_hover_label = self.canvasl.create_image((392.00, 11.00), image=self.min_button_hover)
        self.canvasl.tag_bind(self.min_button_hover_label, "<Button-1>", self.minim)
        self.canvasl.tag_bind(self.min_button_hover_label, "<Leave>", self.on_leave_min)

    def on_leave_min(self, event):
        self.min_button_leave = PhotoImage(file="includes/min_button_leave.gif")
        self.min_button_leave_label = self.canvasl.create_image((392.00, 11.00), image=self.min_button_leave)
        self.canvasl.tag_bind(self.min_button_leave_label, "<Enter>", self.on_enter_min)

    # ------- Setting Constants -------
    def __init__(self, z, a,z2,a2,z_string,z1_string,z2_string,a_string,a1_string,a2_string, q):
        self.z = z
        self.a = a
        self.z2 = z2
        self.a2 = a2
        self.q = q
        self.z1 = self.z - self.z2
        self.a1 = self.a - self.a2
        self.z_string = z_string
        self.z1_string = z1_string
        self.z2_string = z2_string
        self.a_string = a_string
        self.a1_string = a1_string
        self.a2_string = a2_string

    def cppm(self):

        # ------------ Constants -------------
        g = 0.9517 * (1 - 1.7826 * ((self.a - self.z * 2) ** 2) / (self.a ** 2))
        # print("g=", g)
        rp = 1.28 * (self.a ** (1 / 3)) - 0.760 + 0.8 * (self.a ** (-1 / 3))
        r1 = 1.28 * (self.a1 ** (1 / 3)) - 0.760 + 0.8 * (self.a1 ** (-1 / 3))
        r2 = 1.28 * (self.a2 ** (1 / 3)) - 0.760 + 0.8 * (self.a2 ** (-1 / 3))
        # print(rp, r1, r2)
        c1 = (r1 * r1 - 1) / r1
        c2 = (r2 * r2 - 1) / r2
        c = (rp * rp - 1) / rp
        rc = c1 + c2
        # print(c1, c2, c)
        vp_constant = 4 * 3.14 * 1 * g * ((c1 * c2) / (c1 + c2))
        vc_constant = self.z1 * self.z2 * 1.44
        e0 = 2 * (c - c1 - c2)
        D = self.z1 * self.z2 * 1.44
        v01 = ((-D) / (rc ** 2)) + (0.9270 * vp_constant)
        print(
        'vc constant =', vc_constant, 'rc=', rc, 'vp constant=', vp_constant, 'e0 = ', e0, 'v01 = ', v01, "D = ", D)
        i = 0
        d = 0
        d_a = []
        v_curve = []
        v = []
        v_root = []
        while d <= 100:
            # for z in range(-5.00,100.00):
            # --------------------r is the total separation between nuclei anytime
            d_a.append(d)
            r = c1 + c2 + d
            o = 0.000
            if (d >= 0.000) and (d < 1.947):
                o = -1.7817 + 0.9270 * d + 0.01696 * (d ** 2.0) - 0.05148 * (d ** 3.0)
            elif (d >= 1.94750) and (d < 6.0):
                o = -4.41 * math.exp(- d / 0.7176)
            if (i == 0):
                v0 = (vc_constant / r) + (vp_constant * o) - self.q
                print("v0=", v0, "z =", d)
            v.append((vc_constant / r) + (vp_constant * o))
            v_curve.append(v[i] - self.q)
            if ((v[i] - self.q) < 0.0):
                v_root.append(0)
            else:
                v_root.append((v[i] - self.q) ** 0.5)
            i = i + 1
            d = d + 1
        print("d=", d)
        print("length of v array = ", len(v_root))
        # print("length of v_root  array = ", len(v_root))
        # print("Final Element of v_root=", v_root[10499])
        # -------------------- integration ---------------
        s = 0.0
        x = 1
        while x < 98:
            t = x + 1
            s = s + 2.0 * v_root[t] + 4.0 * v_root[(t + 1)]
            x = x + 2
        integral = ((s + v_root[0] + v_root[100] + 4.0 * v_root[1]) * 1 / 3.0) + (v0 ** 0.5) / (
                    (-1 / e0) + 0.5 * (v01 / v0))
        # print("Value integration = ", integral)
        # ---------- Final Calculations
        # -------- h Plancks constant in eVs
        h = 4.135 * 10.0 ** (-15)
        # print("h= ", h)
        # -------- Gamow's factor -0.721 constant obtained by substituting all other values
        gc = (((self.a1 * self.a2) / self.a) ** 0.5) * (0.218745)
        # print("gc = ", gc)
        # print("integral = ", integral)

        GF = gc * integral
        print("GF= ", GF)
        # -------- Barrier penetrability ---------
        P = (math.exp(-GF)) ** 2.0
        print("P= ", P)
        # -------- Empirical Zero point energy ---
        Ev = self.q * (0.056 + 0.039 * math.exp((4 - self.a2) / 2.5)) * 10.0 ** (6.0)
        print("Ev= ", Ev)
        # -------- Freaquency --------------------
        freq = (2.0 * Ev) / h
        print("freq= ", freq)
        # -------- Half life time ----------------
        T_half = 0.6931 / (freq * P)
        print("T_half= ", T_half)
        # -------- Log T half --------------------
        log_T_half = round(math.log10(T_half), 3)  # /365 * 24 * 60 * 60),3)
        print("log_T_half= ", log_T_half)
        cppm_s = str(log_T_half)
        # -------- Returns Results ---------------
        return cppm_s

    # ----- Result Window -------
    def result_window(self):
        self.r_window = Toplevel()
        self.result_bg = PhotoImage(file="includes/result_bg.gif")
        self.w = self.result_bg.width()
        self.h = self.result_bg.height()
        self.canvasl = Canvas(self.r_window, height=self.h, width=self.w, bd=-1.5)
        self.bgl_label = self.canvasl.create_image((0, 0), image=self.result_bg, anchor=N + W)
        self.canvasl.pack()
        self.canvasl.bind("<Map>", self.frame_mapped)
        # -------------------Button ----------
        # -------- Title Bar ---------
        self.title_bar = self.canvasl.create_rectangle(0, 0, self.w - 65, 100, width=30, fill="", outline="")
        self.canvasl.tag_bind(self.title_bar, "<B1-Motion>", self.move_window_results)
        # -------- Close Button ------
        self.close_button_results_leave = PhotoImage(file="includes/close_button_leave.gif")
        self.close_button_results_leave_label = self.canvasl.create_image((437.00, 11.00),
                                                                          image=self.close_button_results_leave)
        self.canvasl.tag_bind(self.close_button_results_leave_label, "<Button-1>", self.close)
        self.canvasl.tag_bind(self.close_button_results_leave_label, "<Enter>", self.on_enter_close)
        # --------------- Custom minimise Button --------
        self.min_button = PhotoImage(file="includes/min_button_leave.gif")
        self.min_button_label = self.canvasl.create_image((392.000, 11.00), image=self.min_button)
        self.canvasl.tag_bind(self.min_button_label, "<Button-1>", self.minim)
        self.canvasl.tag_bind(self.min_button_label, "<Enter>", self.on_enter_min)
        # ------------ Font Style ---------------
        label_font_input = font.Font(family='Calibri Regular', size=12,weight="bold")
        label_font_output = font.Font(family='Calibri Regular', size=14)
        # ----------- Results Labels ------------
        self.canvasl.create_text((78.0, 120.00), font=label_font_input, text="Z = "+self.z_string, fill="white")
        self.canvasl.create_text((78.0, 140.0), font=label_font_input, text="A = "+self.a_string, fill="white")
        self.canvasl.create_text((269.0, 120.00), font=label_font_input, text="Z = "+self.z2_string, fill="black")
        self.canvasl.create_text((269.0, 140.0), font=label_font_input, text="A = "+self.a2_string, fill="black")
        self.canvasl.create_text((407.0, 115.00), font=label_font_input, text="Z = "+self.z1_string, fill="white")
        self.canvasl.create_text((407.0, 140.0), font=label_font_input, text="A = "+self.a1_string, fill="white")
        self.canvasl.create_text((319.5, 212.50), font=label_font_output, text=self.cppm(), fill="gray10")
        # ----------- Centering ------------------
        self.r_window.update_idletasks()
        self.x = (self.r_window.winfo_screenwidth() // 2) - (self.w // 2)
        self.y = (self.r_window.winfo_screenheight() // 2) - (self.h // 2)
        self.r_window.geometry('{}x{}+{}+{}'.format(self.w, self.h, self.x, self.y))
        # ----------- Disabling Title Bar and Resize Option
        self.r_window.wm_overrideredirect(True)
        self.r_window.resizable(False, False)
        self.r_window.mainloop()


# ------------------- Main Window -----------------
class App(Tk):
    # --------- Move Window ---------
    def minim(self, event):
        self.overrideredirect(False)
        self.wm_state("iconic")

    def frame_mapped(self, event):
        self.update_idletasks()
        self.overrideredirect(True)
        self.state('normal')

    def startMove(self, event):
        self.x = event.x
        self.y = event.y

    def stopMove(self, event):
        self.x = None
        self.y = None

    def move_window(self, event):
        self.geometry('+{0}+{1}'.format(event.x_root, event.y_root))

    # --------- Close Window --------
    def close(self, event):
        self.destroy()

    # --------- Hovering Effects to Buttons ----
    def on_enter_close(self, event):
        self.close_button_hover = PhotoImage(file="includes/close_button_enter.gif")
        self.close_button_hover_label = self.canvasl.create_image((437.00, 11.00), image=self.close_button_hover)
        self.canvasl.tag_bind(self.close_button_hover_label, "<Button-1>", self.close)
        self.canvasl.tag_bind(self.close_button_hover_label, "<Leave>", self.on_leave_close)

    def on_enter_results(self, event):
        self.results_button_hover = PhotoImage(file="includes/result_button_enter.gif")
        self.results_button_hover_label = self.canvasl.create_image((235.50, 333.00), image=self.results_button_hover)
        self.canvasl.tag_bind(self.results_button_hover_label, "<Button-1>", self.result)
        self.canvasl.tag_bind(self.results_button_hover_label, "<Leave>", self.on_leave_results)

    def on_leave_close(self, event):
        self.close_button_leave = PhotoImage(file="includes/close_button_leave.gif")
        self.close_button_leave_label = self.canvasl.create_image((437.00, 11.00), image=self.close_button_leave)
        self.canvasl.tag_bind(self.close_button_leave_label, "<Enter>", self.on_enter_close)

    def on_leave_results(self, event):
        self.results_button_hover_leave = PhotoImage(file="includes/result_button_leave.gif")
        self.results_button_hover_leave_label = self.canvasl.create_image((235.0, 333.00),
                                                                          image=self.results_button_hover_leave)
        self.canvasl.tag_bind(self.results_button_hover_leave_label, "<Enter>", self.on_enter_results)

    def on_enter_min(self, event):
        self.min_button_hover = PhotoImage(file="includes/min_button_enter.gif")
        self.min_button_hover_label = self.canvasl.create_image((392.00, 11.00), image=self.min_button_hover)
        self.canvasl.tag_bind(self.min_button_hover_label, "<Button-1>", self.minim)
        self.canvasl.tag_bind(self.min_button_hover_label, "<Leave>", self.on_leave_min)

    def on_leave_min(self, event):
        self.min_button_leave = PhotoImage(file="includes/min_button_leave.gif")
        self.min_button_leave_label = self.canvasl.create_image((392.00, 11.00), image=self.min_button_leave)
        self.canvasl.tag_bind(self.min_button_leave_label, "<Enter>", self.on_enter_min)

    # ------ Rsults -----------
    def result(self, event):
        # ------------Getting inputs
        self.z = int(self.z_entry.get())
        self.z_string = str(self.z_entry.get())
        self.a = int(self.a_entry.get())
        self.a_string = str(self.a_entry.get())
        self.z2 = int(self.z2_entry.get())
        self.z2_string=str(self.z2_entry.get())
        self.a2 = int(self.a2_entry.get())
        self.a2_string = str(self.a2_entry.get())
        self.z1_string = str(self.z-self.z2)
        self.a1_string = str(self.a-self.a2)
        self.q = float(self.q_string.get())
        results = Results(self.z, self.a,self.z2, self.a2,self.z_string,self.z1_string,self.z2_string,self.a_string,self.a1_string,self.a2_string, self.q)
        results.result_window()

    # results.cppm()
    # results.xu()
    # results.kps()

    # ------- Initialisation --------
    def __init__(self):
        Tk.__init__(self)
        self.withdraw()
        splash = Splash(self)
        ## setup stuff goes here
        time.sleep(3)
        ## finished loading so destroy splash
        splash.destroy()
        ## show window again
        self.deiconify()
        # ---------- App window settings
        self.overrideredirect(1)
        self.resizable(False, False)
        self.app_bg = PhotoImage(file="includes/app_bg.gif")
        self.w = self.app_bg.width()
        self.h = self.app_bg.height()
        self.canvasl = Canvas(self, height=self.h, width=self.w, bd=-1.5)
        self.bgl_label = self.canvasl.create_image((0, 0), image=self.app_bg, anchor=N + W)
        self.canvasl.pack()
        self.canvasl.bind("<Map>", self.frame_mapped)
        # ---------- Entry Areas
        # ---- Parent Atomic Number ----
        self.z_entry = Entry(self.canvasl, width=5, bd=0, relief=RIDGE)
        self.z_entry.insert(0, "0")
        # ---- Parent Mass Number ------
        self.a_entry = Entry(self.canvasl, width=5, bd=0, relief=RIDGE)
        self.a_entry.insert(0, "0")
        # ---- Emitted Atomic Number ----
        self.z2_entry = Entry(self.canvasl, width=5, bd=0, relief=RIDGE)
        self.z2_entry.insert(0, "0")
        # ---- Emitted Mass Number ------
        self.a2_entry = Entry(self.canvasl, width=5, bd=0, relief=RIDGE)
        self.a2_entry.insert(0, "0")
        # ---- Q Value ----------
        self.q_string = Entry(self.canvasl, width=5, bd=0, relief=RIDGE)
        self.q_string.insert(0, "0")
        # ---- Entry Windows ----
        self.canvasl.create_window((163.5, 195.0), window=self.z_entry)
        self.canvasl.create_window((163.50, 228.0), window=self.a_entry)
        self.canvasl.create_window((384.5, 195.0), window=self.z2_entry)
        self.canvasl.create_window((384.5, 228.0), window=self.a2_entry)
        self.canvasl.create_window((262.50, 269.0), window=self.q_string)
        # ---------Button Images
        # --------------- Custom Title Bar -----------
        self.title_bar = self.canvasl.create_rectangle(0, 0, self.w - 20, 150, width=30, fill="", outline="")
        self.canvasl.tag_bind(self.title_bar, "<B1-Motion>", self.move_window)
        # --------------- Results Button -------------
        self.results_button = PhotoImage(file="includes/result_button_leave.gif")
        self.results_button_label = self.canvasl.create_image((235.0, 333.00), image=self.results_button)
        self.canvasl.tag_bind(self.results_button_label, "<Button-1>", self.result)
        self.canvasl.tag_bind(self.results_button_label, "<Enter>", self.on_enter_results)
        # --------------- Custom Close Button --------
        self.close_button = PhotoImage(file="includes/close_button_leave.gif")
        self.close_button_label = self.canvasl.create_image((437.00, 11.00), image=self.close_button)
        self.canvasl.tag_bind(self.close_button_label, "<Button-1>", self.close)
        self.canvasl.tag_bind(self.close_button_label, "<Enter>", self.on_enter_close)
        # --------------- Custom minimise Button --------
        self.min_button = PhotoImage(file="includes/min_button_leave.gif")
        self.min_button_label = self.canvasl.create_image((392.000, 11.00), image=self.min_button)
        self.canvasl.tag_bind(self.min_button_label, "<Button-1>", self.minim)
        self.canvasl.tag_bind(self.min_button_label, "<Enter>", self.on_enter_min)
        # --------------- Removing Title Bar And Disabling Resizing --
        self.overrideredirect(1)
        self.resizable(False, False)
        # --------- Window Center Align--------------
        self.update_idletasks()
        self.x = (self.winfo_screenwidth() // 2) - (self.w // 2)
        self.y = (self.winfo_screenheight() // 2) - (self.h // 2)
        self.geometry('{}x{}+{}+{}'.format(self.w, self.h, self.x, self.y))
        # -------- required to make window show before the program gets to the mainloop
        self.update()


# ------------------- Entry -----------------------
if __name__ == "__main__":
    app = App()
    app.mainloop()
