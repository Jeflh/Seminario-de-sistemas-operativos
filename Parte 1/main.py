import os

MAX_CAPACITY = 4 # Procesos máximos por lote
registeredID = []

def newProcess(count):
  os.system('cls')
  print(f'\n\tProceso {count}')
  name = input('\nNombre del programador: ')
  operation = input('Operación a realizar: ')
  maxTime = input('Tiempo máximo estimado: ')
  numberID = input('Número de programa (ID): ')
  
  # Validación de datos 
  if name == '' or operation == '' or maxTime == '' or numberID == '':
    print('\nNo se puede dejar ningún campo vacío.')
    os.system('pause')
    return None

  if not validId(numberID):
    print('\nEl ID ya se encuentra registrado, por favor ingrese otro')
    os.system('pause')
    return None

  if not validTime(maxTime):
    print('\nEl tiempo máximo debe ser un número entero mayor a 0.')
    os.system('pause')
    return None

  if not validOperation(operation):
    print('\nLa operación ingresada no es válida.')
    os.system('pause')
    return None

  registeredID.append(numberID) # Agrega el ID a la lista de IDs registrados

  return [name, operation, maxTime, numberID]

# Validación de ID
def validId(numberID):
  if numberID in registeredID:
    return False
  else:
    return True

def validOperation (operation):
  if '+' in operation or '-' in operation or '*' in operation or '/' in operation or '%' in operation:
    return True
  else:
    return False


def validTime (maxTime):
  if maxTime.isdigit() and int(maxTime) > 0:
    return True
  else:
    return False


def printBatch(batch):
  for process in batch:
    pass

def printLots(lots):
  pass


if __name__ == '__main__':
  # Código principal
  lots = []
  batch = []
  count = 1

  os.system('cls')
  processes = int(input('\nIngrese la cantidad de procesos que desea agregar: '))

  while processes != 0:
    process = newProcess(count)
    if process is not None:
      batch.append(process)
      count += 1
      if len(batch) == MAX_CAPACITY or processes == 1:
        lots.append(batch)
        batch = []

      processes -= 1

  print(lots)
