############################################# IMPORTING ################################################
import tkinter as tk
from tkinter import ttk, filedialog
from tkinter import messagebox as mess
import tkinter.simpledialog as tsd
import cv2, os, csv
import numpy as np
from PIL import Image
import pandas as pd
import datetime, time

# optional audio on Windows; will be ignored on other platforms
try:
    import winsound
except Exception:
    winsound = None

############################################# FUNCTIONS ################################################

def assure_path_exists(path):
    directory = os.path.dirname(path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)

def tick():
    # update clock label
    try:
        clock.config(text=time.strftime('%H:%M:%S'))
        clock.after(1000, tick)
    except Exception:
        pass

def contact():
    mess.showinfo('Contact Us', "Please contact us on: xxxxxxxxxxxxx@gmail.com")

def check_haarcascadefile():
    if not os.path.isfile("haarcascade_frontalface_default.xml"):
        mess.showerror("Missing File", "Haarcascade file missing! Please contact support.")
        try:
            window.destroy()
        except:
            pass

def save_pass():
    assure_path_exists("TrainingImageLabel/")
    exists1 = os.path.isfile("TrainingImageLabel/psd.txt")
    if exists1:
        with open("TrainingImageLabel/psd.txt", "r") as tf:
            key = tf.read()
    else:
        # if no existing password, prompt to set one
        try:
            master.destroy()
        except:
            pass
        new_pas = tsd.askstring('Password Setup', 'Enter a new password', show='*')
        if not new_pas:
            mess.showwarning('No Password', 'Password not set! Please try again')
            return
        with open("TrainingImageLabel/psd.txt", "w") as tf:
            tf.write(new_pas)
        mess.showinfo('Password Registered', 'New password registered successfully!')
        return

    op = old.get()
    newp = new.get()
    nnewp = nnew.get()
    if op == key:
        if newp == nnewp:
            with open("TrainingImageLabel/psd.txt", "w") as tf:
                tf.write(newp)
            mess.showinfo('Success', 'Password changed successfully!')
            try:
                master.destroy()
            except:
                pass
            return
        else:
            mess.showerror('Mismatch', 'Confirm your new password again!')
    else:
        mess.showerror('Wrong Password', 'Old password is incorrect!')

def change_pass():
    global master, old, new, nnew
    master = tk.Toplevel(window)
    master.geometry("500x350")
    master.title("Change Password")
    master.configure(bg="#1a1a2e")
    master.resizable(False, False)

    card = tk.Frame(master, bg='#16213e')
    card.place(x=50, y=50, width=400, height=250)

    tk.Label(card, text='🔐 Change Password', font=('Segoe UI', 18, 'bold'),
             bg='#16213e', fg='white').place(x=100, y=20)

    tk.Label(card, text='Current Password', bg='#16213e', fg='#a8a8a8').place(x=50, y=70)
    old = tk.Entry(card, show='*', bg="#0f3460", fg="white", relief='flat', insertbackground='white')
    old.place(x=50, y=95, width=300, height=28)

    tk.Label(card, text='New Password', bg='#16213e', fg='#a8a8a8').place(x=50, y=130)
    new = tk.Entry(card, show='*', bg="#0f3460", fg="white", relief='flat', insertbackground='white')
    new.place(x=50, y=150, width=140, height=28)

    tk.Label(card, text='Confirm', bg='#16213e', fg='#a8a8a8').place(x=220, y=130)
    nnew = tk.Entry(card, show='*', bg="#0f3460", fg="white", relief='flat', insertbackground='white')
    nnew.place(x=220, y=150, width=130, height=28)

    tk.Button(card, text="💾 Save", bg="#38a169", fg="white", relief='flat',
              command=save_pass).place(x=50, y=200, width=130, height=35)
    tk.Button(card, text="❌ Cancel", bg="#e53e3e", fg="white", relief='flat',
              command=master.destroy).place(x=220, y=200, width=130, height=35)

def psw():
    assure_path_exists("TrainingImageLabel/")
    exists1 = os.path.isfile("TrainingImageLabel/psd.txt")
    if exists1:
        with open("TrainingImageLabel/psd.txt", "r") as tf:
            key = tf.read()
    else:
        new_pas = tsd.askstring('Set Password', 'Enter new password', show='*')
        if new_pas:
            with open("TrainingImageLabel/psd.txt", "w") as tf:
                tf.write(new_pas)
            mess.showinfo('Saved', 'Password set successfully!')
            update_registration_count()
            return
        else:
            mess.showwarning('No Password', 'Password not set!')
            return

    password = tsd.askstring('Password', 'Enter password', show='*')
    if password == key:
        TrainImages()
        update_registration_count()
    elif password:
        mess.showerror('Wrong', 'Incorrect password!')

