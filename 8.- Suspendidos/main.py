import os
import time
import random
import keyboard
import threading


# Variables globales
MEMORY_SIZE = 200
PAGE_SIZE = 5

frames = MEMORY_SIZE // PAGE_SIZE

# Crear la memoria como una lista de marcos de página vacíos
memory = ['    '] * frames
memory[38] = '💿   '
memory[39] = '💿   '
frames -= 2

listedProcesses = []
blockedProcesses = []
finishedProcesses = []
save_suspend = False
load_suspend = False
pause_program = False
interruption = False
key_new_process = False
show_table = False
error = False
global_time = 0

# se crea un nuevo proceso con los datos necesarios para su ejecución  
def createNewProcess(count):
  numberID = count # 0
  operation = createOperation() # 1
  maxTime = random.randint(5, 16) # 2 debe ser 5, 16
  elapsedTime = 0 # 3
  result = '-' # 4
  blockedTime = 0 # 5
  joinedTime = 0 # 6 Tiempo de llegada
  finishedTime = '-' # 7 Tiempo de finalización
  returnTime = '-' # 8 Finalización - Llegada
  responseTime = '-' # 9 
  waitingTime = 0 # 10 
  serviceTime = 0 # 11
  state = 'Nuevo' # 12
  tme = maxTime # 13
  size = random.randint(6, 25) # 14
  frames = [] # 15

  return [numberID, operation, maxTime, elapsedTime, result, blockedTime, joinedTime, finishedTime, returnTime, responseTime, waitingTime, serviceTime, state, tme, size, frames]


def divide_into_pages(process_size):
    num_pages, remainder = divmod(process_size, 5)
    if remainder > 0:
        num_pages += 1
    return num_pages


def find_empty_frame():
    empty_frames = [i for i, frame in enumerate(memory) if frame == '    ']
    if empty_frames:
        return random.choice(empty_frames)
    else:
        return None


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
  print(f'\t\t     [{minutes:01d}:{seconds:02d}]')



def setListedProcesses(list):
  global listedProcesses
  listedProcesses = list


