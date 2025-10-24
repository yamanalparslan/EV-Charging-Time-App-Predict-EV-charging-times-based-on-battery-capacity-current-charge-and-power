import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
import json
import os

class EVChargingCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("⚡ EV Şarj Süresi Hesaplayıcı")
        self.root.geometry("1000x850")
        self.root.configure(bg="#1a1a2e")
        self.root.resizable(True, True)
        self.root.minsize(900, 700)
        
        # Değişkenler
        self.battery_capacity = tk.DoubleVar(value=75.0)
        self.current_charge = tk.DoubleVar(value=20.0)
        self.charging_speed = tk.StringVar(value="50.0")
        
        # Özel araçlar listesi
        self.custom_vehicles = self.load_custom_vehicles()
        
        # Notebook (Tab sistemi)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True)
        
        # Stil ayarları
        style = ttk.Style()
        style.theme_use('default')
        style.configure('TNotebook', background='#1a1a2e', borderwidth=0)
        style.configure('TNotebook.Tab', 
                       background='#16213e', 
                       foreground='white',
                       padding=[20, 10],
                       font=('Helvetica', 11, 'bold'))
        style.map('TNotebook.Tab',
                 background=[('selected', '#0f3460')],
                 foreground=[('selected', 'white')])
        
        # Tab 1: Ana Hesaplama
        self.main_frame = tk.Frame(self.notebook, bg="#1a1a2e")
        self.notebook.add(self.main_frame, text="🔋 Şarj Hesaplama")
        
        # Tab 2: Araç Yönetimi
        self.vehicle_frame = tk.Frame(self.notebook, bg="#1a1a2e")
        self.notebook.add(self.vehicle_frame, text="🚗 Araç Yönetimi")
        
        self.create_main_widgets()
        self.create_vehicle_management_widgets()
        self.update_display()
        
    def load_custom_vehicles(self):
        """Kaydedilmiş araçları yükle"""
        try:
            if os.path.exists('custom_vehicles.json'):
                with open('custom_vehicles.json', 'r', encoding='utf-8') as f:
                    return json.load(f)
        except:
            pass
        return []
    
    def save_custom_vehicles(self):
        """Araçları kaydet"""
        try:
            with open('custom_vehicles.json', 'w', encoding='utf-8') as f:
                json.dump(self.custom_vehicles, f, ensure_ascii=False, indent=2)
        except Exception as e:
            messagebox.showerror("Hata", f"Kaydetme hatası: {str(e)}")
    
    def create_main_widgets(self):
        # Başlık Frame
        header_frame = tk.Frame(self.main_frame, bg="#0f3460", height=80)
        header_frame.pack(fill="x", padx=0, pady=0)
        
        title_label = tk.Label(
            header_frame,
            text="⚡ EV Şarj Süresi Hesaplayıcı",
            font=("Helvetica", 24, "bold"),
            bg="#0f3460",
            fg="white"
        )
        title_label.pack(pady=15)
        
        # Ana Container
        main_container = tk.Frame(self.main_frame, bg="#1a1a2e")
        main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Sol Panel - Batarya Göstergesi
        left_panel = tk.Frame(main_container, bg="#16213e", relief="raised", bd=2)
        left_panel.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        # Batarya Gösterge Başlık
        battery_title = tk.Label(
            left_panel,
            text="🔋 BATARYA DURUMU",
            font=("Helvetica", 16, "bold"),
            bg="#16213e",
            fg="white"
        )
        battery_title.pack(pady=15)
        
        # Batarya Canvas
        self.battery_canvas = tk.Canvas(
            left_panel,
            width=300,
            height=150,
            bg="#16213e",
            highlightthickness=0
        )
        self.battery_canvas.pack(pady=10)
        
        # Yüzde Gösterge
        self.percentage_label = tk.Label(
            left_panel,
            text="0.0%",
            font=("Helvetica", 48, "bold"),
            bg="#16213e",
            fg="#4ecca3"
        )
        self.percentage_label.pack(pady=10)
        
        # Enerji Bilgisi
        self.energy_label = tk.Label(
            left_panel,
            text="0.0 / 75.0 kWh",
            font=("Helvetica", 14),
            bg="#16213e",
            fg="#a8dadc"
        )
        self.energy_label.pack(pady=5)
        
        # Eksik Enerji
        self.remaining_label = tk.Label(
            left_panel,
            text="Eksik: 0.0 kWh",
            font=("Helvetica", 12),
            bg="#16213e",
            fg="#ffd93d"
        )
        self.remaining_label.pack(pady=5)
        
        # Süre Göstergesi
        time_frame = tk.Frame(left_panel, bg="#0f3460", relief="solid", bd=2)
        time_frame.pack(fill="x", padx=20, pady=20)
        
        time_title = tk.Label(
            time_frame,
            text="⏱️ TAM ŞARJ SÜRESİ",
            font=("Helvetica", 12, "bold"),
            bg="#0f3460",
            fg="white"
        )
        time_title.pack(pady=10)
        
        self.time_label = tk.Label(
            time_frame,
            text="0 saat 0 dakika",
            font=("Helvetica", 20, "bold"),
            bg="#0f3460",
            fg="#4ecca3"
        )
        self.time_label.pack(pady=10)
        
        self.finish_time_label = tk.Label(
            time_frame,
            text="Bitiş: --:--",
            font=("Helvetica", 11),
            bg="#0f3460",
            fg="#a8dadc"
        )
        self.finish_time_label.pack(pady=(0, 10))
        
        # Sağ Panel - Kontroller
        right_panel = tk.Frame(main_container, bg="#16213e", relief="raised", bd=2)
        right_panel.pack(side="right", fill="both", expand=True, padx=(10, 0))
        
        controls_title = tk.Label(
            right_panel,
            text="⚙️ AYARLAR",
            font=("Helvetica", 16, "bold"),
            bg="#16213e",
            fg="white"
        )
        controls_title.pack(pady=15)
        
        # Batarya Kapasitesi
        self.create_slider_section(
            right_panel,
            "🔋 Batarya Kapasitesi (kWh)",
            self.battery_capacity,
            30, 150, 5,
            "#4ecca3"
        )
        
        # Mevcut Şarj
        self.create_slider_section(
            right_panel,
            "📊 Mevcut Şarj (kWh)",
            self.current_charge,
            0, 150, 1,
            "#ffd93d"
        )
        
        # Şarj Hızı - Manuel Giriş
        speed_frame = tk.Frame(right_panel, bg="#16213e")
        speed_frame.pack(fill="x", padx=20, pady=10)
        
        speed_label = tk.Label(
            speed_frame,
            text="⚡ Şarj Hızı (kW)",
            font=("Helvetica", 11, "bold"),
            bg="#16213e",
            fg="white",
            anchor="w"
        )
        speed_label.pack(fill="x")
        
        speed_input_frame = tk.Frame(speed_frame, bg="#0f3460", relief="solid", bd=2)
        speed_input_frame.pack(fill="x", pady=5)
        
        self.speed_entry = tk.Entry(
            speed_input_frame,
            textvariable=self.charging_speed,
            font=("Helvetica", 18, "bold"),
            bg="#0f3460",
            fg="#ff6b6b",
            justify="center",
            relief="flat",
            insertbackground="gray"
        )
        self.speed_entry.pack(fill="x", padx=10, pady=10)
        self.speed_entry.bind('<KeyRelease>', lambda e: self.update_display())
        
        # Hızlı şarj hızı butonları
        speed_buttons_frame = tk.Frame(speed_frame, bg="#16213e")
        speed_buttons_frame.pack(fill="x", pady=5)
        
        speeds = [
            ("3.7 kW\nEv", "3.7"),
            ("6.7 kW\nEv+", "6.7"),
            ("22 kW\nAC", "22"),
            ("50 kW\nDC", "50"),
            ("100 kW\nDC+", "100"),
            ("150 kW\nSüper", "150"),
        ]
        
        for i, (text, value) in enumerate(speeds):
            btn = tk.Button(
                speed_buttons_frame,
                text=text,
                command=lambda v=value: self.charging_speed.set(v) or self.update_display(),
                bg="#0f3460",
                fg="gray",
                font=("Helvetica", 8, "bold"),
                relief="raised",
                bd=1,
                cursor="hand2",
                activebackground="#1a508b",
                activeforeground="white",
                padx=5,
                pady=5
            )
            btn.grid(row=i//3, column=i%3, padx=2, pady=2, sticky="ew")
        
        for i in range(3):
            speed_buttons_frame.grid_columnconfigure(i, weight=1)
        
        # Hızlı Seçim Başlık
        quick_title = tk.Label(
            right_panel,
            text="🚗 Popüler Modeller",
            font=("Helvetica", 12, "bold"),
            bg="#16213e",
            fg="gray"
        )
        quick_title.pack(pady=(20, 10))
        
        # Scrollable frame için canvas
        canvas_frame = tk.Frame(right_panel, bg="#16213e")
        canvas_frame.pack(fill="both", expand=True, padx=20, pady=(0, 10))
        
        canvas = tk.Canvas(canvas_frame, bg="#16213e", highlightthickness=0, height=200)
        scrollbar = tk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
        self.button_frame = tk.Frame(canvas, bg="#16213e")
        
        self.button_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.button_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        self.refresh_vehicle_buttons()
        
        # Maliyet Bilgisi
        cost_frame = tk.Frame(right_panel, bg="#0f3460", relief="solid", bd=2)
        cost_frame.pack(fill="x", padx=20, pady=(10, 20))
        
        cost_title = tk.Label(
            cost_frame,
            text="💰 MALİYET TAHMİNİ",
            font=("Helvetica", 11, "bold"),
            bg="#0f3460",
            fg="white"
        )
        cost_title.pack(pady=8)
        
        self.cost_label = tk.Label(
            cost_frame,
            text="0.00 TL",
            font=("Helvetica", 18, "bold"),
            bg="#0f3460",
            fg="#ffd93d"
        )
        self.cost_label.pack(pady=5)
        
        cost_info = tk.Label(
            cost_frame,
            text="(2.50 TL/kWh)",
            font=("Helvetica", 9),
            bg="#0f3460",
            fg="#a8dadc"
        )
        cost_info.pack(pady=(0, 8))
    
    def create_vehicle_management_widgets(self):
        """Araç yönetimi sayfası"""
        # Başlık
        header = tk.Frame(self.vehicle_frame, bg="#0f3460")
        header.pack(fill="x", pady=0)
        
        title = tk.Label(
            header,
            text="🚗 Araç Yönetimi",
            font=("Helvetica", 24, "bold"),
            bg="#0f3460",
            fg="white"
        )
        title.pack(pady=20)
        
        # Ana container
        container = tk.Frame(self.vehicle_frame, bg="#1a1a2e")
        container.pack(fill="both", expand=True, padx=30, pady=30)
        
        # Sol panel - Yeni araç ekleme
        left = tk.Frame(container, bg="#16213e", relief="raised", bd=2)
        left.pack(side="left", fill="both", expand=True, padx=(0, 15))
        
        add_title = tk.Label(
            left,
            text="➕ Yeni Araç Ekle",
            font=("Helvetica", 16, "bold"),
            bg="#16213e",
            fg="white"
        )
        add_title.pack(pady=20)
        
        # Form alanları
        form_frame = tk.Frame(left, bg="#16213e")
        form_frame.pack(fill="x", padx=30, pady=10)
        
        # Araç Adı
        tk.Label(
            form_frame,
            text="Araç Adı:",
            font=("Helvetica", 11, "bold"),
            bg="#16213e",
            fg="white",
            anchor="w"
        ).pack(fill="x", pady=(10, 5))
        
        self.vehicle_name_entry = tk.Entry(
            form_frame,
            font=("Helvetica", 12),
            bg="#0f3460",
            fg="white",
            relief="flat",
            insertbackground="white"
        )
        self.vehicle_name_entry.pack(fill="x", ipady=8, pady=5)
        
        # Batarya Kapasitesi
        tk.Label(
            form_frame,
            text="Batarya Kapasitesi (kWh):",
            font=("Helvetica", 11, "bold"),
            bg="#16213e",
            fg="white",
            anchor="w"
        ).pack(fill="x", pady=(15, 5))
        
        self.vehicle_capacity_entry = tk.Entry(
            form_frame,
            font=("Helvetica", 12),
            bg="#0f3460",
            fg="white",
            relief="flat",
            insertbackground="white"
        )
        self.vehicle_capacity_entry.pack(fill="x", ipady=8, pady=5)
        
        # Varsayılan Şarj
        tk.Label(
            form_frame,
            text="Varsayılan Şarj (kWh):",
            font=("Helvetica", 11, "bold"),
            bg="#16213e",
            fg="white",
            anchor="w"
        ).pack(fill="x", pady=(15, 5))
        
        self.vehicle_charge_entry = tk.Entry(
            form_frame,
            font=("Helvetica", 12),
            bg="#0f3460",
            fg="white",
            relief="flat",
            insertbackground="white"
        )
        self.vehicle_charge_entry.pack(fill="x", ipady=8, pady=5)
        
        # Varsayılan Şarj Hızı
        tk.Label(
            form_frame,
            text="Varsayılan Şarj Hızı (kW):",
            font=("Helvetica", 11, "bold"),
            bg="#16213e",
            fg="white",
            anchor="w"
        ).pack(fill="x", pady=(15, 5))
        
        self.vehicle_speed_entry = tk.Entry(
            form_frame,
            font=("Helvetica", 12),
            bg="#0f3460",
            fg="white",
            relief="flat",
            insertbackground="white"
        )
        self.vehicle_speed_entry.pack(fill="x", ipady=8, pady=5)
        
        # Ekle butonu
        add_btn = tk.Button(
            form_frame,
            text="✓ Aracı Ekle",
            command=self.add_custom_vehicle,
            bg="#4ecca3",
            fg="white",
            font=("Helvetica", 12, "bold"),
            relief="flat",
            cursor="hand2",
            activebackground="#45b393",
            activeforeground="white",
            padx=20,
            pady=12
        )
        add_btn.pack(fill="x", pady=20)
        
        # Sağ panel - Araç listesi
        right = tk.Frame(container, bg="#16213e", relief="raised", bd=2)
        right.pack(side="right", fill="both", expand=True, padx=(15, 0))
        
        list_title = tk.Label(
            right,
            text="📋 Kayıtlı Araçlar",
            font=("Helvetica", 16, "bold"),
            bg="#16213e",
            fg="white"
        )
        list_title.pack(pady=20)
        
        # Scrollable liste
        list_container = tk.Frame(right, bg="#16213e")
        list_container.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        scrollbar = tk.Scrollbar(list_container, bg="#0f3460")
        scrollbar.pack(side="right", fill="y")
        
        self.vehicle_listbox = tk.Listbox(
            list_container,
            font=("Helvetica", 11),
            bg="#0f3460",
            fg="white",
            selectbackground="#4ecca3",
            selectforeground="white",
            relief="flat",
            borderwidth=0,
            highlightthickness=0,
            yscrollcommand=scrollbar.set,
            selectmode=tk.SINGLE
        )
        self.vehicle_listbox.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.vehicle_listbox.yview)
        
        # Buton frame
        btn_frame = tk.Frame(right, bg="#16213e")
        btn_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        delete_btn = tk.Button(
            btn_frame,
            text="🗑️ Sil",
            command=self.delete_custom_vehicle,
            bg="#ff6b6b",
            fg="white",
            font=("Helvetica", 11, "bold"),
            relief="flat",
            cursor="hand2",
            activebackground="#ff5252",
            padx=15,
            pady=8
        )
        delete_btn.pack(side="left", padx=(0, 10))
        
        refresh_btn = tk.Button(
            btn_frame,
            text="🔄 Yenile",
            command=self.refresh_vehicle_list,
            bg="#457b9d",
            fg="white",
            font=("Helvetica", 11, "bold"),
            relief="flat",
            cursor="hand2",
            activebackground="#3d6d8a",
            padx=15,
            pady=8
        )
        refresh_btn.pack(side="left")
        
        self.refresh_vehicle_list()
    
    def refresh_vehicle_list(self):
        """Araç listesini yenile"""
        self.vehicle_listbox.delete(0, tk.END)
        for vehicle in self.custom_vehicles:
            self.vehicle_listbox.insert(
                tk.END,
                f"{vehicle['name']} - {vehicle['capacity']} kWh"
            )
    
    def add_custom_vehicle(self):
        """Yeni araç ekle"""
        try:
            name = self.vehicle_name_entry.get().strip()
            capacity = float(self.vehicle_capacity_entry.get())
            charge = float(self.vehicle_charge_entry.get())
            speed = float(self.vehicle_speed_entry.get())
            
            if not name:
                messagebox.showwarning("Uyarı", "Lütfen araç adı girin!")
                return
            
            if capacity <= 0 or charge < 0 or speed <= 0:
                messagebox.showwarning("Uyarı", "Lütfen geçerli değerler girin!")
                return
            
            vehicle = {
                "name": name,
                "capacity": capacity,
                "charge": charge,
                "speed": speed
            }
            
            self.custom_vehicles.append(vehicle)
            self.save_custom_vehicles()
            self.refresh_vehicle_list()
            self.refresh_vehicle_buttons()
            
            # Formu temizle
            self.vehicle_name_entry.delete(0, tk.END)
            self.vehicle_capacity_entry.delete(0, tk.END)
            self.vehicle_charge_entry.delete(0, tk.END)
            self.vehicle_speed_entry.delete(0, tk.END)
            
            messagebox.showinfo("Başarılı", f"{name} başarıyla eklendi!")
            
        except ValueError:
            messagebox.showerror("Hata", "Lütfen sayısal değerleri doğru formatta girin!")
    
    def delete_custom_vehicle(self):
        """Seçili aracı sil"""
        selection = self.vehicle_listbox.curselection()
        if not selection:
            messagebox.showwarning("Uyarı", "Lütfen silinecek aracı seçin!")
            return
        
        index = selection[0]
        vehicle_name = self.custom_vehicles[index]['name']
        
        if messagebox.askyesno("Onay", f"{vehicle_name} silinsin mi?"):
            del self.custom_vehicles[index]
            self.save_custom_vehicles()
            self.refresh_vehicle_list()
            self.refresh_vehicle_buttons()
            messagebox.showinfo("Başarılı", "Araç silindi!")
    
    def refresh_vehicle_buttons(self):
        """Hızlı seçim butonlarını yenile"""
        # Eski butonları temizle
        for widget in self.button_frame.winfo_children():
            widget.destroy()
        
        # Varsayılan araçlar
        default_vehicles = [
            ("Tesla Model Y SR", 62.5, 20, "62.5"),
            ("VW ID.4", 52, 25, "52"),
            ("Togg T10X", 52.4, 15, "52.4"),
        ]
        
        # Tüm araçları birleştir
        all_vehicles = default_vehicles + [
            (v['name'], v['capacity'], v['charge'], str(v['speed']))
            for v in self.custom_vehicles
        ]
        
        # Butonları oluştur
        for i, vehicle in enumerate(all_vehicles):
            name, capacity, charge, speed = vehicle
            row = i // 2
            col = i % 2
            
            btn = tk.Button(
                self.button_frame,
                text=f"{name}\n{capacity} kWh",
                command=lambda c=capacity, ch=charge, s=speed: self.set_vehicle(c, ch, s),
                bg="#2d3436",
                fg="gray",
                font=("Helvetica", 10, "bold"),
                relief="raised",
                bd=2,
                cursor="hand2",
                activebackground="#636e72",
                activeforeground="white",
                padx=12,
                pady=12
            )
            btn.grid(row=row, column=col, padx=5, pady=5, sticky="ew")
        
        self.button_frame.grid_columnconfigure(0, weight=1)
        self.button_frame.grid_columnconfigure(1, weight=1)
    
    def create_slider_section(self, parent, label_text, variable, min_val, max_val, resolution, color):
        frame = tk.Frame(parent, bg="#16213e")
        frame.pack(fill="x", padx=20, pady=10)
        
        label = tk.Label(
            frame,
            text=label_text,
            font=("Helvetica", 11, "bold"),
            bg="#16213e",
            fg="gray",
            anchor="w"
        )
        label.pack(fill="x")
        
        value_label = tk.Label(
            frame,
            text=f"{variable.get():.1f}",
            font=("Helvetica", 14, "bold"),
            bg="#16213e",
            fg=color,
            anchor="e"
        )
        value_label.pack(fill="x", pady=(5, 0))
        
        slider = tk.Scale(
            frame,
            from_=min_val,
            to=max_val,
            resolution=resolution,
            variable=variable,
            orient="horizontal",
            bg="#0f3460",
            fg="white",
            troughcolor="#1a1a2e",
            highlightthickness=0,
            sliderlength=30,
            sliderrelief="flat",
            activebackground=color,
            command=lambda x: self.on_slider_change(value_label, variable, color)
        )
        slider.pack(fill="x", pady=5)
        
        return slider
        
    def on_slider_change(self, label, variable, color):
        label.config(text=f"{variable.get():.1f}")
        self.update_display()
        
    def set_vehicle(self, capacity, charge, speed):
        self.battery_capacity.set(capacity)
        self.current_charge.set(charge)
        self.charging_speed.set(speed)
        self.update_display()
        
    def update_display(self):
        try:
            capacity = self.battery_capacity.get()
            current = self.current_charge.get()
            speed = float(self.charging_speed.get())
            
            if speed <= 0:
                speed = 1.0
                self.charging_speed.set("1.0")
        except:
            return
        
        # Mevcut şarjı kapasiteye göre sınırla
        if current > capacity:
            current = capacity
            self.current_charge.set(current)
        
        # Hesaplamalar
        percentage = (current / capacity) * 100
        remaining = capacity - current
        
        if remaining <= 0:
            hours = 0
            minutes = 0
        else:
            time_hours = remaining / speed
            hours = int(time_hours)
            minutes = int((time_hours - hours) * 60)
        
        # Batarya rengini belirle
        if percentage >= 80:
            color = "#4ecca3"
        elif percentage >= 50:
            color = "#457b9d"
        elif percentage >= 20:
            color = "#ffd93d"
        else:
            color = "#ff6b6b"
        
        # Batarya çiz
        self.draw_battery(percentage, color)
        
        # Yüzde göster
        self.percentage_label.config(text=f"{percentage:.1f}%", fg=color)
        
        # Enerji bilgisi
        self.energy_label.config(text=f"{current:.1f} / {capacity:.1f} kWh")
        self.remaining_label.config(text=f"Eksik: {remaining:.1f} kWh")
        
        # Süre göster
        if remaining <= 0:
            self.time_label.config(text="Tam Şarjlı! 🎉", fg="#4ecca3")
            self.finish_time_label.config(text="Araç hazır")
        else:
            time_text = ""
            if hours > 0:
                time_text += f"{hours} saat "
            time_text += f"{minutes} dakika"
            self.time_label.config(text=time_text, fg=color)
            
            finish_time = datetime.now() + timedelta(hours=hours, minutes=minutes)
            self.finish_time_label.config(text=f"Bitiş: {finish_time.strftime('%H:%M')}")
        
        # Maliyet
        cost = remaining * 2.50
        self.cost_label.config(text=f"{cost:.2f} TL")
        
    def draw_battery(self, percentage, color):
        canvas = self.battery_canvas
        canvas.delete("all")
        
        battery_x = 30
        battery_y = 30
        battery_width = 240
        battery_height = 90
        terminal_width = 20
        
        # Terminal
        canvas.create_rectangle(
            battery_x + battery_width, battery_y + 25,
            battery_x + battery_width + terminal_width, battery_y + battery_height - 25,
            fill="#34495e", outline="#2c3e50", width=2
        )
        
        # Gövde
        canvas.create_rectangle(
            battery_x, battery_y,
            battery_x + battery_width, battery_y + battery_height,
            fill="#2c3e50", outline="#34495e", width=3
        )
        
        # Dolgu
        fill_width = (battery_width - 10) * (percentage / 100)
        if fill_width > 0:
            canvas.create_rectangle(
                battery_x + 5, battery_y + 5,
                battery_x + 5 + fill_width, battery_y + battery_height - 5,
                fill=color, outline=""
            )
        
        # Parlama efekti
        if percentage > 5:
            canvas.create_rectangle(
                battery_x + 10, battery_y + 10,
                battery_x + 10 + max(0, fill_width - 10), battery_y + 30,
                fill="", outline="white", width=0,
                stipple="gray50"
            )

def main():
    root = tk.Tk()
    app = EVChargingCalculator(root)
    root.mainloop()

if __name__ == "__main__":
    main()
    #made by yaman alparslan
