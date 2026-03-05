from enum import Enum

class RolEmpleado(Enum):
    TAQUILLERO="taquillero"
    ADMIN="admin"
    LIMPIEZA="limpieza"

class TipoSala(Enum):
    DOS_D="dos_d"
    TRES_D="tres_d"
    IMAX="imax"

class EstadoReserva(Enum):
    PENDIENTE="pendiente"
    PAGADA="pagada"
    CANCELADA="cancelada"

class Pelicula:
    def __init__(self, titulo, duracion, clasificacion, genero):
        self.titulo = titulo
        self.duracion = duracion
        self.clasificacion = clasificacion
        self.genero = genero
    def obtenerSinopsis(self):   
        return f"Titulo: {self.titulo}, Clasificación: {self.clasificacion}, Género: {self.genero}, Duración: {self.duracion} minutos" 
    
    def esAptaParaTodoPublico(self):
        return self.clasificacion in ["AA", "A"]

class Espacio:
    def __init__(self, idEspacio, nombre, ubicacion):
        self.idEspacio = idEspacio
        self.nombre = nombre
        self.ubicacion = ubicacion
        self.disponibilidad = True
    def verificarDisponibilidad(self): 
        if self.disponibilidad:
            return f"El espacio {self.idEspacio} está disponible"  
        else:
            return f"El espacio {self.idEspacio} está ocupado en la ubicación {self.ubicacion}" 
    
    def limpiarEspacio(self):
        return f"El espacio {self.idEspacio} ha sido limpiado"
    
class Promocion:
    def __init__(self,codigo, descripcion, porcentajeDescuento, fechaExpiracion):
        self.codigo = codigo
        self.descripcion = descripcion
        self.descuento = porcentajeDescuento   # Convertir porcentaje a decimal
        self.fechaExpiracion = fechaExpiracion
    def esValida(self, fechaActual):
        if fechaActual <= self.fechaExpiracion:
            return f"La promoción '{self.descripcion}' es válida hasta {self.fechaExpiracion}"
        else:
            return f"La promoción '{self.descripcion}' ha expirado el {self.fechaExpiracion}"
    def aplicarDescuento(self, precioOriginal):
        precioConDescuento = precioOriginal * (1 - self.descuento / 100)
        return f"Precio original: ${precioOriginal}, Descuento: {self.descuento}%, Precio final: ${precioConDescuento:.2f}"

class Persona:
    def __init__(self, idPersona, nombre, email, telefono):
        self.idPersona = idPersona
        self.nombre = nombre
        self.email = email
        self.telefono=telefono
    def login(self):
        return f"El usuario {self.nombre} con ID {self.idPersona} ha iniciado sesión"
    def logout(self):
        return f"El usuario {self.nombre} con ID {self.idPersona} ha cerrado sesión"    
    def actualizarDatos(self, nuevoEmail, nuevoTelefono):
        self.email = nuevoEmail
        self.telefono = nuevoTelefono
        return f"Los datos del usuario {self.nombre} han sido actualizados"
    
class Usuario(Persona):
    def __init__(self, idPersona, nombre, email, telefono, puntosFidelidad):
        super().__init__(idPersona, nombre, email, telefono)
        self.puntosFidelidad =puntosFidelidad
        self.historialReservas=[]
    def crearReserva(self, reserva):
        self.historialReservas.append(reserva)
        return f"La reserva {reserva.idReserva} ha sido creada para el usuario {self.nombre}"
    def consultarPromociones(self, promociones, fechaActual):
        promocionesValidas = [promo for promo in promociones if promo.esValida(fechaActual).startswith("La promoción")]
        return f"Promociones válidas para el usuario {self.nombre}: {[promo.descripcion for promo in promocionesValidas]}"
    def cancelarReserva(self, reserva):
        if reserva in self.historialReservas:
            self.historialReservas.remove(reserva)
            return f"La reserva {reserva.idReserva} ha sido cancelada para el usuario {self.nombre}"
        else:
            return f"La reserva {reserva.idReserva} no se encuentra en el historial del usuario {self.nombre}"
class Empleado(Persona):
    def __init__(self, idPersona, nombre, email, telefono, rol, horario, idEmpleado):
        super().__init__(idPersona, nombre, email, telefono)
        self.idEmpleado = idEmpleado
        self.rol = rol
        self.horario = horario
    def marcarEntrada(self, entrada):
        return f"El empleado {self.rol.value} ha marcado su entrada a las {entrada}"
    def gestionarFunciones(self, funcion):
        return f"El empleado {self.nombre} está gestionando la función {funcion.idFuncion}"