def printInterface(startTime, quantum):
  global global_time
  global pause_program
  global show_table
  global key_new_process
  global interruption
  global error
  global listedProcesses
  global blockedProcesses
  global memory
  global frames
  global save_suspend
  global load_suspend

  suspendedCount = 0
  
  countProcess = len(listedProcesses)
  totalProcess = countProcess

  executionMemory = []
  pressedIKey = False


  try: 
    while frames >= 0:
      process = listedProcesses.pop(0)
      process[6] = int(time.time() - startTime) # Joined time
      num_pages = divide_into_pages(process[14])

      if (frames - num_pages) >= 0:
        for i in range(num_pages):
          empty_frame = find_empty_frame()
          if empty_frame is not None:
              memory[empty_frame] = '💙 ID:' + str(process[0])
              process[15].append(empty_frame)

        process[12] = 'Listo'
        executionMemory.append(process)
        frames -= num_pages

      else:
        listedProcesses.insert(0, process)
        break

  except:
    pass

  i = 0
  

  stablistQuantum = quantum

  while i < countProcess:

    try:
      process = executionMemory[0]
      noProcessYet = False

    except:
      noProcessYet = True
      process = []
      
    if noProcessYet == False:
      maxTime = process[2]
      # State of process
      process[12] = 'Listo'
      # Response time
      if process[9] == '-':
        process[9] = int(time.time() - startTime)   

    try:
      executionMemory.pop(0)
      noProcessYet = False
      
    except:
      noProcessYet = True
      maxTime = 99

    if noProcessYet and len(listedProcesses) == 0 and len(executionMemory) == 0 and len(blockedProcesses) == 0 and suspendedCount == 0:
      break
  
    while maxTime > 0:

      if process != []:
        for frame_index in process[15]:
          memory[frame_index] = '💗 ID:' + str(process[0])

      if quantum == 0 and noProcessYet == False:
        quantum = stablistQuantum
        process[2] = maxTime
        process[12] = 'Listo'
        listedProcesses.append(process)

        for frame_index in process[15]:
            memory[frame_index] = '💙 ID:' + str(process[0])

        try:
          newProcess = listedProcesses.pop(0)
          executionMemory.append(newProcess)
          countProcess += 1
          
        except:
          pass
      
        pressedIKey = True
        break

      if pause_program:
        print('------------------------------------------------')
        print('El programa se encuentra pausado, presione "C" para continuar.')
        pausedTime = time.time()
        keyboard.wait('c')
        resumedTime = time.time()

        inactiveTime = int(resumedTime - pausedTime )
        startTime = startTime + inactiveTime
        global_time -= inactiveTime

      # tiempos de bloqueo con coldown de 8
      if interruption:
        if noProcessYet == False:
          process[2] = maxTime
          process[5] = 0 # 8 es el tiempo de bloqueo
          process[11] = process[3]
          process[12] = 'Bloqueado'
          blockedProcesses.append(process)
          quantum = stablistQuantum
          for frame_index in process[15]:
            memory[frame_index] = '💜 ID:' + str(process[0])
        
        interruption = False
        pressedIKey = True
        countProcess += 1
        break
      
      if error:
        if noProcessYet == False and process != []:
          process[2] = maxTime
          process[4] = 'ERROR'
          process[7] = int(time.time() - startTime)
          # Return time
          process[8] = int(process[7] - process[6])
          # Service time
          process[11] = process[3]
          process[10] = int(process[8] - process[11])
          process[12] = 'Terminado'
          finishedProcesses.append(process)
          quantum = stablistQuantum

          for frame_index in process[15]:
            memory[frame_index] = '    '
          frames += len(process[15])


        error = False
        break

      if key_new_process:
        countProcess += 1
        totalProcess += 1
        newProcess = createNewProcess(totalProcess)
        listedProcesses.append(newProcess)
        num_pages = divide_into_pages(newProcess[14])

        if (frames - num_pages) >= 0:
          newProcess = listedProcesses.pop(0)
          newProcess[6] = int(time.time() - startTime) # Joined time
        
          for i in range(num_pages):
            empty_frame = find_empty_frame()
            if empty_frame is not None:
                memory[empty_frame] = '💙 ID:' + str(process[0])
                newProcess[15].append(empty_frame)

          executionMemory.append(newProcess)
          frames -= num_pages
            
        key_new_process = False

        if noProcessYet:
          noProcessYet = False
          break
      
      if load_suspend and suspendedCount > 0:
        processesLoaded = openFile()
        if processesLoaded == [] or processesLoaded == None:
          pass
        else:
          num_pages = divide_into_pages(processesLoaded[14])
          if (frames - num_pages) >= 0:
            for frame in processesLoaded[15]:
              memory[frame] = '💙 ID:' + str(processesLoaded[0])

            executionMemory.append(processesLoaded)
            frames -= num_pages

            suspendedCount -= 1

        load_suspend = False
        if noProcessYet:
          noProcessYet = False
          break
        

      if show_table:
        process[2] = maxTime
        process[3] += 1
        process[11] = process[3]
        process[12] = 'Ejecutando'
        os.system('cls')
        print(f'Procesos nuevos: {len(listedProcesses)}', end='\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t')
        timer(startTime, time.time())
        showTime()
        print('----------------------------------------------------------------------------------------------------------------------------------------------')
        print('\t\t\t\t\t\t\tTabla de procesos (BCP)', end='\n\n')
        printAllTimes(executionMemory, blockedProcesses, process)
        print('----------------------------------------------------------------------------------------------------------------------------------------------')
        printMemory()
        print('------------------------------------------------')
        print('El programa se encuentra pausado, presione "C" para continuar.')
        pausedTime = time.time()
        keyboard.wait('c')
        resumedTime = time.time()

        inactiveTime = int(resumedTime - pausedTime )
        startTime = startTime + inactiveTime
        global_time -= inactiveTime

        show_table = False

      os.system('cls')
      
      if noProcessYet == False and process != []:
        maxTime -= 1
        quantum -= 1

      #Se guarda todos los datos del proceso finalizado correctamente en la lista de procesos terminados
      if maxTime == 0 and process != []:
        result = makeOperation(process[1])       
        # Result
        process[4] = result
        # Finished time
        process[7] = int( time.time() - startTime) + 1
        # Return time
        process[8] = int(process[7] - process[6])
        # Service time
        process[11] = process[13]
         # Waiting time for round robin, tiempo de finalizacion - tiempo de llegada - tiempo de servicio
        process[10] = int(process[8] - process[11])
      
        process[12] = 'Terminado'
        finishedProcesses.append(process)
        for frame_index in process[15]:
          memory[frame_index] = '    '
        frames += len(process[15])

      timer(startTime, time.time())
      showTime() 
      print(f'Procesos nuevos: {len(listedProcesses)} \t\tSuspendidos: {suspendedCount}')
      
      try:
        print(f'Próximo:     ID: {listedProcesses[0][0]}   Tamaño: {listedProcesses[0][14]}     Páginas: {divide_into_pages(listedProcesses[0][14])}')
      except:
        pass
      print(f'Quantum: {stablistQuantum}\t\t   Quantum restante: {quantum + 1}')
      print('------------------------------------------------')

      print(f'\tCola de procesos listos', end='\n\n')
      if noProcessYet == False and process != []:
        printList(executionMemory)
      print('------------------------------------------------') 
      
      print('\tProceso en ejecución', end='\n\n')

      if noProcessYet == False and process != []:
        printProcess(process)
        print(f'Tiempo restante: {maxTime + 1}')
      
      print('------------------------------------------------')

      if len(blockedProcesses) > 0:
        if save_suspend:
          suspendProcess = blockedProcesses.pop(0)
          suspendProcess[12] = 'Nuevo'
          suspendProcess[5] = 0
          writeFile(suspendProcess)
          for frame_index in suspendProcess[15]:
            memory[frame_index] = '    '
          frames += len(suspendProcess[15])
          suspendedCount += 1
          save_suspend = False

        print('\tProcesos bloqueados', end='\n\n')
        blockedProcesses, executionMemory, enoProcessYet, maxTime = printBlocked(blockedProcesses, executionMemory, noProcessYet, maxTime)
        print('------------------------------------------------')
        
      else:
        save_suspend = False
      
      print('\tProcesos terminados', end='\n\n')
      printFinished()   
      
      if noProcessYet == False and process != []:
        process[3] += 1
      
      # print("Contador: ", countProcess)
      # print("Tiempo Maximo: ", maxTime)
      # print("Tiempo I: ", i)
      # print('----------------------------------------------------------------------------------------------------------------------------------------------')
      # print(noProcessYet)
      # print(len(listedProcesses))
      # print(len(executionMemory))
      # print(len(blockedProcesses))
      printMemory()
      time.sleep(1) 
       

    if frames >= 0 and pressedIKey == False or suspendedCount > 0:
      try:
        newProcess = listedProcesses.pop(0)
        newProcess[6] = int(time.time() - startTime) # Joined time
        num_pages = divide_into_pages(newProcess[14])

        if (frames - num_pages) >= 0:
          newProcess = listedProcesses.pop(0)
          newProcess[6] = int(time.time() - startTime) # Joined time
        
          for i in range(num_pages):
            empty_frame = find_empty_frame()
            if empty_frame is not None:
                memory[empty_frame] = '💙 ID:' + str(process[0])
                newProcess[15].append(empty_frame)
            newProcess[12] = 'Listo'

          executionMemory.append(newProcess)
          countProcess += 1
          frames -= num_pages

        else:
          # Agregar al principio de la lista de procesos
          listedProcesses.insert(0, newProcess)

      except:
        pass
     
    pressedIKey = False

    if noProcessYet == False and process != []:
      i += 1

  # Fin del ciclo WHILE

  # print(len(listedProcesses), len(executionMemory), len(blockedProcesses))

  if len(listedProcesses) == 0 and len(executionMemory) == 0 and len(blockedProcesses) == 0 and suspendedCount == 0:
    os.system('cls')

    timer(startTime, time.time())
    print(end='\t\t\t\t\t       ')
    showTime() 
    print('----------------------------------------------------------------------------------------------------------------------------------------------')
    print('\t\t\t\t\t\t\tProcesos terminados', end='\n\n')
    printTableOfTimes()
    print('----------------------------------------------------------------------------------------------------------------------------------------------')
    print('Se han terminado todos los procesos.', end='\n\n')
    try:
      os.remove('suspendido.txt')
    except OSError:
      pass
    os.system('pause')


