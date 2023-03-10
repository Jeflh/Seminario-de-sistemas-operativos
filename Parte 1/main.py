import os
import time

MAX_CAPACITY = 4 # Procesos máximos por lote
registeredID = []
finishedProcesses = []


def newProcess(count):
  os.system('cls')
  print(f'\n\tProceso {count}')

  name = input('\nNombre del programador: ')
  operation = input('Operación a realizar: ')

  if not validOperation(operation):
    print('\nLa operación ingresada no es válida.')
    os.system('pause')
    return None

  try:
    maxTime = int(input('Tiempo máximo estimado: '))
    if not validTime(maxTime):
      print('\nEl tiempo máximo debe ser un número entero mayor a 0.')
      os.system('pause')
      return None

    numberID = int(input('Número de programa: '))
    if not validId(numberID):
      print('\nEl ID ya se encuentra registrado, por favor ingrese otro')
      os.system('pause')
      return None
    
  except ValueError:
    print('\nEl tiempo estimado y el ID deben ser enteros positivos.')
    os.system('pause')
    return None
  
  # Validación de datos 
  if name == '' or operation == '' or maxTime == '' or numberID == '':
    print('\nNo se puede dejar ningún campo vacío.')
    os.system('pause')
    return None


  registeredID.append(numberID) # Agrega el ID a la lista de IDs registrados

  return [name, operation, maxTime, numberID]


def validId(numberID):
  if numberID in registeredID:
    return False
  else:
    return True


def validOperation (operation):
  if '+' in operation:
    separeteItems = operation.split('+')
    if separeteItems[0] == '' or separeteItems[1] == '':
      return False
    else:
      return True
  elif '-' in operation:
    separeteItems = operation.split('-')
    if separeteItems[0] == '' or separeteItems[1] == '':
      return False
    else:
      return True
  elif '*' in operation:
    separeteItems = operation.split('*')
    if separeteItems[0] == '' or separeteItems[1] == '':
      return False
    else:
      return True
  elif '%' in operation:
    separeteItems = operation.split('%')
    if separeteItems[0] == '' or separeteItems[1] == '':
      return False
    else:
      return True
  elif '/' in operation: 
    separateItems = operation.split('/')
    if separateItems[1] == '0' or separateItems[0] == '' or separateItems[1] == '':
      return False
    else:
      return True
  else:
    return False


def validTime (maxTime):
  if maxTime > 0:
    return True
  else:
    return False


def timer(startTime, endTime):
  elapsedTime = int(endTime - startTime)
  minutes, seconds = divmod(elapsedTime, 60)
  return f'[{minutes:02d}:{seconds:02d}]'


def printInterface(batch, pending, numLots, total_process, startTime):
  for process in batch:
    elapsedTime = 0;
    maxTime = process[2]
    while maxTime > 0:
      # Falta borrar el proceso de la lista de procesos en ejecución
      if maxTime == 1:
        result = makeOperation(process[1])
        process.append(result)
        process.append(numLots-pending)
        finishedProcesses.append(process)

      print(f'Lotes pendientes: {pending}', end='\t\t\t')
      print(timer(startTime, time.time()))
      print('------------------------------------------------')
      print(f'\tLote en ejecución', end='\n\n')
      printBatch(batch)
      print('------------------------------------------------')
      printProcess(process)
      print(f'\nTiempo restante: {maxTime}', end='\t')
      print(f'Tiempo transcurrido: {elapsedTime}')
      print('------------------------------------------------')
      print('\tProcesos terminados', end='\n\n')
      printFinished()

      maxTime -= 1
      elapsedTime += 1
      time.sleep(1)
      
      if maxTime == 0:
        total_process -= 1
      
      if pending == 0 and total_process == 0:
        print('------------------------------------------------')
        print('Se han terminado todos los procesos.', end='\n\n')
        os.system('pause')
      else:
        os.system('cls')
    

def printBatch(batch):
  print ("{:<10} {:<5}".format('Nombre','Tiempo máximo estimado'), end='\n\n')
  for process in batch:
    print ("{:<20} {:<5}".format(process[0],process[2]))


def printProcess(process):
  print('\tProceso en ejecución', end='\n\n')
  print(f'Nombre: {process[0]}')
  print(f'Operación: {process[1]}')
  print(f'Tiempo máximo estimado: {process[2]}')
  print(f'Número de programa: {process[3]}')
  

def makeOperation(operation):
  if '+' in operation:
    separateItems = operation.split('+')
    if '.' in separateItems[0]:
      a = float(separateItems[0])
    else:
      a = int(separateItems[0])

    if '.' in separateItems[1]:
      b = float(separateItems[1])
    else:
      b = int(separateItems[1])

    result = a + b

  elif '-' in operation:
    separateItems = operation.split('-')
    if '.' in separateItems[0]:
      a = float(separateItems[0])
    else:
      a = int(separateItems[0])

    if '.' in separateItems[1]:
      b = float(separateItems[1])
    else:
      b = int(separateItems[1])

    result = a - b

  elif '*' in operation:
    separateItems = operation.split('*')
    if '.' in separateItems[0]:
      a = float(separateItems[0])
    else:
      a = int(separateItems[0])

    if '.' in separateItems[1]:
      b = float(separateItems[1])
    else:
      b = int(separateItems[1])

    result = a * b

  elif '/' in operation:
    separateItems = operation.split('/')
    if '.' in separateItems[0]:
      a = float(separateItems[0])
    else:
      a = int(separateItems[0])

    if '.' in separateItems[1]:
      b = float(separateItems[1])
    else:
      b = int(separateItems[1])

    result = a / b

  elif '%' in operation:
    separateItems = operation.split('%')
    if '.' in separateItems[0]:
      a = float(separateItems[0])
    else:
      a = int(separateItems[0])

    if '.' in separateItems[1]:
      b = float(separateItems[1])
    else:
      b = int(separateItems[1])

    result = a % b

  return round(result, 2)


def printFinished():
  print ("{:<5} {:<10} {:<10} {:<5}".format('ID','Operación', 'Resultado', 'Lote'), end='\n\n')
  for process in finishedProcesses:
    print ("{:<5} {:<10} {:<10} {:<5}".format(process[3],process[1], process[4], process[5]))
  

if __name__ == '__main__':
  # Código principal
  lots = []
  batch = []
  count = 1

  os.system('cls')
  numProcess = int(input('\nIngrese la cantidad de procesos que desea agregar: '))
  total_process = numProcess
  while numProcess != 0:
    process = newProcess(count)
    if process is not None:
      batch.append(process)
      count += 1
      if len(batch) == MAX_CAPACITY or numProcess == 1:
        lots.append(batch)
        batch = []

      numProcess -= 1

  time.sleep(0.5)
  os.system('cls')
  pending = len(lots) - 1
  startTime = time.time()

  for lot in lots:
    printInterface(lot, pending, len(lots), total_process, startTime)
    pending -= 1
    total_process -= 4