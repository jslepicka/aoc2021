.386
.model flat, stdcall
.stack 4096
includelib libcmt.lib
includelib libvcruntime.lib
includelib libucrt.lib
includelib legacy_stdio_definitions.lib

.data
szFilename db "3.txt", 0
szReadMode db "r", 0
szPart1 db "Part 1: %d", 10, 0
szPart2 db "Part 2: %d", 10, 0

.data?
strbuf db 16 dup (?)
filehandle dd ?

input dd 1024 dup (?)
input_copy dd 1024 dup (?)
temp_input dd 1024 dup (?)
counts dd 12 dup (?)

.code
extern printf:near
extern fopen:near
extern fclose:near
extern fgets:near

main PROC C
	input_count equ [ebp-4]

	push ebp
	mov ebp, esp
	sub esp, 4

	call read_input
	cmp eax, -1
	je return

	mov input_count, eax
	push eax
	push offset input
	call part1
	add esp, 8

	push eax
	push offset szPart1
	call printf
	add esp, 8

	mov eax, input_count
	push eax
	push offset input
	call part2
	add esp, 8

	push eax
	push offset szPart2
	call printf
	add esp, 8

	mov eax, 0
return:
	mov esp, ebp
	pop ebp
	ret
main ENDP

; read file and store ints in [input]
; return the number of records read

read_input proc
	input_count equ [ebp - 4]

	push ebp
	mov ebp, esp
	sub esp, 4

	mov dword ptr input_count, 0

	push offset szReadMode
	push offset szFilename
	call fopen
	add esp, 8
	cmp eax, 0
	jne continue
	mov eax, -1
	jmp return
continue:
	mov [filehandle], eax

	lea esi, [input]
filereadloop:
	;fgets(mystring, len, filehandle)
	push [filehandle]
	push 16
	push offset strbuf
	call fgets
	add esp, 12
	cmp eax, 0
	je donereading

	xor eax, eax
	mov ecx, 0
	xor ebx, ebx
bitloop:
	shl ebx, 1
	mov al, byte ptr [strbuf + cx]
	sub al, 48
	or bl, al
	inc cx
	cmp cx, 12
	je bitdone
	jmp bitloop
bitdone:
	mov [esi], ebx
	add esi, 4
	inc dword ptr [input_count]
	jmp filereadloop

donereading:
	;close file
	push [filehandle]
	call fclose
	add esp, 4

	mov eax, [input_count]
return:
	mov esp, ebp
	pop ebp
	ret
read_input ENDP


get_counts proc
	input_ptr equ [ebp + 8]
	input_count equ [ebp + 12]

	push ebp
	mov ebp, esp
	sub esp, 8

	xor ecx, ecx

clearloop:
	mov [counts + ecx*4], 0
	inc ecx
	cmp ecx, 12
	jne clearloop

	mov eax, input_ptr
	xor esi, esi

scanloop:
	mov ecx, [eax+esi*4] ;ecx now has input
	mov edx, 0
bitloop:
	bt ecx, edx
	jnc notset
	inc dword ptr [counts+edx*4]
notset:
	inc edx
	cmp edx, 12
	jne bitloop
	inc esi
	cmp esi, input_count
	jne scanloop

	mov eax, dword ptr [counts]
return:
	mov esp, ebp
	pop ebp
	ret

get_counts endp

get_gamma proc
	input_ptr equ [ebp + 8]
	input_count equ [ebp + 12]

	push ebp
	mov ebp, esp

	push input_count
	push input_ptr
	call get_counts
	add esp, 8

	xor eax, eax ;gamma
	mov ebx, input_count

	mov esi, 0
countloop:
	mov edx, dword ptr [counts + esi*4]
	; need to compare count to input_count / 2, but need to take, e.g., 1.5 into account without floating point
	; so instead of diving input_count by 2, we'll just multiple count by 2 instead.
	shl edx, 1
	cmp edx, ebx
	jl continue
	mov ecx, esi
	mov edi, 1
	shl edi, cl
	or eax, edi
continue:  
	inc esi
	cmp esi, 12			;12 bits per input
	jne countloop

;return gamma in eax
return:
	mov esp, ebp
	pop ebp
	ret

get_gamma endp

part1 proc
	input_ptr equ [ebp + 8]
	input_count equ [ebp + 12]

	push ebp
	mov ebp, esp

	push input_count
	push input_ptr
	call get_gamma
	add esp, 8

	;eax has gamma
	mov ebx, eax
	xor ebx, 4095
	imul eax, ebx

return:
	mov esp, ebp
	pop ebp
	ret

part1 ENDP

get_rating proc
	gamma_xor equ [ebp - 4]
	result_count equ [ebp - 8]
	bitmask equ [ebp - 12]
	gamma equ [ebp - 16]
	check equ [ebp - 20]
	input_ptr equ [ebp + 8]
	input_count equ [ebp + 12]
	flip equ [ebp + 16]

	push ebp
	mov ebp, esp
	sub esp, 20

	;copy input to input_copy
	mov esi, input_ptr
	mov edi, offset input_copy
	mov ecx, 1024
	rep movsd

	mov ecx, 11 ;bit

	mov ebx, input_count
	mov dword ptr result_count, ebx

loop1:
	mov ebx, result_count
	cmp ebx, 1
	jle done
	push ecx
	push result_count
	push offset input_copy
	call get_gamma
	add esp, 8
	pop ecx
	cmp dword ptr [flip], 1
	jne noflip
	xor eax, 4095
noflip:
	mov gamma, eax

	mov edx, 1
	shl edx, cl
	mov bitmask, edx

	and eax, edx
	mov check, eax

	mov esi, 0
	mov edi, 0
resultloop:
	mov eax, [input_copy + esi*4]
	and eax, bitmask
	cmp eax, check
	jne continue

	mov eax, [input_copy + esi*4]
	mov [temp_input + edi*4], eax
	inc edi

continue:
	inc esi
	cmp esi, result_count
	je doneresultloop
	jmp resultloop

doneresultloop:
	mov result_count, edi
	mov esi, [temp_input]
	mov esi, 0


copyloop:
	mov eax, [temp_input + esi*4]
	mov [input_copy + esi*4], eax
	inc esi
	cmp esi, result_count
	jne copyloop

	dec ecx
	jmp loop1
done:
	mov eax, [temp_input]
return:
	mov esp, ebp
	pop ebp
	ret
get_rating endp

part2 proc
	input_ptr equ [ebp + 8]
	input_count equ [ebp + 12]
	
	push ebp
	mov ebp, esp
	sub esp, 8

	push 0
	push input_count
	push input_ptr
	call get_rating
	add esp, 12

	push eax

	push 1
	push input_count
	push input_ptr
	call get_rating
	add esp, 12

	pop ebx
	imul eax, ebx

return:
	mov esp, ebp
	pop ebp
	ret

part2 ENDP

END
