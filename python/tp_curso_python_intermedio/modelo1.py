import sqlite3
from peewee import *
import re


base = SqliteDatabase("mi_base1.db")

class BaseModel(Model):
    class Meta:
        database = base

class Tabla(BaseModel):
    id = IntegerField(primary_key=True)
    codigo = IntegerField()
    materia = CharField(unique = True)
    #para que no se puedan ingresar dos materias iguales- el unique



class Crud():
    
    def __init__(self,):
        pass

    def conexion(self,):
        base.connect()
    
    def crear_tabla(self, ):
        base.create_tables([Tabla])

    def alta(self, codigo, materia, mi_treview):
        patron=re.compile(r"^[1-9][0-9]{0,3}$")
        if re.match(patron,codigo) and materia !="":
            tabla = Tabla()
            tabla.materia = materia
            tabla.codigo = codigo
            try:
                tabla.save()
            except:
                print("debe ser una materia diferente")
            self.seleccion(mi_treview)
            
        else:
            print("no es una materia/cod valido(del 1 al 9999)")

        

    def seleccion(self, mi_treview):
        records = mi_treview.get_children()
        for elem in records:
            mi_treview.delete(elem)
        
        for fila in Tabla.select():
            mi_treview.insert("", 0, text=fila.codigo, values=(fila.materia))

    def borrar(self, mi_treview):
       
        try:
            linea = mi_treview.selection()
            item = mi_treview.item(linea)
            print(item)
            mi_treview.delete(linea)
            mat1=str(item['values'][0])
            borrar = Tabla.get(Tabla.materia==mat1)
            borrar.delete_instance()
        except:
            print("debe seleccionar una fila")
        

    def modificar(self, entrada_id, entrada_mat, mi_treview):
        try:
            linea = mi_treview.selection()
            item = mi_treview.item(linea)
            materiaAnt = str(item['values'][0])
            cod = entrada_id.get()
            materia = entrada_mat.get()

            patron=re.compile(r"^[1-9][0-9]{0,3}$")
            if re.match(patron,cod) and materia !="":
                actualizar = Tabla.update(materia = materia, codigo = cod).where(Tabla.materia== materiaAnt)
                actualizar.execute()
                self.seleccion(mi_treview)
            else:
                print("no es una materia/cod valido(del 1 al 9999)")
        except:
            print("selecciona una fila y luego escriba en las entradas")

    





    
if __name__=="__main__":
    pass
        

