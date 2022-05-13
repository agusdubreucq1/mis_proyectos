from tkinter import *
from tkinter import ttk
from tkinter.messagebox import*
import re
import random
import sqlite3

"""
EXPLICACION:
la idea del programa es poder listar las materias aprobadas de un alumno
pudiendo agregar, modificar, eliminar y consultar las materias, estas
se agregan por el id(el cual si o si va de 1 a 9999) y el nombre de
la materia(que es distinto de vacio). Con el id me referia al codigo de la materia
por eso mismo no lo hice incrementable ya que no depende del orden en que 
se apruebe la materia.
En la parte inferior se encuentra el boton de los colores, el cual al
presionarlo se cambian los colores del fondo, el boton de los colores, y 
del titulo de forma aleatoria.
"""


base = sqlite3.connect("mibase_tp.db")
cursor = base.cursor()
def crear_tabla(): 
    sql = "CREATE TABLE materias\
            (id INTEGER PRIMARY KEY,\
                    materia varchar(20))"
    cursor.execute(sql)
    base.commit()

try:
    crear_tabla()
except:
    print("tabla ya creada")




root = Tk()
root.title("HISTORIA ACADEMICA")
root.geometry("600x400")
root.resizable(width=False, height=False)



titulo = Label(root,text="UNIVERSIDAD", fg="red", bg="#aaaaaa", width=85, height=2)
titulo.grid(row=0, column=0, columnspan=4, pady=2)

tit_materias = Label(root,text="materias aprobadas", fg="black", width=30, height=2)
tit_materias.grid(row=1,column=0,columnspan=2, sticky=W+E, padx=2)

tit_agregar = Label(root,text="agregar materias", fg="black", width=30, height=2)
tit_agregar.grid(row=1,column=2,columnspan=2, sticky=W+E, padx=2)

#entrada de datos-------------------------------------------------------
label_id=Label(root,text="id", fg="black", width=15, height=1)
label_id.grid(row=2,column=2, sticky=W+E,padx=2,pady=1)

text_id = StringVar()
entrada_id=Entry(root,textvariable=text_id,width=15)
entrada_id.grid(row=2,column=3, padx=2,sticky=W+E)

label_mat=Label(root,text="materia", fg="black", width=15, height=1)
label_mat.grid(row=3,column=2, sticky=W+E,padx=2,pady=1)

text_mat = StringVar()
entrada_mat=Entry(root, textvariable=text_mat, width=15)
entrada_mat.grid(row=3, column=3, padx=2, sticky=W+E)
#entrada de datos******************************************************


#treeview---------------------------------------------------------

tree=ttk.Treeview(root, columns=("size", "modified"),height=13)
tree["columns"]=("col1")
tree.column("#0",width=15, anchor=W)
tree.column("col1",width=15, anchor=W)

tree.heading("#0", text="id")
tree.heading("col1", text="materia")

tree.grid(row=2,column=0,columnspan=2, rowspan=14, sticky=W+E)

#treeview**************************************************

#botones--------------------------------------------------------------

def actualizar_treeview(mitreview):
    records = mitreview.get_children()
    for element in records:
        mitreview.delete(element)

    sql = "SELECT * FROM materias ORDER BY id ASC"
    datos=cursor.execute(sql)

    resultado = datos.fetchall()
    for fila in resultado:
        print(fila)
        mitreview.insert("", 0, text=fila[0], values=(fila[1]))


def agregar():
    id1=text_id.get()
    print(id1)
    mat1=text_mat.get()
    print(mat1)
    patron=re.compile(r"^[1-9][0-9]{0,3}$")
    if re.match(patron,id1) and mat1!="":
        text_id.set("")
        text_mat.set("")
        tree.insert("", "end", text=str(id1), values=(mat1))
        print("materia agregada: ")
        rta.set("se agrego correctamente")

        sql1="INSERT INTO materias(id, materia) VALUES('"+id1+"', '"+mat1+"')"
        try:
            cursor.execute(sql1)
            base.commit()
        except:
            print("ya existia ese id")
        actualizar_treeview(tree)
    else:
        rta.set("no es una materia/id valido(del 1 al 9999)")

    

    
def eliminar():
    valor = tree.selection()
    print(valor)
    if valor==():
        print("no hay nada")
        rta.set("seleccione una fila para eliminar")
    else:
        if askyesno("eliminar","seguro que desea eliminar esa fila"):
            item = tree.item(valor)
            print(item)
            tree.delete(valor)
            id1=str(item['text'])
            #mat1=item['values'][0]
            print("el id es: ",id1,type(id1))
            #print("la mat es: ",mat1,type(mat1))
            print("materia eliminada")
            rta.set("")

            sql1="DELETE FROM materias WHERE id="+id1
            cursor.execute(sql1)
            base.commit()
            showinfo("si","la fila se elimino con exito")
        else:
            showinfo("no","la fila no se elimino")
    


    
def modificar():
    id1=text_id.get()
    mat1=text_mat.get()
    print(id1)
    print(mat1)
    text_id.set("")
    text_mat.set("")

    if id1!="" and mat1!="":
        sql1="UPDATE materias set materia='"+mat1+"' WHERE id="+id1
        cursor.execute(sql1)
        base.commit()
        actualizar_treeview(tree)
        print("materia modificada")
        rta.set("modificado exitoso")
    else:
        rta.set("no se pudo modificar")

def consultar():
    id1=text_id.get()
    mat1=text_mat.get()

    sql="SELECT * FROM materias WHERE id="+id1+" AND materia='"+mat1+"'"
    data=cursor.execute(sql)
    resultado=data.fetchall()
    print(resultado)
    if not resultado:
        rta.set("no se encontro")
    else:
        rta.set("se encontro")


funcion=[agregar, eliminar, modificar]
bot_agregar= Button(root,text="agregar", command=agregar)
bot_agregar.grid(row=4, column=2)

bot_eliminar= Button(root,text="eliminar", command=eliminar)
bot_eliminar.grid(row=5, column=2)

bot_modificar= Button(root,text="modificar", command=modificar)
bot_modificar.grid(row=4, column=3)

bot_consultar= Button(root,text="consultar", command=consultar)
bot_consultar.grid(row=5, column=3)


#botones***********************************************************

rta= StringVar()
respuesta = Label(root, textvariable=rta, fg="#f00")
respuesta.grid(row=6, column=2, rowspan=3, columnspan=2, sticky=W+E)

#boton colores-------------------------------------------------------------
def cambiar_color():
    valores=["0","1","2","3","4","5","6",\
        "7","8","9","a","b","c","d","e","f"]
    color_root="#"
    color_colores="#"
    color_titulo="#"
    color_letra="#"
    for x in range(0,6):
        num=random.randint(0,15)
        color_root+=valores[num]
        if num <14:
            color_colores+=valores[num+2]
        else:
            color_colores+="f"
        if num <12:
            color_titulo+=valores[num+4]
        else:
            color_titulo+="d"
        if num<8:
            color_letra+=valores[num+8]
        else:
            color_letra+=valores[num-8]
    print("color: ",color_root)
    print("color_colores: ",color_colores)
    root.configure(background=color_root)
    colores.configure(background=color_colores)
    titulo.configure(background=color_titulo, fg=color_letra)
    


colores=Button(root,text="colores",command=cambiar_color,width=30)
colores.grid(row=16,column=0,columnspan=4)



#boton colores*********************************************************************

actualizar_treeview(tree)

root.mainloop()