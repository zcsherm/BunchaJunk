TITLE Program Template     (template.asm)

; Author: 
; Last Modified:
; OSU email address: ONID_ID@oregonstate.edu
; Course number/section:   CS271 Section ???
; Project Number:                 Due Date:
; Description: This file is provided as a template from which you may work
;              when developing assembly projects in CS271.

INCLUDE Irvine32.inc

; (insert macro definitions here)

; (insert constant definitions here)
DAYS_MEASURED = 28
TEMPS_PER_DAY = 23
MAX_TEMP	  = 40
MIN_TEMP	  = 30
ARRAYSIZE	  = DAYS_MEASURED * TEMPS_PER_DAY
DATA_SIZE	  = 1										; Change if you change the size of the temp entries
TEMP_RANGE	  = MAX_TEMP + 1 - MIN_TEMP
;TEMP_BAND	  = TEMP_RANGE / (DAYS_MEASURED/2)

.data

	temp_array		BYTE ARRAYSIZE DUP(?)
	daily_lows		BYTE ARRAYSIZE DUP(?)
	daily_highs		BYTE ARRAYSIZE DUP(?)
	average_low		BYTE ?
	average_high	BYTE ?
	space_char		BYTE " ",0
	temp_msg		BYTE "Here are the temperatures for each day (each row is a day):",13,10,0
	low_msg			BYTE "These are the low temperatures for each day:",13,10,0
	high_msg		BYTE "These are the high temperatures for each day:",13,10,0

.code
main PROC
	
	; Get a new seed
	CALL	Randomize

	; Get our temperature data
	PUSH	OFFSET temp_array
	CALL	generateTemperatures

	; Print the temperatures
	PUSH	DWORD PTR DAYS_MEASURED
	PUSH	DWORD PTR TEMPS_PER_DAY
	PUSH	OFFSET temp_msg
	PUSH	OFFSET space_char
	PUSH	OFFSET temp_array
	CALL	displayTempArray

	; Get the daily lows
	PUSH	OFFSET daily_lows
	PUSH	OFFSET temp_array
	CALL	findDailyLows

	; Get the daily highs
	PUSH	OFFSET daily_highs
	PUSH	OFFSET temp_array
	CALL	findDailyHighs

	; Print out the lows for each day
	PUSH	DWORD PTR 1
	PUSH	DWORD PTR DAYS_MEASURED
	PUSH	OFFSET low_msg
	PUSH	OFFSET space_char
	PUSH	OFFSET daily_lows
	CALL	displayTempArray

	; Print out the highs for each day
	PUSH	DWORD PTR 1
	PUSH	DWORD PTR DAYS_MEASURED
	PUSH	OFFSET high_msg
	PUSH	OFFSET space_char
	PUSH	OFFSET daily_highs
	CALL	displayTempArray
	Invoke ExitProcess,0	; exit to operating system
main ENDP

;-------------------------------------------------------------------------------------------------------------
; Name: generateTemperatures
;
; Description: Prints the program details and extracredit info
;
; Preconditions: None
;
; Postconditions: None
;
; Receives: 
;			[EBP+8]	 - temp_array_offset , reference - input/output
;
; Returns: None, alters command line
;
;------------------------------------------------------------------------------------------------------------
generateTemperatures	PROC
	; Preserve registers
	PUSH	EBP
	MOV		EBP, ESP
	PUSH	ECX
	PUSH	EAX
	PUSH	ESI
	
	; Generate a temp for every temp in the range
	MOV		ECX, ARRAYSIZE
	MOV		ESI, [EBP+8]

_get_random_temp:
	; Get a random value in the range of our temps
	MOV		EAX, TEMP_RANGE
	CALL	RandomRange

	; Add the min temp to it so it is between min and max temp
	ADD		EAX, MIN_TEMP

	; Write it into the array and move the index forward
	MOV		[ESI], EAX
	ADD		ESI, DATA_SIZE
	LOOP	_get_random_temp
	
	; Restore registers
	POP		ESI
	POP		EAX
	POP		ECX
	POP		EBP
	RET		4

generateTemperatures	ENDP

;-------------------------------------------------------------------------------------------------------------
; Name: findDailyLows
;
; Description: finds the low temperatures for each day
;
; Preconditions: None
;
; Postconditions: None
;
; Receives: 
;			[EBP+24] - author_name offset
;			[EBP+20] - program_name offset
;			[EBP+16] - description offset
;			[EBP+12] - daily_lows offset, refference - input/output
;			[EBP+8]	 - temp_array offset , reference - input
;
; Returns: None, alters command line
;
;------------------------------------------------------------------------------------------------------------
findDailyLows			PROC
	; Preserve registers
	PUSH	EBP
	MOV		EBP, ESP
	PUSH	ECX
	PUSH	EAX
	PUSH	EDX
	PUSH	ESI

	; Clear upper bits of EAX and setup references to both arrays
	XOR		EAX, EAX
	MOV		ESI, [EBP+8]								; ESI points to the temp_array
	MOV		EDX, [EBP+12]

	; Iterate through the temp_array for each day
	MOV		ECX, DAYS_MEASURED
