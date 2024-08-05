import tkinter as tk 
from tkinter import ttk, messagebox

import dnsdb2
import dnstwist
from rapidfuzz.distance import Levenshtein
import datetime


class Typosquatting_UI (tk.Tk):
    def __init__(self):
        super().__init__()
        self.label_bold = ttk.Style()
        self.label_bold.configure('Normal.TLabelframe.Label', font=('courier', 13, 'bold'))
        self.initial = True
        self.term = None
        self.subdomain_only = None
        self.fake_TLD = 'fakeTLD'               # leave this alone
        self.typosquatting_domains = {}
        self.unique_distance = set()
        self.typosquatting_domains_fuzzer = {}

        self.DNSDB_key = tk.StringVar()
        self.pad_object = 5        
        self.term_var = tk.StringVar()
        self.subdomain_only_var = tk.StringVar(None, True)
        self.timelast_var = tk.StringVar(None, '-300')
        self.total_var = tk.StringVar()
        self.totalclean_var = tk.StringVar()
        self.search_total_var = tk.StringVar()
        self.totalapi_var = tk.StringVar()
        self.seleted_data = tk.StringVar()
        self.selected_theme = tk.StringVar()
        self.search_entry = tk.StringVar()
        self.display_distance = tk.StringVar()
        self.punycode = tk.StringVar()
        self.client = None
        self.style = ttk.Style()
        self.tabControl = ttk.Notebook(self)
        
        self.geometry("1110x650")
        self.title("Typosquatting with DNSDB")
        
        self.tab_main = tk.Frame(self.tabControl, padx=self.pad_object, pady=self.pad_object)
        self.tab_api = tk.Frame(self.tabControl, padx=self.pad_object, pady=self.pad_object)
        self.tab_pdns = tk.Frame(self.tabControl, padx=self.pad_object, pady=self.pad_object)
        self.tab_setting = tk.Frame(self.tabControl, padx=self.pad_object, pady=self.pad_object)

        self.tab_main_tree1 = None
        self.tab_main_tree2 = None

        self.show_tab_main()
        self.show_tab_api()
        self.show_tab_pdns()
        self.show_tab_setting()
        
    def show_tab_setting(self):
        ### Setting
        tk.Label(self.tab_setting, text='DNSDB API Key:', font=('calibre',10, 'bold')).grid(row=0, column=0, sticky='w', pady=self.pad_object)
        tk.Entry(self.tab_setting, textvariable=self.DNSDB_key, show='*', width=50).grid(row=0, column=1, sticky='w', pady=self.pad_object)
        tk.Button(self.tab_setting, text="Save", command=self.saveAPIKey).grid(row=0, column=2, sticky='e', pady=self.pad_object)

        theme_frame = ttk.LabelFrame(self.tab_setting, text='Themes', style = "Normal.TLabelframe")
        theme_frame.grid(row=1, column=0, columnspan=3, sticky='w', padx=10)

        theme_row = 0
        for theme_name in self.style.theme_names():
            rb = ttk.Radiobutton(theme_frame, text=theme_name, value=theme_name, variable=self.selected_theme, command=lambda: self.change_theme())
            rb.grid(row=theme_row, padx=10, pady=5, sticky='w')
            theme_row += 1        
        return None
    
    def show_tab_main(self):
        ###
        main_frame = ttk.LabelFrame(self.tab_main, text=' User Input ', style="Normal.TLabelframe")
        main_frame.grid(row=0, column=0, sticky='nw', padx=10, pady=10)
        tk.Label(main_frame, text='Term:', font=('calibre',10, 'bold')).grid(row=0, column=0, sticky='w', pady=self.pad_object)
        tk.Entry(main_frame, textvariable=self.term_var).grid(row=0, column=1, columnspan=2, sticky='w', pady=self.pad_object)
        ttk.Separator(main_frame, orient='vertical').grid(row=0, column=3, rowspan=2, padx=25, sticky='nsew')
        tk.Button(main_frame, text="Generate Typosquatting", command=self.generateButton).grid(row=0, column=4, rowspan=2, pady=self.pad_object)

        tk.Label(main_frame, text='Subdomain Only:', font=('calibre',10, 'bold')).grid(row=1, column=0, sticky='w', pady=self.pad_object)
        tk.Radiobutton(main_frame, text='Yes', variable=self.subdomain_only_var, value=True, indicatoron=0).grid(row=1, column=1, sticky='w', pady=self.pad_object)
        tk.Radiobutton(main_frame, text='No', variable=self.subdomain_only_var, value=False, indicatoron=0).grid(row=1, column=2, sticky='w', pady=self.pad_object)

        self.tabControl.add(self.tab_main, text="    Main    ")
        self.tabControl.add(self.tab_api, text="    API    ")
        self.tabControl.add(self.tab_pdns, text="    pDNS Data    ")
        self.tabControl.add(self.tab_setting, text="    Setting    ")
        self.tabControl.pack(expand=1, fill='both')

        self.tab_main_summary_frame = ttk.LabelFrame(self.tab_main, text=' Total Summary ', width=350, style="Normal.TLabelframe")
        self.tab_main_summary_frame.grid(row=1, column=0, sticky='w', padx=10)
                
        # Row 3
        tk.Label(self.tab_main_summary_frame, text = 'Total: ', font=('calibre',10, 'bold')).grid(row=3, column=0, sticky='w', pady=self.pad_object)
        tk.Label(self.tab_main_summary_frame, textvariable=self.total_var).grid(row=3, column=1, columnspan=3, sticky='w', pady=self.pad_object)

        # Row 4
        tk.Label(self.tab_main_summary_frame, text = 'Clean Total: ', font=('calibre',10, 'bold')).grid(row=4, column=0, sticky='w', pady=self.pad_object)
        tk.Label(self.tab_main_summary_frame, textvariable=self.totalclean_var).grid(row=4, column=1, sticky=tk.W, pady=self.pad_object)
        
        # Row 5
        tk.Label(self.tab_main_summary_frame, text = 'Total API: ', font=('calibre',10, 'bold')).grid(row=5, column=0, sticky='w', pady=self.pad_object)
        tk.Label(self.tab_main_summary_frame, textvariable=self.totalapi_var).grid(row=5, column=1, sticky='w', pady=self.pad_object)

        self.tab_main_tree1 = ttk.Treeview(self.tab_main_summary_frame, column=(None, None), show='headings', height=10)        
        self.tab_main_tree1.heading("# 1", text="Levenshtein Distance")
        self.tab_main_tree1.column("# 1", anchor=tk.E)
        self.tab_main_tree1.heading("# 2", text="Number of Typosquatting")
        self.tab_main_tree1.column("# 2", anchor=tk.E)
        self.tab_main_tree1.grid(row=10, columnspan=5)

        # Typosquatting tab
        self.Typosquatting_frame = ttk.LabelFrame(self.tab_main, text=' Summary ', width=800, style="Normal.TLabelframe")
        self.Typosquatting_frame.grid(row=0, column=1, rowspan=2, sticky='w', padx=10, pady=10)

        self.tab_main_tree2 = ttk.Treeview(self.Typosquatting_frame, column=(None, None, None, None), show='headings', height=20)
        self.tab_main_tree2.heading("# 1", text="Distance")
        self.tab_main_tree2.column("# 1", anchor=tk.E, width=60)
        self.tab_main_tree2.heading("# 2", text="Label")
        self.tab_main_tree2.column("# 2", anchor=tk.E, width=150)
        self.tab_main_tree2.heading("# 3", text="Punycode")
        self.tab_main_tree2.column("# 3", anchor=tk.E, width=150)
        self.tab_main_tree2.heading("# 4", text="Fuzzer")
        self.tab_main_tree2.column("# 4", anchor=tk.E, width=150)
        self.tab_main_tree2.grid(row=0, column=0, columnspan=3)
        #tree.item(tree.selection()[0])['values'][1]
        self.tab_main_tree2.bind("<<TreeviewSelect>>", lambda event: self.get_punycode(self.tab_main_tree2))

        scrollbar2 = ttk.Scrollbar(self.Typosquatting_frame, orient=tk.VERTICAL, command=self.tab_main_tree2.yview)
        self.tab_main_tree2.configure(yscroll=scrollbar2.set)
        scrollbar2.grid(row=0, column=4, sticky='ns')

        tk.Label(self.Typosquatting_frame, text='Punycode:', font=('calibre',10, 'bold')).grid(row=1, column=0, sticky='w', pady=self.pad_object)
        tk.Entry(self.Typosquatting_frame, textvariable=self.punycode, width=30).grid(row=1, column=1, sticky='w', pady=self.pad_object)

        tk.Label(self.Typosquatting_frame, text='Search Punycode:', font=('calibre',10, 'bold')).grid(row=2, column=0, sticky='w', pady=self.pad_object)
        tk.Entry(self.Typosquatting_frame, textvariable=self.search_entry, width=30).grid(row=2, column=1, sticky='w', pady=self.pad_object)
        tk.Button(self.Typosquatting_frame, text="Search", command=lambda: self.search_tree(self.tab_main_tree2)).grid(row=2, column=2, sticky='e', pady=self.pad_object)
        
        tk.Label(self.Typosquatting_frame, text='Search Result:', font=('calibre',10, 'bold')).grid(row=3, column=0, sticky='w', pady=self.pad_object)
        tk.Label(self.Typosquatting_frame, textvariable=self.search_total_var).grid(row=3, column=1, sticky='w', pady=self.pad_object)
        
        tk.Label(self.Typosquatting_frame, text='Export to CSV:', font=('calibre',10, 'bold')).grid(row=4, column=0, sticky='w', pady=self.pad_object)
        tk.Button(self.Typosquatting_frame, text="Export", command=lambda: self.export_to_csv(self.tab_main_tree2)).grid(row=4, sticky='w', column=1, pady=self.pad_object)
        
        self.tab_main_summary_frame.grid_remove()
        self.Typosquatting_frame.grid_remove()
        return None

    def show_tab_api(self):
        # API tab
        self.tab_api_regex_frame = ttk.LabelFrame(self.tab_api, text=' Regex ', width=350, style="Normal.TLabelframe")
        self.tab_api_regex_frame.grid(row=0, column=0, sticky='w', padx=10, pady=10)
        self.tab_api_tree1 = ttk.Treeview(self.tab_api_regex_frame, column=(None, None, None, None), show='headings', height=10)
        self.tab_api_tree1.heading("# 1", text="Distance")
        self.tab_api_tree1.column("# 1", anchor=tk.E, width=60)
        self.tab_api_tree1.heading("# 2", text="Run")
        self.tab_api_tree1.column("# 2", anchor=tk.E, width=50)
        self.tab_api_tree1.heading("# 3", text="Total Run")
        self.tab_api_tree1.column("# 3", anchor=tk.E, width=60)
        self.tab_api_tree1.heading("# 4", text="Regex")
        self.tab_api_tree1.column("# 4", anchor=tk.E, width=326)
        self.tab_api_tree1.grid(row=0, column=0, columnspan=5)

        self.TArea = tk.Text(self.tab_api_regex_frame, height=17, width=62)
        self.TArea.grid(row=1, column=0, columnspan=3, padx=20, pady=self.pad_object)
        
        tk.Label(self.tab_api_regex_frame, text = 'Time Last After: ', font=('calibre',10, 'bold')).grid(row=2, column=0, sticky='w', padx=20, pady=self.pad_object)
        tk.OptionMenu(self.tab_api_regex_frame, self.timelast_var, '-300', '-600','-3600', '-7200', '-86400').grid(row=2, column=1, columnspan=2, sticky='w', pady=self.pad_object)
        tk.Button(self.tab_api_regex_frame, text="Call DNSDB API", command=lambda: self.call_DNSDB(self.tab_api_tree1)).grid(row=2, column=2, rowspan=2, pady=self.pad_object)        
        
        self.result_data_frame = ttk.LabelFrame(self.tab_api, text=' Result Data ', width=350, style="Normal.TLabelframe")           
        self.result_data_frame.grid(row=0, column=1, sticky='w', padx=10, pady=10)

        tk.Label(self.result_data_frame, textvariable=self.display_distance, font=('calibre',10, 'bold')).grid(row=0, column=0, columnspan=2, sticky='w', pady=self.pad_object)

        self.tab_api_tree2 = ttk.Treeview(self.result_data_frame, column=(None, None), show='headings', height=23)
        self.tab_api_tree2.heading("#1", text='RRType')
        self.tab_api_tree2.column("#1", anchor=tk.E, width=50)
        self.tab_api_tree2.heading("#2", text="Domain")
        self.tab_api_tree2.column("#2", anchor=tk.E, width=455)
        self.tab_api_tree2.grid(row=1, column=0)

        scrollbar4 = ttk.Scrollbar(self.result_data_frame, orient=tk.VERTICAL, command=self.tab_api_tree2.yview)
        self.tab_api_tree2.configure(yscroll=scrollbar4.set)
        scrollbar4.grid(row=1, column=1, sticky='ns')
        self.tab_api_tree2.bind("<<TreeviewSelect>>", lambda event: self.getDomainRow(TArea, self.tab_api_tree2))

        TArea = tk.Text(self.result_data_frame, height=1, width=55)
        TArea.grid(row=2, column=0, columnspan=2, sticky='w')
        tk.Button(self.result_data_frame, text="get pDNS", command=lambda: self.get_pDNS(TArea)).grid(row=2, column=0, sticky='e', pady=self.pad_object)     
        
        self.tab_api_regex_frame.grid_remove()
        self.result_data_frame.grid_remove()
        return None

    def show_tab_pdns(self):
        self.pDNS_frame = ttk.LabelFrame(self.tab_pdns, text=' Data ', width=350, style="Normal.TLabelframe")
        self.pDNS_frame.grid(row=0, column=0, sticky='w', padx=10, pady=10)

        self.tab_pdns_tree = ttk.Treeview(self.pDNS_frame, column=(None, None, None, None, None, None, None), show='headings', height=26, selectmode="extended")
        self.tab_pdns_tree.heading("#1", text='COUNT')
        self.tab_pdns_tree.column("#1", anchor=tk.E, width=50)
        self.tab_pdns_tree.heading("#2", text="TIME FIRST")
        self.tab_pdns_tree.column("#2", anchor=tk.E, width=120)
        self.tab_pdns_tree.heading("#3", text="TIME LAST")
        self.tab_pdns_tree.column("#3", anchor=tk.E, width=120)
        self.tab_pdns_tree.heading("#4", text="RRNAME")
        self.tab_pdns_tree.column("#4", anchor=tk.E, width=180)
        self.tab_pdns_tree.heading("#5", text="RRTYPE")
        self.tab_pdns_tree.column("#5", anchor=tk.E, width=50)
        self.tab_pdns_tree.heading("#6", text="BAILIWICK")
        self.tab_pdns_tree.column("#6", anchor=tk.E, width=180)
        self.tab_pdns_tree.heading("#7", text="RDATA")
        self.tab_pdns_tree.column("#7", anchor=tk.E, width=360)
        self.tab_pdns_tree.grid(row=1, column=0)   
        self.pDNS_frame.grid_remove()
        return None

    def generateButton (self):
        for item in self.tab_main_tree1.get_children(): self.tab_main_tree1.delete(item)
        for item in self.tab_main_tree2.get_children(): self.tab_main_tree2.delete(item)

        if (len(self.term_var.get()) == 0): 
            messagebox.showwarning('Error', 'Set a term value')
            return None
        
        self.intial = True
        self.term=self.term_var.get().lower()
        self.subdomain_only=self.subdomain_only_var.get()
        self.generate_info()

        self.total_var.set(self.total)
        self.totalclean_var.set(self.totalclean)

        total_API = 0
        for dist in self.unique_distance:
            tmp = [k for k,v in self.typosquatting_domains.items() if v == dist]
            self.tab_main_tree1.insert('', 'end', text="1", values=(dist, len(tmp)))

            for d in tmp:
                idna_encoded_bytes = d.encode('idna')
                unicode_string = idna_encoded_bytes.decode('idna')
                self.tab_main_tree2.insert('', 'end', text="1", values=(dist, unicode_string, d, self.typosquatting_domains_fuzzer[d]))          
            
            myregex = self.break_into_segment(tmp)

            total_API += len(myregex)
            
            # Each API call
            i = 1
            for reg in myregex:
                reg = '^.*({}).*\..*\..+$'.format('|'.join(reg)) if (self.subdomain_only) else '|'.join(reg)
                self.tab_api_tree1.insert('', 'end', text="1", values=(dist, i, len(myregex), reg))
                i += 1

        self.tab_api_tree1.bind("<<TreeviewSelect>>", lambda event: self.getAPIrow(self.TArea, self.tab_api_tree1))
        
        self.totalapi_var.set(total_API)
        
        if (self.initial):
            self.tab_main_summary_frame.grid()
            self.Typosquatting_frame.grid()
            self.tab_api_regex_frame.grid()
            #self.result_data_frame.grid()
            self.pDNS_frame.grid()
            self.initial = False
        return None
    
    def saveAPIKey(self):
        self.client = dnsdb2.Client(self.DNSDB_key.get())
        return None
    
    def generate_info(self):
        if (len(self.term) == 0):
            messagebox.showwarning('Error', 'Set a term value')
            return None
        
        ###
        self.typosquatting_domains = {}
        self.unique_distance = set()
        self.total = 0
        self.totalclean = 0
        self.search_total_var.set('')

        # Testing 
        #typosquatting_domains_object = []
        
        typosquatting = dnstwist.Fuzzer(self.term + '.' + self.fake_TLD)
        typosquatting.generate()

        for d in typosquatting.domains:
            new_d = d['domain'].replace( '.' + self.fake_TLD, '').replace('-' + self.fake_TLD + '.com', '').replace(self.fake_TLD, '')
            idna_encoded_bytes = new_d.encode('idna')
            unicode_string = idna_encoded_bytes.decode('idna')
            # skipping term in typosquatting (term<letter>)
            if (self.term in unicode_string): continue
            distance = Levenshtein.distance(self.term, unicode_string)

            self.typosquatting_domains[new_d] = distance
            self.unique_distance.add(distance)
            self.typosquatting_domains_fuzzer[new_d] = d['fuzzer']
            #print(new_d + " " + d['fuzzer'])

        self.typosquatting_domains[self.term] = 0
        self.unique_distance.add(0)
        self.typosquatting_domains_fuzzer[self.term] = ""

        self.total = len(typosquatting.domains)
        self.totalclean = len(self.typosquatting_domains)
        

        return None
 
    def break_into_segment (self, patterns):
        #Inputs must be less than 1250 total characters in length after encoding.
        # so far max tested with python is ~4164
        max_len = 3900          # Max Len for UI flex search (1250)   # 2048 default for DT # 4k max for API
        current_len = 0
        regex_array = []
        tmp_array = []
        for p in patterns:
            new_len = current_len + len(p) + 1      # 3 for the '|' after encoding (%7C) if using with UI else is 1
            if (current_len == 0):
                tmp_array.append(p)
                current_len = len(p)
            elif ((current_len > 0) and (new_len < max_len)):
                current_len = new_len
                tmp_array.append(p)
            else:
                regex_array.append(tmp_array)
                tmp_array = []                  # clear method causing issue
                tmp_array.append(p)
                current_len = len(p)

        regex_array.append(tmp_array)
        return regex_array

    def search_tree (self, tree):
        self.search_total = 0
        i = 0
        query = self.search_entry.get().lower()
        selections = []
        for child in tree.get_children():
            child_value = tree.item(child)['values']
            if query in (child_value[1] + child_value[2]):   # compare strings in  lower cases.
                selections.append(child)
                i += 1
        tree.selection_set(selections)
        #print(self.search_total)
        self.search_total_var.set(i)
        return None

    def export_to_csv (self, tree):
        dest_file = 'typosquatting_term.csv'
        with open(dest_file, 'w', encoding="utf-8") as writer:
            writer.write("{},{},{}".format('Distance','Label','Punycode\n'))
            for child in tree.get_children():
                chv = tree.item(child)['values']
                writer.write("{},{},{}\n".format(chv[0], chv[1], chv[2]))
        return None

    def getAPIrow (self, TArea, tree):
        TArea.delete(1.0, tk.END)
        TArea.insert(tk.END, tree.item(tree.selection()[0])['values'][3])
        return None

    def call_DNSDB(self, tree):
        try:
            row_id = tree.selection()[0]
        except Exception as e:
            messagebox.showwarning('Error', e)
            return None

        if (len(self.DNSDB_key.get()) == 0 ):
            messagebox.showwarning('Error', 'Set the DNSDB key in the setting tab')
            return None
        
        exclude = None

        myregex = tree.item(row_id)['values'][3]
        dist = tree.item(row_id)['values'][0]
        self.display_distance.set('Distance: ' + str(dist))

        time_last_after = self.timelast_var.get()
        limit = 1000000
        offset = 0
        for item in self.tab_api_tree2.get_children(): self.tab_api_tree2.delete(item)
        while True:
            try:                
                for res in self.client.flex_rrnames_regex(myregex, exclude=exclude, time_last_after=time_last_after, limit=limit, offset=offset):                
                    self.tab_api_tree2.insert('', 'end', text="0", values=(res['rrtype'], res['rrname']))                
            except dnsdb2.QueryLimited as e:
                offset += limit
            except dnsdb2.exceptions.QueryError as e:
                messagebox.showwarning('Error', e)
                break
            except dnsdb2.exceptions.QueryFailed as e:
                messagebox.showwarning('Error', e)
                break
            except dnsdb2.DnsdbException as e:
                messagebox.showwarning('Error', e)
                break
            else:
                break
        
        self.result_data_frame.grid()
        return None

    def getDomainRow(self, TArea, tree):
        TArea.delete(1.0, tk.END)
        TArea.insert(tk.END, tree.item(tree.selection()[0])['values'][1])
        return None

    def get_pDNS (self, TArea):
        domain = str(TArea.get('1.0','2.0')).strip()

        time_last_after = self.timelast_var.get()
        limit = 1000000
        offset = 0
        for item in self.tab_pdns_tree.get_children(): self.tab_pdns_tree.delete(item)
        while True:
            try:
                for res in self.client.lookup_rrset(domain, time_last_after=time_last_after):
                    f_date = datetime.datetime.fromtimestamp(res['time_first'])
                    l_date = datetime.datetime.fromtimestamp(res['time_last'])
                    self.tab_pdns_tree.insert('', 'end', text="0", values=(res['count'], f_date, l_date, res['rrname'], res['rrtype'], res['bailiwick'], res['rdata']))  
            except dnsdb2.QueryLimited as e:
                offset += limit
            except dnsdb2.exceptions.QueryError as e:
                messagebox.showwarning('Error', e)
                break
            except dnsdb2.exceptions.QueryFailed as e:
                messagebox.showwarning('Error', e)
                break
            except dnsdb2.DnsdbException as e:
                messagebox.showwarning('Error', e)
                break
            else:
                break
        return None

    def get_punycode (self, tree):
        self.punycode.set(tree.item(tree.selection()[0])['values'][2])        
        return None

if __name__ == "__main__":
    tt = Typosquatting_UI()
    tt.mainloop()
