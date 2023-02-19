import os
import time
import random
import keyboard
import threading

MAX_CAPACITY = 4 # Procesos máximos por lote
finishedProcesses = []
pause_program = False
interruption = False
error = False
global_time = 0

def newProcess(count):
  numberID = count
  operation = createOperation()
  maxTime = random.randint(5, 16)
  elapsedTime = 0
  result = None
  batch = None
  return [numberID, operation, maxTime, elapsedTime, result, batch]


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


def printInterface(batch, pending, processLeft, numLots, startTime):
  global global_time
  global pause_program
  global interruption
  global error

  ejecutionBatch = batch.copy()

  for process in batch:
    elapsedTime = 0
    ejecutionBatch.pop(0) 
    maxTime = process[2]
  
    process[5] = numLots-pending
    
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
        ejecutionBatch.append(process)
        batch.append(process)
        interruption = False
        break

      if error:
        processLeft -= 1
        process[4] = 'Error'
        finishedProcesses.append(process)
        error = False
        break

      os.system('cls')

      if maxTime == 1:
        result = makeOperation(process[1])       
        process[4] = result
        finishedProcesses.append(process)
        
      print(f'Lotes pendientes: {pending}', end='\t\t\t')
      timer(startTime, time.time())
      showTime()
      print('------------------------------------------------')

      if len(ejecutionBatch) != 0:
        print(f'\tProcesos en espera del lote en ejecución', end='\n\n')
        printBatch(ejecutionBatch)
        print('------------------------------------------------') 

      if processLeft != 0:
        printProcess(process)
        print(f'\n\tTiempo restante: {maxTime}')
        print('------------------------------------------------')
      
      print('\tProcesos terminados', end='\n\n')
      printFinished()

      maxTime -= 1
      elapsedTime += 1
      time.sleep(0.1)

      if maxTime == 0:
        processLeft -= 1

      if pending == 0 and processLeft == 0:
        os.system('cls')
        print(f'Lotes pendientes: {pending}', end='\t\t\t')
        timer(startTime, time.time())
        showTime()
        print('------------------------------------------------')
        print('\tProcesos terminados', end='\n\n')
        printFinished()
        print('------------------------------------------------')
        print('Se han terminado todos los procesos.', end='\n\n')
        os.system('pause')


def printBatch(batch):
  print ("{:<3} {:<25} {:<0}".format('ID','Tiempo máximo estimado', 'Tiempo transcurrido'), end='\n\n')
  for process in batch:
    print ("{:<13} {:<24} {:<0}".format(process[0],process[2], process[3]))


def printProcess(process):
  print('\tProceso en ejecución', end='\n\n')
  print(f'ID: {process[0]}')
  print(f'Lote: {process[5]}')
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
    print ("{:<5} {:<10} {:<10} {:<5}".format(process[0],process[1], process[4], process[5]))
  

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

  os.system('cls')
  pending = len(lots) - 1
  startTime = time.time()

  for lot in lots:
    printInterface(lot, pending, processLeft, len(lots), startTime)
    pending -= 1
    processLeft -= 4
  
  