def clear():
    txt.delete(0, 'end')
    message1.config(text="Ready to capture images...")

def clear2():
    txt2.delete(0, 'end')
    message1.config(text="Ready to capture images...")

def TakeImages():
    # keep original logic but call check and update UI
    check_haarcascadefile()
    columns = ['SERIAL NO.', '', 'ID', '', 'NAME']
    assure_path_exists("StudentDetails/")
    assure_path_exists("TrainingImage/")

    serial = 0
    if os.path.isfile("StudentDetails/StudentDetails.csv"):
        with open("StudentDetails/StudentDetails.csv", 'r') as f:
            serial = sum(1 for _ in f) // 2
    else:
        with open("StudentDetails/StudentDetails.csv", 'a+', newline='') as f:
            csv.writer(f).writerow(columns)
        serial = 1

    Id, name = txt.get(), txt2.get()
    if name.replace(" ", "").isalpha():
        cam = cv2.VideoCapture(0)
        detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        sampleNum = 0
        while True:
            ret, img = cam.read()
            if not ret:
                break
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 255), 2)
                sampleNum += 1
                cv2.imwrite(f"TrainingImage/{name}.{serial}.{Id}.{sampleNum}.jpg",
                            gray[y:y + h, x:x + w])
                cv2.imshow('Taking Images', img)
            if (cv2.waitKey(100) & 0xFF == ord('q')) or sampleNum > 50:
                break
        cam.release()
        cv2.destroyAllWindows()
        with open('StudentDetails/StudentDetails.csv', 'a+', newline='') as f:
            csv.writer(f).writerow([serial, '', Id, '', name])
        message1.config(text=f"✅ Images captured for ID: {Id}")
        update_registration_count()
    else:
        message1.config(text="❌ Enter a valid name")

def TrainImages():
    # unchanged logic, but update UI & count afterwards
    check_haarcascadefile()
    assure_path_exists("TrainingImageLabel/")
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    faces, Ids = getImagesAndLabels("TrainingImage")
    if not faces:
        mess.showwarning('No Data', 'Please register someone first!')
        return
    recognizer.train(faces, np.array(Ids))
    recognizer.save("TrainingImageLabel/Trainner.yml")
    message1.config(text="✅ Profile saved successfully!")
    message.config(text=f"📊 Total Registrations: {len(set(Ids))}")
    update_registration_count()

def getImagesAndLabels(path):
    faces, Ids = [], []
    if not os.path.isdir(path):
        return faces, Ids
    for imagePath in [os.path.join(path, f) for f in os.listdir(path)]:
        try:
            img = Image.open(imagePath).convert('L')
            faces.append(np.array(img, 'uint8'))
            Ids.append(int(os.path.split(imagePath)[-1].split(".")[1]))
        except Exception:
            # skip unreadable files
            continue
    return faces, Ids

