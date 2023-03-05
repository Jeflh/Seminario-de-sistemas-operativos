print('\tProcesos bloqueados', end='\n\n')
      print ("{:<3} {:<20} {:<15} {:<0}".format('ID','Tiempo máximo estimado', 'Tiempo restante', 'Tiempo bloqueado'), end='\n\n')
      for process in blockedProcesses:
        print ("{:<13} {:<20} {:<15} {:<0}".format(process[0],process[2], process[3], process[5]))
        process[5] -= 1

        if process[5] == 0:
          blockedProcesses.remove(process)
          ejecutionMemory.insert(3, process)
      print('------------------------------------------------')