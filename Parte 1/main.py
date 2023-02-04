

MAX_CAPACITY = 4 # Procesos máximos por lote
registeredId = []

def newProcess():
  name = input('\nNombre del programador: ')
  operation = input('Operación a realizar: ')
  maxTime = input('Tiempo máximo estimado: ')
  numberID = input('Número de programa (ID): ')
  
  
  # Validación de datos 
  if not validId(numberID):
    print('El ID ya se encuentra registrado, por favor ingrese otro')
    return None

  if name == '' or operation == '' or maxTime == '' or numberID == '':
    print('No se puede agregar el proceso, por favor ingrese todos los datos')
    return None

  registeredId.append(numberID) # Agrega el ID a la lista de IDs registrados
  print(registeredId) # Imprime la lista de IDs registrados
  return [name, operation, maxTime, numberID]

# Validación de ID
def validId(numberID):
  
  if numberID in registeredId:
    return False
  else:
    return True

    
if __name__ == '__main__':
  # Código principal
  lots = []
  batch = []

  processes = int(input('Ingrese la cantidad de procesos que desea agregar: '))

  while processes != 0:
    process = newProcess()

    if process is not None:
      batch.append(process)

    if len(batch) == MAX_CAPACITY or processes == 1:
      lots.append(batch)
      batch = []

    processes -= 1

  print(lots)