def printMemory():
  global memory

  print('\n\t\tMarcos de memoria')
  for i in range(40):
    # Salto de linea cada 4 elementos
    if i % 4 == 0:
      print()

    # Mostrar el índice con dos dígitos
    index = str(i).zfill(2)
    print(f'{index}: {memory[i]}', end='\t\t')

  print()


def printList(list):
  print ("{:<3} {:<25} {:<0}".format('ID','Tiempo máximo estimado', 'Tiempo transcurrido'), end='\n\n')
  for process in list:
    print ("{:<13} {:<24} {:<0}".format(process[0],process[2], process[3]))


def printBlocked(blockedProcesses, executionMemory, noProcessYet, maxTime):   
  global frames
  print("{:<10}{:<0}".format('ID', 'Tiempo bloqueo restante'), end='\n\n')
  for process in blockedProcesses:
    print("{:<20}{:<0}".format(process[0], process[5]))
    process[5] += 1

    if process[5] == 8:
      blockedProcesses.remove(process)
      frames += len(process[15])

      if frames - len(process[15]) >= 0:
        executionMemory.append(process)
        frames -= len(process[15])

      else:
        listedProcesses.append(process)

      noProcessYet = False
      if maxTime == 99:
        maxTime = 0

  return blockedProcesses, executionMemory, noProcessYet, maxTime


