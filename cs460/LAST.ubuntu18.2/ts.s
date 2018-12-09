    .text
.code 32
.global reset_handler
.global vectors_start, vectors_end
.global proc, procsize
.global tswitch, scheduler, running, goumode
.global switchPgdir, mkPtable, get_cpsr, get_spsr
.global irq_tswitch, setulr
.global copy_vector, copyistack, irq_handler, vectorInt_init
.global int_on, int_off, lock, unlock
.global get_fault_status, get_fault_addr, get_spsr

reset_handler:
    ldr r0, =proc
    ldr r1, =procsize
    ldr r2, [r1, #0]
    add r0, r0, r2
    sub r0, #4
    mov r1, #0x2000
    str r1, [r0]
    mov sp, r1
    mov r4, r0

    // go in IRQ mode to set IRQ stack
    msr cpsr, #0xD2
    ldr sp, =irq_stack
    // go in FIQ mode to set FIQ stack
    msr cpsr, #0xD1
    ldr sp, =fiq_stack
    // go in ABT mode to set ABT stack
    msr cpsr, #0xD7
    ldr sp, =abt_stack
    // go in UND mode to set UND stack
    msr cpsr, #0xDB
    ldr sp, =und_stack
    // go back in SVC mode
    msr cpsr, #0xD3
    // set SVC mode spsr to USER mode with IRQ on
    msr spsr, #0x10

    // copy vector table to address 0
    bl copy_vector
    // create initial pgdir and pgtable at 16KB
    bl mkPtable
    ldr r0, mtable
    mcr p15, 0, r0, c2, c0, 0
    mcr p15, 0, r0, c8, c7, 0
    // set DOMAIN 0,1 : 01=CLIENT mode(check permission)
    mov r0, #0x5
    mcr p15, 0, r0, c3, c0, 0
    // enable MMU
    mrc p15, 0, r0, c1, c0, 0
    orr r0, r0, #0x00000001
    mcr p15, 0, r0, c1, c0, 0
    nop
    nop
    nop
    mrc p15, 0, r2, c2, c0
    mov r2, r2
    // enable IRQ interrupts, then call main() in C
    mrs r0, cpsr
    bic r0, r0, #0xC0
    mrs cpsr, r0
    BL main
    B . //main() never return; in case it does, just loop here
mtable: .word 0x4000
svc_entry:
    stmfd sp!, (r0-r12, lr)
    // access running PROC
    ldr r5, =running PROC
    ldr r6, [r5, #0]
    mrs r7, spsr
    str r7, [r6, #16]
    // to SYS mode to access Umode usp, upc
    mrs r7, cpsr
    mov r8, r7
    orr r7, r7, #ox1F
    msr cpsr, r7
    // now in SYS mode, sp and lr same as User mode
    str sp, [r6, #8]
    str lr, [r6, #12]
    // change back to SVC mode
    msr cpsr, r8
    // save kmode sp into running->ksp at offest 4;
    // used in fork() to copy parent's kstack to child's kstack
    str sp, [r6, #4]
    // enable IRQ interrupts
    mrs r7, cpsr
    bic r7, r7, #0xC0
    msr cpsr, r7
    bl svc_handler
    // replace saved r0 on stack with the return value
    add sp, sp, #4
    stmfd sp!, {r0}
goUmode:
// disable IRQ interrupts
    mrs r7, cpsr
    orr r7, r7, #0xC0 // I and F bits=1 mask out IRQ,FIQ
    msr cpsr, r7 // write to cpsr
    bl kpsig // handle outstanding signals
    bl reschedule // reschedule process
    // access running PROC
    ldr r5, =running
    // r5 = &running
    ldr r6, [r5, #0]
    // r6 -> PROC of running
    // goto SYS mode to access user mode usp
    mrs r2, cpsr // r2 = SVC mode cpsr
    mov r3, r2 // save a copy in r3
    orr r2, r2, #0x1F // r2 = SYS mode
    msr cpsr, r2 // change to SYS mode
    ldr sp, [r6, #8]
    msr cpsr, r3 // restore usp from running->usp
    // back to SVC mode
    // replace pc in kstack with p->upc
    mov r3, sp
    add r3, r3, #52
    ldr r4, [r6, #12]
    str r4, [r3]
    //return to running proc in Umode
    ldmfd sp!, {r0-r12, pc}^
irq_handler:
    sub lr, lr, #4
    stmfd sp!, {r0-r12, lr}
    // save all Umode regs in IRQ stack
    // may switch task at end of IRQ processing; save Umode info
    mrs r0, spsr
    and r0, #0x1F
    cmp r0, #0x10 // check whether was in Umode
    bne noUmode // no need to save Umode context if NOT in Umode
    // access running PROC
    ldr r5, =running // r5=&running
    ldr r6, [r5, #0] // r6 -> PROC of running
    mrs r7, spsr
    str r7, [r6, #16]
    // to SYS mode to access Umode usp=r13 and cpsr
    mrs r7, cpsr
    // r7 = SVC mode cpsr
    mov r8, r7
    // save a copy of cpsr in r8
    orr r7, r7, #0x1F // r7 = SYS mode
    msr cpsr, r7 // change cpsr to SYS mode
    // now in SYS mode, r13 same as User mode sp r14=user mode lr
    str sp, [r6, #8] // save usp into proc.usp at offset 8
    str lr, [r6, #12] // save upc into proc.upc at offset 12
    // change back to IRQ mode
    msr cpsr, r8
noUmode:
    bl irq_chandler
    // call irq_handler() in C in SVC mode
    // check mode
    mrs r0, spsr
    and r0, #0x1F
    cmp r0,  #0x10
    // check if in Umode
    bne kiret
    // proc was in Umode when IRQ interrupt: handle signal, may tswitch
    bl kpsig
    bl reschedule
    // re-schedule: may tswitch
    // CURRENT running PROC return to Umode
    ldr r5, =running
    // r5=&running
    ldr r6, [r5, #0]
    // r6 -> PROC of running
    // restore Umode.[sp,pc,cpsr] from saved PROC.[usp,upc,ucpsr]
    ldr r7, [r6, #16]
    // r7 = saved Umode cpsr
    // restore spsr to saved Umode cpsr
    msr spsr, r7
    // go to SYS mode to access user mode sp
    mrs r7, cpsr
    mov r8, r7
    // r7 = SVC mode cpsr
    // save a copy of cpsr in r8
    orr r7, r7, #0x1F // r7 = SYS mode
    msr cpsr, r7 // change cpsr to SYS mode
    // now in SYS mode; restore Umode usp
    ldr sp, [r6, #8]
    //set usp in Umode = running->usp
    // back to IRQ mode
    msr cpsr, r8
    // go back to IRQ mode
kiret:
    ldmfd sp!, {r0-r12, pc}^ // return to Umode
	here: // return from tswitch()
	restore Umode.[usp,cpsr] from PROC.[usp,ucpsr]
	ldmfd sp, {r0-r12, pc}^
	// return to Umode
// ---------------- ts.s.4 --------------------------
tswitch:
	// tswitch() in Kmode
	mrs r0, cpsr // disable interrupts
	orr r0, r0, #0xC0 // I and F bits=1: mask out IRQ, FIQ
	mrs cpsr, r0
	// I and F interrupts are disabled
	stmfd sp!, {r0-r12, lr} // save context in kstack
	ldr r0, =running // r0=&running; access running->PROC
	ldr r1, [r0, #0] // r1->running PROC
	str sp, [r1, #4] // running->ksp = sp
	bl scheduler
	ldr r0, =running // resume CURRENT running
	ldr r1, [r0, #0] // r1->runningPROC
	ldr sp, [r1, #4]
	mrs r0, cpsr // sp = running->ksp
	// disable interrupts
	bic r0, r0, #0xC0
	// enable I and F interrupts
	mrs cpsr, r0
	ldmfd sp!, {r0-r12, pc}
irq_tswitch:
	// irq_tswitch: task switch in IRQ mode
	mov r0, sp
	bl copyistack // r0 = IRQ mode current sp
	// transfer INT frame from IRQ stack to SVC stack
	mrs r7, spsr // r7 = IRQ mode spsr, which must be Umode cpsr
	// flatten out irq stack
	ldr sp, =irq_stack_top
	// change to SVC mode
	mrs r0, cpsr
	bic r1, r0, #0x1F // r1 = r0 = cspr's lowest 5 bits cleared to 0
	orr r1, r1, #0x13
	msr cpsr, r1 // OR in 0x13=10011 = SVC mode
	// write to cspr, so in SVC mode now
	ldr r5, =running // r5 = &running
	ldr r6, [r5, #0] // r6 -> PROC of running
	// svc stack already has an irq frame, set SVC sp to kstack[-14]
	ldr sp, [r6, #4] // SVC mode sp= &running->kstack[SSIZE-14]
	bl tswitch // switch task in SVC mode
	ldr r5, =running // r5=&running
	ldr r6, [r5, #0]
	ldr r7, [r6, #16] // r6 -> PROC of running
	// r7 = saved Umode cpsr
	// restore spsr to saved Umode cpsr
	msr spsr, r7
	// go to SYS mode to access user mode sp
	mrs r7, cpsr // r7 = SVC mode cpsr
	mov r8, r7 // save a copy of cpsr in r8
	orr r7, r7, #0x1F // r7 = SYS mode
	msr cpsr, r7
	// change cpsr to SYS mode
	// now in SYS mode; restore Umode usp
	ldr sp, [r6, #8] // restore usp
	ldr lr, [r6, #12] // restore upc; REALLY need this?
	// back to SVC mode
	msr cpsr, r8
	// go back to IRQ mode
	ldmfd sp!, {r0-r12, pc}^ // return via INT frame in SVC stack
switchPgdir: // switch pgdir to new PROC's pgdir; passed in r0
	// r0 contains new PROC's pgdir address
	mcr p15, 0, r0, c2, c0, 0
	// set TTBase
	mov r1, #0
	mcr p15, 0, r1, c8, c7, 0 // flush TLB
	mcr p15, 0, r1, c7, c10, 0 // flush cache
	mrc p15, 0, r2, c2, c0, 0
	// set domain: all 01=client(check permission)	
	mov r0, #0x5 //01|01 for CLIENT|client
	mcr p15, 0, r0, c3, c0, 0
	mov pc, lr // return
//-------------ts.s.5 --------------------------
// IRQ interrupt mask/unmask functions
int_on:
	msr cpsr, r0
	mov pc,lr
int_off:
	mrs r4, cpsr
	mov r0, r4
	orr r4, r4, #0x80
	// set bit means MASK off IRQ interrupt
	msr cpsr, r4
	mov pc,lr
	// enable IRQ directly
unlock:
	mrs r4, cpsr
	bic r4, r4, #0x80
	// clear bit means UNMASK IRQ interrupt
	msr cpsr, r4
	mov pc,lr
	// disable IRQ directly
lock:
	mrs r4, cpsr
	orr r4, r4, #0x80
	// set bit means MASK off IRQ interrupt
	msr cpsr, r4
	mov pc,lr
get_cpsr:
	mrs r0, cpsr
	mov pc, lr
get_spsr:
	mrs r0, spsr
	mov pc, lr
setulr: // setulr(oldPC): set Umode lr=oldPC for signal catcher()
	mrs r7, cpsr // to SYS mode
	mov r8, r7 // save cpsr in r8
	orr r7, #0x1F //
	msr cpsr, r7
	// in SYS mode now
	mov lr, r0
	msr cpsr, r8 // set Umode lr to oldPC
	// back to original mode
	mov pc, lr // return
vectors_start:
	LDR PC, reset_handler_addr
	LDR PC, undef_handler_addr
	LDR PC, svc_handler_addr
	LDR PC, prefetch_abort_handler_addr
	LDR PC, data_abort_handler_addr
	B .
	LDR PC, irq_handler_addr
	LDR PC, fiq_handler_addr
reset_handler_addr:	.word reset_handler
undef_handler_addr: .word undef_abort_handler
svc_handler_addr: .word svc_entry
prefetch_abort_handler_addr: .word prefetch_abort_handler
data_abort_handler_addr:
irq_handler_addr: .word data_abort_handler
.word irq_handler
fiq_handler_addr: .word fiq_handler
vectors_end:
// end of ts.s file