def TrackImages():
    # original logic preserved; added overlay status bar + optional beep
    check_haarcascadefile()
    assure_path_exists("Attendance/")
    for k in tv.get_children():
        tv.delete(k)

    if not os.path.isfile("TrainingImageLabel/Trainner.yml"):
        mess.showerror('Missing', 'Please save profile first!')
        return

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read("TrainingImageLabel/Trainner.yml")

    faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    cam = cv2.VideoCapture(0)
    if not cam.isOpened():
        mess.showerror('Camera', 'Cannot open camera!')
        return

    df_path = "StudentDetails/StudentDetails.csv"
    if not os.path.isfile(df_path):
        mess.showerror('Details Missing', 'Students details are missing, please check!')
        cam.release()
        return

    df = pd.read_csv(df_path)
    attendance = None

    try:
        while True:
            ret, im = cam.read()
            if not ret:
                break
            gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
            faces = faceCascade.detectMultiScale(gray, 1.2, 5)
            status_text = ""
            status_color = (0, 0, 0)  # BGR

            for (x, y, w, h) in faces:
                serial, conf = recognizer.predict(gray[y:y + h, x:x + w])
                if conf < 50:
                    ts = time.time()
                    date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
                    timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                    aa = df.loc[df['SERIAL NO.'] == serial]['NAME'].values
                    ID = df.loc[df['SERIAL NO.'] == serial]['ID'].values
                    ID = str(ID)
                    ID = ID[1:-1]
                    bb = str(aa)
                    bb = bb[2:-2]
                    attendance = [str(ID), '', bb, '', str(date), '', str(timeStamp)]

                    # overlay status bar: green
                    status_text = f"Recognized: {bb} (ID: {ID})"
                    status_color = (0, 128, 0)  # dark green BGR for rectangle
                    # put name near face (blue)
                    cv2.putText(im, bb, (x, y + h + 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
                    # optional beep for recognized
                    if winsound:
                        try:
                            winsound.Beep(1000, 120)
                        except:
                            pass
                else:
                    # unknown
                    status_text = "Unknown person detected"
                    status_color = (0, 0, 255)  # red
                    cv2.putText(im, "Unknown", (x, y + h + 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
                    if winsound:
                        try:
                            winsound.Beep(500, 220)
                        except:
                            pass

                # draw face rectangle (yellow)
                cv2.rectangle(im, (x, y), (x + w, y + h), (0,255,255), 2)

            # draw top status bar if we have faces detected (otherwise don't obscure)
            if faces is not None and len(faces) > 0:
                # fill a rectangle across top
                h_bar = 40
                cv2.rectangle(im, (0,0), (im.shape[1], h_bar), status_color, -1)
                # text in white
                cv2.putText(im, status_text, (10, 28), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 2)

            cv2.imshow("Attendance", im)
            if (cv2.waitKey(1) & 0xFF) == ord('q'):
                break
    except KeyboardInterrupt:
        # allow ctrl-c to stop gracefully
        pass
    finally:
        cam.release()
        cv2.destroyAllWindows()

    # save attendance (same logic as before)
    if attendance:
        date = attendance[4]
        fileName = f"Attendance/Attendance_{date}.csv"
        exists = os.path.isfile(fileName)
        with open(fileName, 'a+', newline='') as f:
            writer = csv.writer(f)
            if not exists:
                writer.writerow(['Id', '', 'Name', '', 'Date', '', 'Time'])
            writer.writerow(attendance)

        # populate treeview with saved attendance file
        try:
            with open(fileName, 'r') as f:
                for i, line in enumerate(csv.reader(f)):
                    if i > 0 and line:
                        tv.insert('', 'end', text=line[0], values=(line[2], line[4], line[6]))
        except Exception:
            pass

######################################## UI Helpers ############################################

def update_registration_count():
    # read student details CSV and compute registration count the same way original code did
    res = 0
    path = "StudentDetails/StudentDetails.csv"
    if os.path.isfile(path):
        try:
            with open(path, 'r') as csvFile1:
                reader1 = csv.reader(csvFile1)
                for l in reader1:
                    res = res + 1
            res = (res // 2) - 1
            if res < 0:
                res = 0
        except Exception:
            res = 0
    message.config(text=f'📊 Total Registrations: {res}')

def view_history():
    # open a window that lists Attendance CSV files and allows preview + export
    assure_path_exists("Attendance/")
    top = tk.Toplevel(window)
    top.title("Attendance History")
    top.geometry("900x600")
    top.configure(bg="#0f1724")

    files = []
    att_dir = "Attendance"
    if os.path.isdir(att_dir):
        for f in sorted(os.listdir(att_dir), reverse=True):
            if f.lower().endswith(".csv"):
                files.append(f)

    # left: listbox of files
    left_frame = tk.Frame(top, bg="#0f1724")
    left_frame.pack(side='left', fill='y', padx=10, pady=10)
    tk.Label(left_frame, text="Files", bg="#0f1724", fg="white", font=('Segoe UI', 12, 'bold')).pack(anchor='nw')
    listbox = tk.Listbox(left_frame, width=40, height=30, bg="#0b1220", fg="white", selectbackground="#0f6d3b")
    listbox.pack(pady=(6,0))
    for f in files:
        listbox.insert('end', f)

    # right: treeview preview + buttons
    right_frame = tk.Frame(top, bg="#0f1724")
    right_frame.pack(side='right', fill='both', expand=True, padx=10, pady=10)
    tvf = ttk.Treeview(right_frame, columns=("name","date","time"), show="tree headings")
    tvf.heading("#0", text="ID")
    tvf.heading("name", text="Name")
    tvf.heading("date", text="Date")
    tvf.heading("time", text="Time")
    tvf.pack(fill='both', expand=True)

    def load_selected_file():
        sel = listbox.curselection()
        if not sel:
            mess.showwarning("Select file", "Please select a file from the list")
            return
        fname = listbox.get(sel[0])
        full = os.path.join(att_dir, fname)
        tvf.delete(*tvf.get_children())
        try:
            with open(full, 'r') as f:
                for i, line in enumerate(csv.reader(f)):
                    if i == 0:
                        continue
                    if line:
                        tvf.insert('', 'end', text=line[0], values=(line[2], line[4], line[6]))
        except Exception as e:
            mess.showerror("Error", f"Could not read file: {e}")

    def export_selected_file():
        sel = listbox.curselection()
        if not sel:
            mess.showwarning("Select file", "Please select a file to export")
            return
        fname = listbox.get(sel[0])
        full = os.path.join(att_dir, fname)
        try:
            df = pd.read_csv(full)
            out = filedialog.asksaveasfilename(defaultextension=".xlsx",
                                               filetypes=[("Excel files", "*.xlsx")],
                                               initialfile=fname.replace(".csv", ".xlsx"))
            if out:
                df.to_excel(out, index=False)
                mess.showinfo("Exported", f"Exported to {out}")
        except Exception as e:
            mess.showerror("Export Error", f"Could not export: {e}")

    btn_frame = tk.Frame(right_frame, bg="#0f1724")
    btn_frame.pack(fill='x', pady=(6,0))
    tk.Button(btn_frame, text="Load File", command=load_selected_file, bg="#3b82f6", fg="white").pack(side='left', padx=6)
    tk.Button(btn_frame, text="Export to Excel", command=export_selected_file, bg="#10b981", fg="white").pack(side='left', padx=6)
    tk.Button(btn_frame, text="Close", command=top.destroy, bg="#6b7280", fg="white").pack(side='right', padx=6)

def toggle_fullscreen():
    # toggle attribute fullscreen
    cur = window.attributes("-fullscreen")
    window.attributes("-fullscreen", not cur)

############################################ GUI ################################################
window = tk.Tk()
window.title("Face Recognition Attendance System")
window.configure(bg="#0f0f23")

# Start maximized to fill screen area (keeps taskbar visible)
try:
    window.state("zoomed")
except Exception:
    # fallback: set geometry to screen size
    screen_w = window.winfo_screenwidth()
    screen_h = window.winfo_screenheight()
    window.geometry(f"{screen_w}x{screen_h}")

window.resizable(True, True)

# ===== Header =====
header = tk.Frame(window, bg="#1a1a2e", height=120)
header.pack(fill="x")
tk.Label(header, text="🎓 Face Recognition Attendance",
         font=('Segoe UI', 26, 'bold'), bg="#1a1a2e", fg="white").place(x=30, y=30)
clock = tk.Label(header, font=('Segoe UI', 16), bg="#1a1a2e", fg="#10b981")
clock.place(relx=0.85, rely=0.3)
tick()

# ===== Body =====
body = tk.Frame(window, bg="#0f0f23")
body.pack(fill="both", expand=True, padx=20, pady=20)
body.columnconfigure(0, weight=1)
body.columnconfigure(1, weight=1)

# --- Left: Attendance ---
left = tk.Frame(body, bg="#1a1a2e", bd=1, relief='flat', highlightthickness=1, highlightbackground="#0f3460")
left.grid(row=0, column=0, sticky="nsew", padx=(0,10))
tk.Label(left, text="📊 Attendance", bg="#3b82f6", fg="white",
         font=('Segoe UI', 16, 'bold')).pack(fill="x")

tk.Button(left, text="🎥 Start Attendance Capture", command=TrackImages,
          bg="#10b981", fg="white", font=('Segoe UI', 12, 'bold'),
          relief='flat', height=2).pack(fill="x", padx=20, pady=12)

tk.Button(left, text="📄 View Attendance History", command=view_history,
          bg="#3b82f6", fg="white", font=('Segoe UI', 12, 'bold'),
          relief='flat', height=2).pack(fill="x", padx=20, pady=(0,12))

tree_frame = tk.Frame(left, bg="#1a1a2e")
tree_frame.pack(fill="both", expand=True, padx=20, pady=(0,20))

style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview",
                background="#16213e", foreground="white", rowheight=28,
                fieldbackground="#16213e", font=('Segoe UI', 10))
style.configure("Treeview.Heading", background="#3b82f6", foreground="white", font=('Segoe UI', 11, 'bold'))

tv = ttk.Treeview(tree_frame, columns=("name","date","time"), show="tree headings")
tv.heading("#0", text="ID"); tv.heading("name", text="Name")
tv.heading("date", text="Date"); tv.heading("time", text="Time")
tv.column("#0", width=100, anchor='center')
tv.pack(fill="both", expand=True, side="left")

scroll = ttk.Scrollbar(tree_frame, orient="vertical", command=tv.yview)
scroll.pack(side="right", fill="y")
tv.configure(yscrollcommand=scroll.set)

# --- Right: Registration ---
right = tk.Frame(body, bg="#1a1a2e", bd=1, relief='flat', highlightthickness=1, highlightbackground="#0f3460")
right.grid(row=0, column=1, sticky="nsew", padx=(10,0))
tk.Label(right, text="➕ Student Registration", bg="#8b5cf6", fg="white",
         font=('Segoe UI', 16, 'bold')).pack(fill="x")

form = tk.Frame(right, bg="#1a1a2e")
form.pack(fill="both", expand=True, padx=30, pady=30)

tk.Label(form, text="🎯 Student ID", fg="white", bg="#1a1a2e", font=('Segoe UI', 12, 'bold')).pack(anchor="w")
txt = tk.Entry(form, bg="#16213e", fg="white", insertbackground='white', relief='flat', font=('Segoe UI', 12))
txt.pack(fill="x", pady=(0,15))

tk.Label(form, text="👤 Student Name", fg="white", bg="#1a1a2e", font=('Segoe UI', 12, 'bold')).pack(anchor="w")
txt2 = tk.Entry(form, bg="#16213e", fg="white", insertbackground='white', relief='flat', font=('Segoe UI', 12))
txt2.pack(fill="x", pady=(0,15))

tk.Button(form, text="📸 Capture Images", command=TakeImages,
          bg="#8b5cf6", fg="white", relief='flat', font=('Segoe UI', 12, 'bold')).pack(fill="x", pady=(0,10))
tk.Button(form, text="💾 Save Profile", command=psw,
          bg="#10b981", fg="white", relief='flat', font=('Segoe UI', 12, 'bold')).pack(fill="x")

# Clear fields button
tk.Button(form, text="♻️ Clear Fields", command=lambda: (txt.delete(0,'end'), txt2.delete(0,'end'), message1.config(text="Ready to capture images...")),
          bg="#6b7280", fg="white", relief='flat', font=('Segoe UI', 12)).pack(fill="x", pady=(10,0))

message1 = tk.Label(form, text="Ready to capture images...", bg="#1a1a2e", fg="#64748b",
                    font=('Segoe UI', 11, 'italic'))
message1.pack(fill="x", pady=(20,0))

# Total registrations
count_frame = tk.Frame(right, bg="#1a1a2e")
count_frame.pack(fill="x", pady=(10,20))
reg_count = 0
if os.path.isfile("StudentDetails/StudentDetails.csv"):
    try:
        with open("StudentDetails/StudentDetails.csv") as f:
            reg_count = max(sum(1 for _ in f)//2 - 1,0)
    except Exception:
        reg_count = 0
message = tk.Label(count_frame, text=f"📊 Total Registrations: {reg_count}",
                   fg="#10b981", bg="#1a1a2e", font=('Segoe UI', 12, 'bold'))
message.pack(anchor="w")

# ===== Bottom =====
bottom = tk.Frame(window, bg="#1a1a2e", height=50)
bottom.pack(fill="x", pady=(5,10))
tk.Label(bottom, text="🤖 AI-Powered Attendance System v2.0",
         bg="#1a1a2e", fg="#64748b").place(x=20, y=15)
tk.Button(bottom, text="🚪 Exit", command=window.destroy,
          bg="#6b7280", fg="white", relief='flat').place(relx=0.9, y=8, width=100, height=35)

# ===== Menu =====
menubar = tk.Menu(window, bg="#1a1a2e", fg="white")
filemenu = tk.Menu(menubar, tearoff=0, bg="#1a1a2e", fg="white")
filemenu.add_command(label="🔐 Change Password", command=change_pass)
filemenu.add_command(label="📞 Contact Us", command=contact)
filemenu.add_command(label="🖥️ Toggle Fullscreen", command=toggle_fullscreen)
filemenu.add_separator()
filemenu.add_command(label="🚪 Exit", command=window.destroy)
menubar.add_cascade(label="⚙️ Settings", menu=filemenu)
window.config(menu=menubar)

# ==============================
# Start the main event loop
# ==============================
update_registration_count()
window.mainloop()
