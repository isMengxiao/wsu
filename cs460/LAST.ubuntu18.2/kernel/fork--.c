//fork1()
//  a common code of all other fork functions.
//  create a new proc with a pgdir and pgtables
//kfork()
//  used only for P0 to create the INIT proc P1
//  loads Umode image file (/bin/init) to P1 and
//  initializes P1's kstack to make it ready to
//  run in Umode
//fork()
//  creates a child proc with an indentical Umode
//  image as the parent
//vfork()
//  the same as fork, but without copying images
