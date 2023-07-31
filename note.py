import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog
import os
from datetime import datetime
import shutil
import sys

class StickyNoteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sticky Note")
        self.notes = []
        
        # 메모를 표시할 텍스트 위젯 생성 및 설정
        self.text_widget = tk.Text(root, wrap="word", font=("Arial", 12), undo=True)
        self.text_widget.pack(fill=tk.BOTH, expand=True)
        
        # 메인 메뉴 생성 및 구성
        self.menu_bar = tk.Menu(root)
        self.root.config(menu=self.menu_bar)
        
        # 파일 메뉴와 그 하위 항목들 추가
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="파일", menu=self.file_menu)
        self.file_menu.add_command(label="새로운 메모", command=self.new_note)
        self.file_menu.add_command(label="메모 저장", command=self.save_note)
        self.file_menu.add_command(label="메모 불러오기", command=self.load_note)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="종료", command=self.root.quit)
        
    def new_note(self):
        # 사용자로부터 새로운 메모 제목을 입력받음
        note_title = simpledialog.askstring("새로운 메모", "메모 제목을 입력하세요:")
        if note_title:
            # 새로운 메모를 메모 리스트에 추가
            self.notes.append({"title": note_title, "content": ""})
            self.display_notes()
        
    def save_note(self):
        # 저장할 메모를 사용자에게 선택하도록 함
        if not self.notes:
            messagebox.showinfo("메모 저장", "저장할 메모가 없습니다.")
            return
        
        note_titles = [note["title"] for note in self.notes]
        selected_title = simpledialog.askstring("메모 저장", "저장할 메모를 선택하세요:", 
                                                list(note_titles), initialvalue=note_titles[0])
        
        # 선택된 메모를 찾아서 내용을 업데이트함
        selected_note = next((note for note in self.notes if note["title"] == selected_title), None)
        if selected_note:
            selected_note["content"] = self.text_widget.get("1.0", tk.END)
            
            # 파일 다이얼로그를 열어 파일명과 저장 경로를 입력받음
            file_path = filedialog.asksaveasfilename(defaultextension=".txt", 
                                                     initialfile=f"{selected_title}.txt",
                                                     filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
            
            # 파일명과 저장 경로가 선택되었다면 메모를 해당 파일에 저장함
            if file_path:
                with open(file_path, "w") as file:
                    file.write(selected_note["content"])
                messagebox.showinfo("메모 저장", "메모가 성공적으로 저장되었습니다.")
        else:
            messagebox.showerror("메모 저장", "메모 저장에 실패했습니다.")
        
    def load_note(self):
        # 저장된 메모 파일 목록을 읽어옴
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            # 선택된 파일의 내용을 읽어와서 텍스트 위젯에 표시
            with open(file_path, "r") as file:
                content = file.read()
                self.text_widget.delete("1.0", tk.END)
                self.text_widget.insert(tk.END, content)
        
    def display_notes(self):
        # 텍스트 위젯을 지우고 메모를 모두 표시함
        self.text_widget.delete("1.0", tk.END)
        
        # 모든 메모를 텍스트 위젯에 표시함
        for note in self.notes:
            title = note["title"]
            content = note["content"]
            self.text_widget.insert(tk.END, f"--- {title} ---\n")
            self.text_widget.insert(tk.END, content + "\n\n")

    def register_startup(self):
        # 현재 실행 중인 스크립트 파일의 경로를 가져옴
        script_path = os.path.abspath(sys.argv[0])

        # 윈도우 시작 프로그램 폴더 경로
        startup_folder = os.path.join(os.environ["APPDATA"], "Microsoft", "Windows", "Start Menu", "Programs", "Startup")
        
        # 애플리케이션을 윈도우 시작 프로그램 폴더로 복사
        app_shortcut_path = os.path.join(startup_folder, "StickyNoteApp.lnk")
        shutil.copy(script_path, app_shortcut_path)

if __name__ == "__main__":
    root = tk.Tk()
    app = StickyNoteApp(root)

    # 메모 애플리케이션을 윈도우 시작 프로그램으로 등록
    #app.register_startup()
    
    root.mainloop()
