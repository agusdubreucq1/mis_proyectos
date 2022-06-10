from modelo1 import *
from tkinter import *
from tkinter import ttk

class Panel():
    def __init__(self, window):
        self.root = window
        self.root.title("universidad")
        self.root.geometry("600x400")
        self.root.resizable(width=False, height=False)
        self.titulo = Label(self.root, text="Universidad", height=1, width=85)
        self.titulo.grid(row=0, column=0, columnspan=4)


        self.listado = Label(self.root, text = "materias aprobadas", height=1, width=30)
        self.listado.grid(row=1, column=0, columnspan=2)

        self.agregado = Label(self.root, text = "agregar materias", height=1, width=30)
        self.agregado.grid(row=1, column=2, columnspan=2, sticky=W+E)


        self.crud = Crud()
        try:
            self.crud.conexion()
            self.crud.crear_tabla()
        except:
            print("error")

        #treeview---------------------------------------------------------

        tree=ttk.Treeview(self.root, columns=("size", "modified"),height=13)
        tree["columns"]=("col1")
        tree.column("#0",width=20, anchor=W)
        tree.column("col1",width=20, anchor=W)

        tree.heading("#0", text="codigo")
        tree.heading("col1", text="materia")

        tree.grid(row=2,column=0,columnspan=2, rowspan=14, sticky=W+E)

        #treeview**************************************************
        var1, var2 = StringVar(), StringVar()

        self.label1= Label(self.root, text="codigo")
        self.label1.grid(row=3,column=2, sticky=W+E)

        self.label2= Label(self.root, text="materia")
        self.label2.grid(row=4,column=2, sticky=W+E)

        self.entrada1 = Entry(self.root, textvariable=var1)
        self.entrada1.grid(row=3, column=3)

        self.entrada2 = Entry(self.root, textvariable=var2)
        self.entrada2.grid(row=4, column=3)

        #botones******************************************************
        self.agregar = Button(self.root, text="agregar", command=lambda:self.crud.alta(self.entrada1.get(), self.entrada2.get(), tree))
        self.agregar.grid(row=5, column=2)

        self.eliminar = Button(self.root, text="eliminar", command=lambda:self.crud.borrar(tree))
        self.eliminar.grid(row=5, column=3)

        self.modificar = Button(self.root, text="modificar", command=lambda:self.crud.modificar(self.entrada1, self.entrada2, tree))
        self.modificar.grid(row=6, column=2)
        #botones******************************************************


        self.crud.seleccion(tree)



        
        