def printProcess(process):
  print(f'ID: {process[0]}')
  print(f'Operación: {process[1]}')
  print(f'Tamaño: {process[14]}')
  print(f'Marcos: {process[15]}')
  print(f'Tiempo máximo estimado: {process[2]}')
  print(f'Tiempo transcurrido: {process[3]}')
  

#Tabla de procesos terminados en ejecución -------------------------------
def printFinished():
  print ("{:<5} {:<10} {:<10} {:<5}".format('ID','Operación', 'Resultado', 'Estado'), end='\n\n')
  for process in finishedProcesses:
    print ("{:<5} {:<10} {:<10} {:<5}".format(process[0],process[1], process[4], process[12]))
  

# tabla final de procesos terminados con todos los tiempos ----------------
def printTableOfTimes():
  print("{:<4}{:<11}{:<11}{:<7}{:<10}{:<17}{:<12}{:<17}{:<13}{:<11}{:<12}{:<0}".format('ID', 'Operacion', 'Resultado', 'TME', 'Estado', 'T. Transcurrido', 'T. Llegada', 'T. Finalización', 'T. Servicio', 'T. Espera', 'T. Retorno', 'T. Respuesta'), end='\n\n')
  for process in finishedProcesses:
    print("{:<6}{:<11}{:<9}{:<6}{:<18}{:<15}{:<14}{:<15}{:<12}{:<12}{:<13}{:<0}".format(process[0], process[1], process[4], process[13], process[12], process[3], process[6], process[7], process[11], process[10], process[8], process[9]))


def printAllTimes(executionMemory, blockedProcesses, actualProcess):
  print("{:<4}{:<11}{:<11}{:<7}{:<10}{:<17}{:<12}{:<17}{:<13}{:<11}{:<12}{:<0}".format('ID', 'Operacion', 'Resultado', 'TME', 'Estado', 'T. Transcurrido', 'T. Llegada', 'T. Finalización', 'T. Servicio', 'T. Espera', 'T. Retorno', 'T. Respuesta'), end='\n\n')

  allProcess = executionMemory + blockedProcesses + listedProcesses + finishedProcesses
  allProcess.insert(0, actualProcess)
  for process in allProcess:
    # Actualizar tiempo de espera para cada proceso

    if process[12] == 'Listo' and process[9] == '-':
      process[10] = global_time

    print("{:<6}{:<11}{:<9}{:<6}{:<18}{:<15}{:<14}{:<15}{:<12}{:<12}{:<13}{:<0}".format(process[0], process[1], process[4], process[13], process[12], process[3], process[6], process[7], process[11], process[10], process[8], process[9]))


