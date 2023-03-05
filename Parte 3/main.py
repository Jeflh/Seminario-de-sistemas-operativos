import os
import time
import random
import keyboard
import threading


# Variables globales
MAX_CAPACITY = 4 
listedProcesses = []
blockedProcesses = []
finishedProcesses = []
pause_program = False
interruption = False
error = False
global_time = 0


def newProcess(count):
  numberID = count # 0
  operation = createOperation() # 1
  maxTime = random.randint(5, 6) # 2 debe ser 5, 16
  elapsedTime = 0 # 3
  result = None # 4
  blockedTime = None # 5
  joinedTime = None # 6
  finishedTime = None # 7
  returnTime = None # 8
  responseTime = None # 9
  waitingTime = None # 10
  serviceTime = None # 11

  return [numberID, operation, maxTime, elapsedTime, result, blockedTime, joinedTime, finishedTime, returnTime, responseTime, waitingTime, serviceTime]

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
  global global_time
  global_time = int(endTime - startTime)


def showTime():
  global global_time
  minutes, seconds = divmod(global_time, 60)
  print(f'[{minutes:02d}:{seconds:02d}]')



def setListedProcesses(list):
  global listedProcesses
  listedProcesses = list


def printInterface(startTime):
  global global_time
  global pause_program
  global interruption
  global error
  global listedProcesses
  global blockedProcesses
  
  countProcess = len(listedProcesses)
  executionMemory = []
  pressedIKey = False

  try: 
    while len(executionMemory) != MAX_CAPACITY:
      process = listedProcesses.pop(0)
      executionMemory.append(process)
  except:
    pass

  i = 0

  while i < countProcess:
    try:
      process = executionMemory[0]
    except:
      pass

    elapsedTime = 0
    maxTime = process[2]
    
    try:
      executionMemory.pop(0)
    except:
      pass
  
    while maxTime > 0:

      if pause_program:
        print('------------------------------------------------')
        print('El programa se encuentra pausado, presione "C" para continuar.')
        pausedTime = time.time()
        keyboard.wait('c')
        resumedTime = time.time()

        inactiveTime = int(resumedTime - pausedTime )
        startTime = startTime + inactiveTime
        global_time -= inactiveTime

      if interruption:
        process[2] = maxTime
        process[3] += elapsedTime
        process[5] = 0 # 8 es el tiempo de bloqueo
        blockedProcesses.append(process)
        interruption = False
        pressedIKey = True
        countProcess += 1
        break

      if error:
        process[4] = 'Error'
        finishedProcesses.append(process)
        error = False
        break

      os.system('cls')
      
      maxTime -= 1
      if maxTime == 0:
        result = makeOperation(process[1])       
        process[4] = result
        finishedProcesses.append(process)
        
        
      print(f'Nuevos procesos: {len(listedProcesses)}', end='\t\t\t')
      timer(startTime, time.time())
      showTime()
      print('------------------------------------------------')

      print(f'\tCola de procesos listos', end='\n\n')
      printList(executionMemory)
      print('------------------------------------------------') 

      process[3] = elapsedTime
      printProcess(process)
      print(f'Tiempo restante: {maxTime}')
      print('------------------------------------------------')

      if len(blockedProcesses) > 0:
        print('\tProcesos bloqueados', end='\n\n')
        blockedProcesses, executionMemory = printBlocked(blockedProcesses, executionMemory)
        print('------------------------------------------------')
      
      print('\tProcesos terminados', end='\n\n')
      printFinished()      
      elapsedTime += 1
      time.sleep(.5)              

    if len(executionMemory) < MAX_CAPACITY and pressedIKey == False:
      try:
        newProcess = listedProcesses.pop(0)
        executionMemory.append(newProcess)

      except:
        pass
     
    pressedIKey = False
    i += 1
  # Fin del ciclo WHILE

  
  os.system('cls')
  print(f'Procesos nuevos: {len(listedProcesses)}', end='\t\t\t')
  timer(startTime, time.time())
  showTime()
  print('------------------------------------------------')
  print('\tProcesos terminados', end='\n\n')
  printFinished()
  print('------------------------------------------------')
  print('Se han terminado todos los procesos.', end='\n\n')
  os.system('pause')


def printList(list):
  print ("{:<3} {:<25} {:<0}".format('ID','Tiempo máximo estimado', 'Tiempo transcurrido'), end='\n\n')
  for process in list:
    print ("{:<13} {:<24} {:<0}".format(process[0],process[2], process[3]))


def printBlocked(blockedProcesses, executionMemory):   
  print("{:<10}{:<0}".format('ID', 'Tiempo bloqueo restante'), end='\n\n')
  for process in blockedProcesses:
    print("{:<20}{:<0}".format(process[0], process[5]))
    process[5] += 1
  
    if process[5] == 8:
      blockedProcesses.remove(process)
      executionMemory.insert(3, process)

  return blockedProcesses, executionMemory


def printProcess(process):
  print('\tProceso en ejecución', end='\n\n')
  print(f'ID: {process[0]}')
  print(f'Operación: {process[1]}')
  print(f'Tiempo máximo estimado: {process[2]}')
  print(f'Tiempo transcurrido: {process[3]}')
  

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
  print ("{:<5} {:<10} {:<10} {:<5}".format('ID','Operación', 'Resultado', 'Estado'), end='\n\n')
  for process in finishedProcesses:
    print ("{:<5} {:<10} {:<10} {:<5}".format(process[0],process[1], process[4], 'Finalizado'))
  

# Eventos de teclado
def on_i_press(event):
  if event.event_type == 'down':
    # Interrupción del procesamiento de lotes
    global interruption
    interruption = True


def on_e_press(event):
  if event.event_type == 'down':
    # Error en el procesamiento de lotes
    global error
    error = True


def on_p_press(event):
  if event.event_type == 'down':
    # Pausar el procesamiento de lotes
    global pause_program
    pause_program = True


def on_c_press(event):
  if event.event_type == 'down':
    # Continuar el procesamiento de lotes
    global pause_program
    pause_program = False


if __name__ == '__main__':
  # Código principal
  
  count = 1

  os.system('cls')
  totalProcesses = int(input('\nIngrese el numero de procesos inicial: '))
  initialProcesses = totalProcesses

  # Registrar las funciones de devolución de llamada para cada tecla
  keyboard.on_press_key('i', on_i_press)
  keyboard.on_press_key('e', on_e_press)
  keyboard.on_press_key('p', on_p_press)
  keyboard.on_press_key('c', on_c_press)

  # Crear un hilo para la detección de pulsaciones de teclas
  key_thread = threading.Thread(target=keyboard.wait)
  key_thread.daemon = True  # Establecer como hilo de segundo plano
  key_thread.start()

  while initialProcesses != 0:
    createdProcess = newProcess(count)
    if createdProcess is not None:
      listedProcesses.append(createdProcess)
      initialProcesses -= 1
      count += 1

  os.system('cls')
  startTime = time.time()

  setListedProcesses(listedProcesses)
  printInterface(startTime)

  