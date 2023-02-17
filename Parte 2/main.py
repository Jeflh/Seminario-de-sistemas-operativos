import os
import time
import random
import keyboard
import threading

MAX_CAPACITY = 4 # Procesos máximos por lote
finishedProcesses = []


def newProcess(count):
  numberID = count
  operation = createOperation()
  maxTime = random.randint(5, 16)
  return [numberID, operation, maxTime]


def createOperation():
  a = random.randint(1, 100)
  b = random.randint(1, 100)
  operation = random.choice(['+', '-', '*', '/', '%'])
  return f'{a}{operation}{b}'


def validTime (maxTime):
  if maxTime > 0:
    return True
  else:
    return False


def timer(startTime, endTime):
  elapsedTime = int(endTime - startTime)
  minutes, seconds = divmod(elapsedTime, 60)
  return f'[{minutes:02d}:{seconds:02d}]'


def printInterface(batch, pending, processLeft, numLots, startTime):
  
  ejecutionBatch = batch.copy()

  for process in batch:
    ejecutionBatch.pop(0)
    elapsedTime = 0;     
    maxTime = process[2]

    while maxTime > 0:

      if maxTime == 1:
        result = makeOperation(process[1])
        process.append(result)
        process.append(numLots-pending)
        finishedProcesses.append(process)
        
      print(f'Lotes pendientes: {pending}', end='\t\t\t')
      print(timer(startTime, time.time()))
      print('------------------------------------------------')

      if pending != 0:
        print(f'\tLote {numLots-pending} en ejecución', end='\n\n')
        printBatch(ejecutionBatch)
        print('------------------------------------------------') 
        
      if pending != 0 and processLeft != 0:
        printProcess(process)
        print(f'\nTiempo restante: {maxTime}', end='\t')
        print(f'Tiempo transcurrido: {elapsedTime}')
        print('------------------------------------------------')
      
      print('\tProcesos terminados', end='\n\n')
      printFinished()
      maxTime -= 1
      elapsedTime += 1
      time.sleep(0.1)

      if maxTime == 0:
        processLeft -= 1

      if pending == 0 and processLeft == 0:
        print('------------------------------------------------')
        print('Se han terminado todos los procesos.', end='\n\n')
        os.system('pause')
      else:
        os.system('cls')

      
    

def printBatch(batch):
  print ("{:<10} {:<5}".format('ID','Tiempo máximo estimado'), end='\n\n')
  for process in batch:
    print ("{:<20} {:<5}".format(process[0],process[2]))


def printProcess(process):
  print('\tProceso en ejecución', end='\n\n')
  print(f'ID: {process[0]}')
  print(f'Operación: {process[1]}')
  print(f'Tiempo máximo estimado: {process[2]}')
  

def makeOperation(operation):
  if '+' in operation:
    separateItems = operation.split('+')
    a = int(separateItems[0])
    b = int(separateItems[1])
    result = a + b

  elif '-' in operation:
    separateItems = operation.split('-')
    a = int(separateItems[0])
    b = int(separateItems[1])
    result = a - b

  elif '*' in operation:
    separateItems = operation.split('*')
    a = int(separateItems[0])
    b = int(separateItems[1])
    result = a * b

  elif '/' in operation:
    separateItems = operation.split('/')
    a = int(separateItems[0])
    b = int(separateItems[1])
    result = a / b

  elif '%' in operation:
    separateItems = operation.split('%')
    a = int(separateItems[0])
    b = int(separateItems[1])
    result = a % b

  return round(result, 2)


def printFinished():
  print ("{:<5} {:<10} {:<10} {:<5}".format('ID','Operación', 'Resultado', 'Lote'), end='\n\n')
  for process in finishedProcesses:
    print ("{:<5} {:<10} {:<10} {:<5}".format(process[0],process[1], process[3], process[4]))
  

# Eventos de teclado
def on_i_press(event):
    if event.event_type == 'down':
      print('Se ha presionado la tecla I')

def on_e_press(event):
    if event.event_type == 'down':
      print('Se ha presionado la tecla E')

def on_p_press(event):
    if event.event_type == 'down':
      print('Se ha presionado la tecla P')

def on_c_press(event):
    if event.event_type == 'down':
      print('Se ha presionado la tecla C')


if __name__ == '__main__':
  # Código principal
  lots = []
  batch = []
  count = 1

  os.system('cls')
  total_process = int(input('\nIngrese el numero de procesos a trabajar: '))
  processLeft = total_process

  # Registrar las funciones de devolución de llamada para cada tecla
  keyboard.on_press_key('i', on_i_press)
  keyboard.on_press_key('e', on_e_press)
  keyboard.on_press_key('p', on_p_press)
  keyboard.on_press_key('c', on_c_press)

  # Crear un hilo para la detección de pulsaciones de teclas
  key_thread = threading.Thread(target=keyboard.wait)
  key_thread.daemon = True  # Establecer como hilo de segundo plano
  key_thread.start()


  while total_process != 0:
    process = newProcess(count)
    if process is not None:
      batch.append(process)
      count += 1
      if len(batch) == MAX_CAPACITY or total_process == 1:
        lots.append(batch)
        batch = []

      total_process -= 1

  time.sleep(0.5)
  os.system('cls')
  pending = len(lots) - 1
  startTime = time.time()

  for lot in lots:
    printInterface(lot, pending, processLeft, len(lots), startTime)
    pending -= 1
    processLeft -= 4
  
  