def openFile():
  global frames
  try:
    with open('suspendido.txt', 'r+') as suspendedProcesses:
      lines = [line.rstrip('\n') for line in suspendedProcesses]

      process = lines[:16]
      requiredFrames = divide_into_pages(int(process[14]))

      if (frames - requiredFrames) >= 0: # Si hay suficientes marcos de memoria disponibles
        suspendedProcesses.seek(0)
        suspendedProcesses.truncate()
        suspendedProcesses.writelines('\n'.join(lines[16:]))
      
      # numberID = count # int 0
      # operation = createOperation() # str 1
      # maxTime = random.randint(5, 16) # int 2
      # elapsedTime = 0 # int 3
      # result = '-' # str 4
      # blockedTime = 0 # int 5 
      # joinedTime = 0 # int 6
      # finishedTime = '-' # str 7
      # returnTime = '-' # str 8
      # responseTime = '-' # str 9
      # waitingTime = 0 # int 10
      # serviceTime = 0 # int 11
      # state = 'Nuevo' # str 12
      # tme = maxTime # int 13
      # size = random.randint(6, 25) # int 14
      # frames = [] # list 15

      # Convertir a int los valores que lo necesiten
      process[0] = int(process[0])
      process[2] = int(process[2])
      process[3] = int(process[3])
      process[5] = int(process[5])
      process[6] = int(process[6])
      process[9] = int(process[9])
      process[10] = int(process[10])
      process[11] = int(process[11])
      process[13] = int(process[13])
      process[14] = int(process[14])
      
      # Convertir a list los valores que lo necesiten
      process[15] = [int(i) for i in process[15][1:-1].split(',')]

      return process

  except FileNotFoundError:
    return []


def writeFile(process):
    try:
      with open('suspendido.txt', 'a') as suspendedProcesses:
        for item in process:
          suspendedProcesses.writelines(str(item) + '\n')
    except IOError:
      pass


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

def on_a_press(event):
  if event.event_type == 'down':
    # Pausar el procesamiento de lotes
    global pause_program
    pause_program = True

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


def on_n_press(event):
  if event.event_type == 'down':
    # Continuar el procesamiento de lotes
    global key_new_process
    key_new_process = True
    

def on_t_press(event):
  if event.event_type == 'down':
    # Continuar el procesamiento de lotes
    global show_table
    show_table = True


def on_s_press(event):
  if event.event_type == 'down':
    global save_suspend
    save_suspend = True


def on_r_press(event):
  if event.event_type == 'down':
    global load_suspend
    load_suspend = True 


if __name__ == '__main__':
  # Código principal
  count = 1

  os.system('cls')
  totalProcesses = int(input('\nIngrese el numero de procesos inicial: '))
  initialProcesses = totalProcesses
  
  
  quantum = 0

  while True:
    quantum = int(input('\nIngrese el quantum: '))
    if quantum > 0 and quantum <= 16:
      break
    else:
      print('Ingrese un valor válido')

  # Registrar las funciones de devolución de llamada para cada tecla
  keyboard.on_press_key('i', on_i_press)
  keyboard.on_press_key('e', on_e_press)
  keyboard.on_press_key('p', on_p_press)
  keyboard.on_press_key('a', on_a_press)
  keyboard.on_press_key('c', on_c_press)
  keyboard.on_press_key('n', on_n_press)
  keyboard.on_press_key('t', on_t_press)
  keyboard.on_press_key('s', on_s_press)
  keyboard.on_press_key('r', on_r_press)

  # Crear un hilo para la detección de pulsaciones de teclas
  key_thread = threading.Thread(target=keyboard.wait)
  key_thread.daemon = True  # Establecer como hilo de segundo plano
  key_thread.start()

  while initialProcesses != 0:
    createdProcess = createNewProcess(count)
    if createdProcess is not None:
        listedProcesses.append(createdProcess)
        initialProcesses -= 1
        count += 1

  os.system('cls')
  startTime = time.time()

  # Borrar el archivo suspendido si es que existe
  try:
    os.remove('suspendido.txt')
  except OSError:
    pass

  setListedProcesses(listedProcesses)
  printInterface(startTime, quantum)

  