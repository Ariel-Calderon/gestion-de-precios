from cProfile import label
from pickle import FALSE
import tkinter as tk
from tkinter import Menu, messagebox
from tkinter import ttk
import logica

from setuptools import Command


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gestión de Precios para Qendra")
        self.geometry("800x600")
        self.crear_menu()

    def crear_menu(self):
        menu_principal = Menu(self)
        self.config(menu=menu_principal)

        menu_archivo = Menu(menu_principal, tearoff=0)
        menu_principal.add_cascade(label="Archivo", menu=menu_archivo)
        menu_archivo.add_command(label="Cargar Archivo CSV", command=self.cargar_archivo)
        menu_archivo.add_command(label="Generar Archivo CSV", command=self.generar_archivo)
        menu_archivo.add_command(label="Salir", command=self.quit)


        menu_productos = Menu(menu_principal, tearoff=0)
        menu_principal.add_cascade(label="Productos", menu=menu_productos)
        menu_productos.add_command(label="Listar Productos", command=self.listar_productos)
        menu_productos.add_command(label="Cargar Producto", command=self.cargar_producto)
        menu_productos.add_command(label="Borrar Producto", command=self.borrar_producto)
        menu_productos.add_command(label="Modificar Producto", command=self.modificar_producto)

        menu_secciones = Menu(menu_principal, tearoff=0)
        menu_principal.add_cascade(label="Secciones", menu=menu_secciones)
        menu_secciones.add_command(label="Listar Secciones",command=self.listar_secciones)
        menu_secciones.add_command(label="Cargar Secciones",command=self.cargar_secciones)
        menu_secciones.add_command(label="Borrar Secciones",command=self.borrar_secciones)
        menu_secciones.add_command(label="Modificar Secciones",command=self.modificar_secciones)

        menu_proveedores = Menu(menu_principal, tearoff=0)
        menu_principal.add_cascade(label="Proveedores", menu=menu_proveedores)
        menu_proveedores.add_command(label="Listar Proveedores",command=self.listar_proveedores)
        menu_proveedores.add_command(label="Cargar Proveedores",command=self.cargar_proveedores)
        menu_proveedores.add_command(label="Borrar Proveedores",command=self.borrar_proveedores)
        menu_proveedores.add_command(label="Modificar Proveedores",command=self.modificar_proveedores)

        menu_gestion = Menu(menu_principal, tearoff=0)
        menu_principal.add_cascade(label="Gestión de Precios", menu=menu_gestion)
        

    def cargar_archivo(self):
        pass

    def generar_archivo(self):
        pass

    def listar_productos(self):
        pass

    def cargar_producto(self):
        formulario= PlantillaProducto(self,"Cargar nuevo producto")
        formulario.grab_set()

    def borrar_producto(self):
        pass

    def modificar_producto(self):
        formulario = PlantillaProducto(self,"Modificar un producto","modificar")
        formulario.grab_set()

    def listar_secciones(self):
        pass

    def cargar_secciones(self):
        formulario=PlantillaSeccion(self,"Cargar nueva sección")
        formulario.grab_set()

    def borrar_secciones(self):
        pass

    def modificar_secciones(self):
        formulario=PlantillaSeccion(self,"Modificar una Sección","modificar")
        formulario.grab_set()

    def listar_proveedores(self):
        pass
    
    def cargar_proveedores(self):
        pass

    def borrar_proveedores(self):
        pass

    def modificar_proveedores(self):
        pass




