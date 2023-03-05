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
  maxTime = random.randint(5, 16) # 2 debe ser 5, 16
  elapsedTime = 0 # 3
  result = None # 4
  blockedTime = 0 # 5
  joinedTime = '-' # 6 Tiempo de llegada
  finishedTime = '-' # 7 Tiempo de finalización
  returnTime = '-' # 8 Finalización - Llegada
  responseTime = '-' # 9 
  waitingTime = '-' # 10
  serviceTime = '-' # 11
  state = '-' # 12
  tme = maxTime # 13

  return [numberID, operation, maxTime, elapsedTime, result, blockedTime, joinedTime, finishedTime, returnTime, responseTime, waitingTime, serviceTime, state, tme]

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
  print(f'[{minutes:01d}:{seconds:02d}]')



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
      process[6] = int(time.time() - startTime) # Joined time
      process[12] = 'Nuevo'
      executionMemory.append(process)
  except:
    pass

  i = 0

  while i < countProcess:
    try:
      process = executionMemory[0]
    except:
      pass

    maxTime = process[2]
    # State of process
    process[12] = 'Listo'
    # Response time
    if process[9] == '-':
      process[9] = int(time.time() - startTime)
    # Waiting time
    process[10] = int(process[9] - process[6])
    

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
        process[5] = 0 # 8 es el tiempo de bloqueo
        process[12] = 'Bloqueado'
        blockedProcesses.append(process)
        interruption = False
        pressedIKey = True
        countProcess += 1
        break

      if error:
        process[2] = maxTime
        process[4] = 'ERROR'
        process[7] = int(time.time() - startTime)
        process[8] = process[3]
        process[11] = int(process[7] - process[10])
        process[12] = 'Finalizado'
        finishedProcesses.append(process)
        error = False
        break

      os.system('cls')
      
      maxTime -= 1
      if maxTime == 0:
        result = makeOperation(process[1])       
        # Result
        process[4] = result
        # Finished time
        process[7] = int( time.time() - startTime) + 1
        # Return time
        process[8] = int(process[7] - process[6])
        # Service time
        process[11] = process[13]
        process[12] = 'Finalizado'
        finishedProcesses.append(process)
        
        
      print(f'Nuevos procesos: {len(listedProcesses)}', end='\t\t\t')
      timer(startTime, time.time())
      showTime()
      print('------------------------------------------------')

      print(f'\tCola de procesos listos', end='\n\n')
      printList(executionMemory)
      print('------------------------------------------------') 
      
     
    
      printProcess(process)
      print(f'Tiempo restante: {maxTime + 1}')
      print('------------------------------------------------')

      if len(blockedProcesses) > 0:
        print('\tProcesos bloqueados', end='\n\n')
        blockedProcesses, executionMemory = printBlocked(blockedProcesses, executionMemory)
        print('------------------------------------------------')
      
      print('\tProcesos terminados', end='\n\n')
      printFinished()   

      process[3] += 1
      time.sleep(1)              

    if len(executionMemory) < MAX_CAPACITY and pressedIKey == False:
      try:
        newProcess = listedProcesses.pop(0)
        newProcess[6] = int(time.time() - startTime)
        executionMemory.append(newProcess)

      except:
        pass
     
    pressedIKey = False
    i += 1
  # Fin del ciclo WHILE

  
  os.system('cls')
  print(f'Procesos nuevos: {len(listedProcesses)}', end='\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t')
  timer(startTime, time.time())
  showTime()
  print('----------------------------------------------------------------------------------------------------------------------------------------------')
  print('\t\t\t\t\t\t\tProcesos terminados', end='\n\n')
  printFinishedTimes()
  print('----------------------------------------------------------------------------------------------------------------------------------------------')
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
    print ("{:<5} {:<10} {:<10} {:<5}".format(process[0],process[1], process[4], process[12]))
  

def printFinishedTimes():
  print("{:<4}{:<11}{:<11}{:<7}{:<10}{:<17}{:<12}{:<17}{:<13}{:<11}{:<12}{:<0}".format('ID', 'Operacion', 'Resultado', 'TME', 'Estado', 'T. Transcurrido', 'T. Llegada', 'T. Finalización', 'T. Servicio', 'T. Espera', 'T. Retorno', 'T. Respuesta'), end='\n\n')
  for process in finishedProcesses:
    print("{:<6}{:<11}{:<10}{:<4}{:<20}{:<14}{:<14}{:<15}{:<12}{:<12}{:<13}{:<0}".format(process[0], process[1], process[4], process[13], process[12], process[3], process[6], process[7], process[11], process[10], process[8], process[9]))

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

  