class Sala(Espacio):
    def __init__(self, idEspacio, nombre, ubicacion, tipo, capacidadTotal, esVip):
        super().__init__(idEspacio, nombre, ubicacion)
        self.tipo = tipo
        self.capacidadTotal = capacidadTotal
        self.esVip=esVip
    def ajustarAforo(self, numeroPersonas):
        if numeroPersonas <= self.capacidadTotal:
            return f"El aforo de la sala {self.nombre} ha sido ajustado para {numeroPersonas} personas"
        else:
            return f"No se puede ajustar el aforo de la sala {self.nombre} a {numeroPersonas} personas, excede la capacidad total de {self.capacidadTotal}"
    def obtenerTipoSala(self, pelicula):
        return f"La película '{pelicula.titulo}' ha sido asignada a la sala {self.nombre} de tipo {self.tipo.value}"
    
class ZonaComida(Espacio):
    def __init__(self, idEspacio, nombre, ubicacion, listaProductos, stockActual):
        super().__init__(idEspacio, nombre, ubicacion)
        self.listaProductos = listaProductos
        self.stockActual = stockActual
    def venderProducto(self, producto, cantidad):
        if producto in self.listaProductos and self.stockActual.get(producto, 0) >= cantidad:
            self.stockActual[producto] -= cantidad
            return f"Se han vendido {cantidad} unidades de {producto} en la zona de comida {self.nombre}"
        else:
            return f"No hay suficiente stock de {producto} para vender {cantidad} unidades en la zona de comida {self.nombre}"
    def actualizarInventario(self, producto, cantidad):
        self.stockActual[producto] = self.stockActual.get(producto, 0) + cantidad
        return f"El inventario del producto {producto} ha sido actualizado en la zona de comida {self.nombre}. Stock actual: {self.stockActual[producto]}"
class Funcion:
    def __init__(self, idFuncion, pelicula, sala, horarioInicio, precioBase):
        self.idFuncion = idFuncion
        self.pelicula = pelicula
        self.sala = sala
        self.horarioInicio = horarioInicio
        self.precioBase = precioBase
    def calcularAsientosLibres(self, asientosLibres):
        asientosOcupados = self.sala.capacidadTotal - asientosLibres
        return f"Asientos libres: {asientosLibres} | Asientos ocupados: {asientosOcupados}"
    def obtenerDetallesFuncion(self):
        return f"Funcion ID: {self.idFuncion}, Pelicula: {self.pelicula.titulo}, Sala: {self.sala.nombre}, Horario: {self.horarioInicio}, Precio: ${self.precioBase}"
class Reserva:
    def __init__ (self, idReserva, asientos, montoTotal, estado):
        self.idReserva = idReserva
        self.asientos = asientos
        self.montoTotal = montoTotal
        self.estado = EstadoReserva.PENDIENTE  
    def actualizarEstado(self, nuevoEstado):
        self.estado = nuevoEstado
        return f"El estado de la reserva {self.idReserva} ha sido actualizado a {self.estado.value}"
    def confirmarPago(self, montoPagado):
        if montoPagado >= self.montoTotal:
            self.estado = EstadoReserva.PAGADA
            return f"El pago de ${montoPagado:.2f} ha sido confirmado para la reserva {self.idReserva}. Estado actualizado a {self.estado.value}"
        else:
            return f"El monto pagado ${montoPagado:.2f} es insuficiente para la reserva {self.idReserva}. Monto total: ${self.montoTotal:.2f}"
    def generarTicket(self):
        if self.estado == EstadoReserva.PAGADA:
            return f"Ticket generado para la reserva {self.idReserva}. Asientos: {self.asientos}, Monto total: ${self.montoTotal:.2f}"
        else:
            return f"No se puede generar el ticket para la reserva {self.idReserva} porque el estado es {self.estado.value}"
    def aplicarPromocion(self, promocion, fechaActual):
        if promocion.esValida(fechaActual).startswith("La promoción"):
            descuentoAplicado = self.montoTotal * (promocion.descuento / 100)
            montoConDescuento = self.montoTotal - descuentoAplicado
            return f"Promoción '{promocion.descripcion}' aplicada. Descuento: ${descuentoAplicado:.2f}, Monto con descuento: ${montoConDescuento:.2f}"
        else:
            return f"No se puede aplicar la promoción '{promocion.descripcion}' porque ha expirado"
       

        