class Plantilla(tk.Toplevel):

    def __init__(self,parent,clase_objeto,modo):
        super().__init__(parent)
        self.clase_objeto = clase_objeto
        self.modo = modo
        self.lista_de_widgets = []  #[etiqueta,widget,clave:bool]  
        self.lista_de_comboboxes = [] # [[objeto combox,"campo clave externa db",lista de id],] Sin incluir la clave principal
        self.clave_principal = [] #[objeto combobox, lista de id] cuando está implementada con un combobox
                                  #[objeto entry] cuando se trata de una entrada de texto y el valor se obtiene con get
        self.campos_obligatorios=[] #[campo de entrada] tiene que ser el objeto del input, sea un combobox o un entry simple 
        self.validacion_decimales = (self.register(self.solo_decimales_con_coma), '%P')
        self.validacion_enteros = (self.register(self.solo_numeros),'%P')

    def cancelar(self):
        self.reset_formulario()
        if self.modo == "modificar":
            self.switch_widgets()
            self.reset_formulario() #hay que resetear antes y despues de switchear los widgets

    def guardar(self):
        if self.chequear_campos_obligatorios():
            self.objeto = self.clase_objeto()        
            self.objeto.asignar_valores(self)
            guardado = self.objeto.guardar()
            if guardado[0]:
                 self.messagebox_temporal("Guardado",guardado[1],1500)
                 self.reset_formulario()
            else:
                self.messagebox_temporal("Error",guardado[1],1500)

    def modificar(self):
        if self.chequear_campos_obligatorios():
            self.objeto.asignar_valores(self)
            if self.objeto.modificar() is not None:
                self.messagebox_temporal("Modificado","El registro fue modificado correctamente.",1500)
                self.reset_formulario() #se resetean sólo los widgets activos
                self.switch_widgets()
                self.reset_formulario() #se resetean los widgets restantes
            else:
                self.messagebox_temporal("Error", "El registro no pudo ser modificado",1500)

    
    def seleccionar(self):   
        if (len(self.clave_principal)>1):
            indice = self.clave_principal[0].current()
            id = self.clave_principal[1][indice]
        else:                
            id = self.clave_principal[0].get()
        
        self.objeto = self.clase_objeto(id)
        self.objeto.completar_campos(self)
        self.switch_widgets()
    
    def messagebox_temporal(self,titulo, mensaje, duracion=2000):        
        ventana_emergente = tk.Toplevel()
        ventana_emergente.title(titulo)
        ventana_emergente.geometry("300x100")
                
        ventana_emergente.transient()
        ventana_emergente.grab_set()
        
        mensaje_label = tk.Label(ventana_emergente, text=mensaje, wraplength=250)
        mensaje_label.pack(expand=True, fill="both", padx=10, pady=10)
               
        ventana_emergente.after(duracion, ventana_emergente.destroy)

    def reset_formulario(self):       
        for widget in self.winfo_children():
            print(f"Widget detectado: {widget}, Tipo: {type(widget)}")            
            if isinstance(widget, ttk.Combobox):                
                widget.set("")
                print ("combobox detectado")
            elif isinstance(widget, tk.Entry):
                widget.delete(0, tk.END)  
                print ("entry detectado")

    def switch_widgets(self):
        for widget in self.winfo_children():
            try:
                estado_actual = str(widget.cget("state"))
                if isinstance(widget,ttk.Combobox):
                    nuevo_estado = "readonly" if estado_actual == "disabled" else "disabled"
                else:
                    nuevo_estado = "normal" if estado_actual == "disabled" else "disabled"             
                widget.configure(state=nuevo_estado)
            except (tk.TclError, AttributeError):
                pass  

    def chequear_campos_obligatorios(self):  
        mensaje = ""  
        check = True 
        print (self.campos_obligatorios)     
        for campo in self.campos_obligatorios:
            variable = campo.cget("textvariable")
            valor = self.getvar(variable) #.strip()
            print (valor)
            if valor is None or valor == "":                
                mensaje += f"El campo {self.obtener_label(campo)} está vacío\n"
        if mensaje != "":
            check = False 
            messagebox.showinfo("Falta información", mensaje)
            print (mensaje)                   
        return check


    def obtener_label(self, widget_objetivo):
        info = widget_objetivo.grid_info()
        fila = int(info["row"])
        columna = int(info["column"])
        contenedor = widget_objetivo.master

        for widget in contenedor.winfo_children():
            if isinstance(widget, tk.Label):
                info_label = widget.grid_info()
                if int(info_label["row"]) == fila and int(info_label["column"]) == columna -1:
                    return widget.cget("text")
        return None
    
    def solo_decimales_con_coma(self, texto):
        if texto == "":
            return True
        if texto.count(",") > 1:
            return False
        try:
            float(texto.replace(",", "."))
            return True
        except ValueError:
            return False
        
    def solo_numeros(self, texto):
        return texto.isdigit() or texto == ""    



    def crear_entry(self, obligatorio:bool, etiqueta: str, nombre_campo:str, validacion = None):
        parametros = self.clase_objeto.ver_parametros()
        tabla = parametros[0]
        campo_clave = parametros[1]

        etiqueta = tk.Label(self, text=etiqueta)
        setattr(self,nombre_campo, tk.StringVar())
        variable = getattr(self, nombre_campo)

        if validacion is not None:
            if validacion == "decimales":
                setattr(self,nombre_campo + "_entrada", tk.Entry(self,textvariable=variable,validate="key",validatecommand=self.validacion_decimales))
            elif validacion == "enteros":
                setattr(self,nombre_campo + "_entrada", tk.Entry(self,textvariable=variable,validate="key",validatecommand=self.validacion_enteros))            
        else:
            setattr(self,nombre_campo + "_entrada", tk.Entry(self,textvariable=variable))

        entry = getattr(self,nombre_campo + "_entrada")

        if campo_clave == nombre_campo:
            self.clave_principal.append(entry)

        if obligatorio:
            self.campos_obligatorios.append(entry)

        self.lista_de_widgets.append([etiqueta,entry,(campo_clave==nombre_campo)])

  
        


    def crear_combobox(self, obligatorio:bool, etiqueta: str, nombre_campo:str,campo_para_mostrar="descripcion",campo_para_guardar="id"):
            parametros = self.clase_objeto.ver_parametros()
            tabla = parametros[0]
            campo_clave = parametros[1]

            es_clave = (campo_clave==nombre_campo)
            if self.modo != "guardar" or not es_clave:                
                if es_clave:
                    lista_clase = getattr(logica, "Lista" + tabla)
                else:
                    lista_clase = getattr(logica, "Lista" + nombre_campo)
                lista_objeto=lista_clase()
                lista_mostrar= lista_objeto.listar_columnas([campo_para_mostrar])
                lista_guardar=lista_objeto.listar_columnas([campo_para_guardar])

                etiqueta = tk.Label(self, text=etiqueta)
                setattr(self,nombre_campo + "_variable", tk.StringVar())
                variable = getattr(self, nombre_campo + "_variable")
                        
                setattr(self,nombre_campo + "_entrada", ttk.Combobox(self,textvariable=variable,values=lista_mostrar,state="readonly"))
                combobox = getattr(self,nombre_campo + "_entrada")
                combobox.grid(row=0, column=1, padx=10, pady=5)  
                if es_clave:
                    self.clave_principal.append(combobox)
                    self.clave_principal.append(lista_guardar)
                else:
                    self.lista_de_comboboxes.append([combobox,nombre_campo,lista_guardar])

                if obligatorio:
                    self.campos_obligatorios.append(combobox)

                self.lista_de_widgets.append([etiqueta,combobox,es_clave])


    

    def render_formulario_ABM (self):
        fila = 0
        for widget in self.lista_de_widgets:
            widget[0].grid(row=fila, column=0, padx=10, pady=5, sticky="w")
            widget[1].grid(row=fila, column=1, padx=10, pady=5)  
            if widget[2] and self.modo=="modificar":
                    widget[0].configure(state="disabled") 
                    widget[1].configure(state="disabled")          
                    tk.Button(self, text="Seleccionar", command= self.seleccionar,state="disabled").grid(row=fila, column=2, columnspan=2, pady=20)
            fila += 1

        tk.Button(self, text="Cancelar", command=self.cancelar).grid(row=fila, column=1, columnspan=2, pady=20)
        if(self.modo=="guardar"):            
            tk.Button(self, text="Guardar", command=self.guardar).grid(row=fila, column=0, columnspan=2, pady=20)
        else:
            tk.Button(self, text="Modificar", command=self.modificar).grid(row=fila, column=0, columnspan=2, pady=20)
            self.switch_widgets()
        














class PlantillaProducto(Plantilla):
    

    def __init__(self, parent,titulo,modo="guardar"):
        super().__init__(parent,logica.Producto,modo)
        self.title(titulo)
        self.geometry("400x300")   

        self.crear_combobox(True,"Sección","Secciones")
        self.crear_entry(True,"Código de PLU","codigo_de_PLU","enteros")
        self.crear_entry(True, "Descripción","descripcion")

        self.render_formulario_ABM()  
            


   

class PlantillaSeccion(Plantilla):

    def __init__(self, parent,titulo,modo="guardar"):
        super().__init__(parent,logica.Seccion,modo)
        self.title(titulo)
        self.geometry("400x300")     

        self.crear_combobox(False,"Sección","id") #no es obligatorio cuando el id es autoincrement en la base
        self.crear_entry(True,"Descripción", "descripcion")
        self.crear_entry(False,"Porcentaje de Ganancia", "porcentaje_ganancia","decimales")

        self.render_formulario_ABM()

            


if __name__ == "__main__":
    app = App()
    app.mainloop()