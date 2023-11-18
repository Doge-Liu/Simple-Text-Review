import os  
import easygui as eg  
  
def save_changes(new_content):  
    with open("./doc.txt","w",encoding="UTF-8") as _poem:  
        _poem.write("".join(new_content))  
  
def modify_poem():   
    with open("./doc.txt","r",encoding="UTF-8") as _poem:  
        _poem_lists = _poem.readlines()  
        print(_poem_lists)  
        _poem_choice = eg.choicebox("选择你要修改的句子:",choices=_poem_lists,title="诗句修改器")  
        _poem_number = _poem_lists.index(_poem_choice)  
        _poem_edit = eg.enterbox(msg="您选择的是"+_poem_choice, title="诗句修改器")  
        if _poem_edit is not None: # 检查用户是否有输入  
            _poem_lists[_poem_number] = _poem_edit+"\n"
            print(_poem_lists)
            save_changes(_poem_lists) # 保存修改  
            eg.msgbox("修改已保存",title="成功")  
        else:  
            eg.msgbox("请输入新的诗句",title="警告")  

def create(text_file):
    