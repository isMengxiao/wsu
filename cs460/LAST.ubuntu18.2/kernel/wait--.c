//ksleep()
//  proc goes to sleep on an event.
//  sleeping PROCs are maintained in a FIFO sleepList for wake up
//kwakeup()
//  wakeup all PROCs that are sleeping on an event
//kexit()
//  proc termination in kernel
//kwait()
//  wait for ZOMBIE child proc, return its pid and exit status