_low_loop_for_day:
	; Start each day by grabbing the first temp of that day
	PUSH	ECX
	MOV		AL, BYTE PTR [ESI]
	MOV		ECX, TEMPS_PER_DAY

	;Iterate through each measurement for that day
_low_loop_per_day:
	; If the next value in the array is lower than whats in AL, move it on over
	CMP		AL, BYTE PTR [ESI]
	JB		_low_next_measure
	MOV		AL, BYTE PTR [ESI]

_low_next_measure:
	; Increment the index
	ADD		ESI, DATA_SIZE
	LOOP	_low_loop_per_day

	; Save the low value for that day and get the next spot for data in the low array
	MOV		[EDX], AL
	ADD		EDX, DATA_SIZE
	POP		ECX
	LOOP	_low_loop_for_day

	; Restore registers
	POP		ESI
	POP		EDX
	POP		EAX
	POP		ECX
	POP		EBP
	RET		8

findDailyLows			ENDP
;-------------------------------------------------------------------------------------------------------------
; Name: findDailyLowsHighs
; Description: finds the high temperatures for each day
;
; Preconditions: None
;
; Postconditions: None
;
; Receives: 
;			[EBP+24] - 
;			[EBP+20] - 
;			[EBP+16] - 
;			[EBP+12] - daily_lows offset, refference - input/output
;			[EBP+8]	 - temp_array offset , reference - input
;
; Returns: None, alters command line
;
;------------------------------------------------------------------------------------------------------------
findDailyHighs			PROC
	; Preserve registers
	PUSH	EBP
	MOV		EBP, ESP
	PUSH	ECX
	PUSH	EAX
	PUSH	EDX
	PUSH	ESI

	; Clear upperbits of EAX, grab references to both arrays
	XOR		EAX, EAX
	MOV		ESI, [EBP+8]								; ESI points to the temp_array
	MOV		EDX, [EBP+12]

	; Iterate through the temp_array for each day
	MOV		ECX, DAYS_MEASURED
_high_loop_for_day:
	; Save the first value for each day in AL
	PUSH	ECX
	MOV		AL, BYTE PTR [ESI]
	MOV		ECX, TEMPS_PER_DAY

	;Iterate through each measurement for that day
_high_loop_per_day:
	; If the next value in the array is larger than AL, replace AL
	CMP		AL, BYTE PTR [ESI]
	JA		_high_next_measure
	MOV		AL, BYTE PTR [ESI]

_high_next_measure:
	; Increment the pointer
	ADD		ESI, DATA_SIZE
	LOOP	_high_loop_per_day

	; Save the low value for that day and get the next spot for data in the low array
	MOV		[EDX], AL
	ADD		EDX, DATA_SIZE
	POP		ECX
	LOOP	_high_loop_for_day

	; Restore registers
	POP		ESI
	POP		EDX
	POP		EAX
	POP		ECX
	POP		EBP
	RET		8

findDailyHighs			ENDP
calcAverageLowHighTemps	PROC
calcAverageLowHighTemps	ENDP

;-------------------------------------------------------------------------------------------------------------
; Name: displayTempArray
;
; Description: Prints the program details and extracredit info
;
; Preconditions: None
;
; Postconditions: None
;
; Receives: 
;			[EBP+24] - rows to print  - value      input
;			[EBP+20] - columns to prt - value,     input  -
;			[EBP+16] - message offset - reference, input
;			[EBP+12] - Space_char	  -	reference, input
;			[EBP+8]	 - array to print - reference, input
;
; Returns: None, alters command line
;
;------------------------------------------------------------------------------------------------------------
displayTempArray		PROC
	; Preserve registers
	PUSH	EBP
	MOV		EBP, ESP
	PUSH	ECX
	PUSH	EAX
	PUSH	EDX
	PUSH	ESI

	; Print out the passed message
	MOV		EDX, [EBP+16]
	CALL	WriteString

_print_temp_array:
	; Setup the reference to the array
	MOV		ESI, [EBP+8]

	; Setup up outer loop, for each row
	MOV		ECX, [EBP+24]

_print_values_per_day:
	; Setup inner loop, for each column
	PUSH	ECX
	MOV		ECX, [EBP+20]

_print_single_reading:
	; Clear upper bits of EAX, and move the next value of the array into AL, and print it
	XOR		EAX, EAX
	MOV		AL, BYTE PTR [ESI]
	CALL	WriteDec

	; Print the passed delimiter
	MOV		EDX, [EBP+12]
	CALL	WriteString

	; Increment the pointer for the array
	ADD		ESI, DATA_SIZE
	LOOP	_print_single_reading
	
	CALL	CrLF
	POP		ECX
	LOOP	_print_values_per_day

	CALL	CrLF
	JMP		_return

_return:
	; Restore registers
	POP		ESI
	POP		EDX
	POP		EAX
	POP		ECX
	POP		EBP
	RET		20

displayTempArray		ENDP
END main
