includelib libcmt.lib

.data
szFilename db "6.txt", 0
szReadMode db "r", 0
szPart1 db "Part 1: %llu", 10, 0
szPart2 db "Part 2: %llu", 10, 0
initial_states db 512 dup (0)

.data?


.code
extern printf:near
extern fopen:near
extern fclose:near
extern fgetc:near

;x64 calling convention
;RCX, RDX, R8, R9 or fp XMM0, XMM1, XMM2, XMM3
;return result in RAX or XMM0

main proc
	sub rsp, 38h
	
	call read_input
	
	mov rcx, 80
	call sim_state
	mov rcx, offset szPart1
	mov rdx, rax
	call printf

	mov rcx, 256
	call sim_state
	mov rcx, offset szPart2
	mov rdx, rax
	call printf

	add rsp, 38h
	mov rax, 0
	ret
main endp

read_input proc
	filehandle equ [rbp - 8] ;64-bit var
	push rbp
	mov rbp, rsp
	sub rsp, 40h

	;open file
	mov rcx, offset szFilename
	mov rdx, offset szReadMode
	call fopen
	cmp rax, 0
	jne fopen_success
	mov rax, -1
	jmp return
fopen_success:
	mov filehandle, rax
	
	;read data in
read_loop:
	mov rcx, filehandle
	call fgetc
	cmp eax, -1
	je eof
	cmp rax, 10
	je eof
	cmp rax, ','
	je read_loop
	sub rax, 48
	inc [initial_states + rax]
	jmp read_loop
eof:
	mov rcx, filehandle
	call fclose

return:
	mov rsp, rbp
	pop rbp
	ret
read_input ENDP

sim_state proc
	states equ [rbp - 128]
	days equ [rbp - 136]
	push rbp
	mov rbp, rsp
	sub rsp, 0C0h

	mov days, rcx

	;copy initial state to states
	xor rcx, rcx
	xor rax, rax
copyloop:
	mov al, byte ptr [initial_states + rcx]
	mov qword ptr [states + rcx*8], rax
	inc rcx
	cmp rcx, 9
	jne copyloop

	mov r8, days
	xor r9, r9
simloop:
	mov r9, states

	xor rax, rax
	xor rcx, rcx
shiftloop:
	mov rax, qword ptr [states+rcx*8+8]
	mov qword ptr [states+rcx*8], rax
	inc rcx
	cmp rcx, 8
	jne shiftloop

	mov rcx, 8
	mov qword ptr [states+rcx*8], r9
	mov rcx, 6
	add qword ptr [states+rcx*8], r9

	dec r8
	jnz simloop

	xor rcx, rcx
	xor rax, rax
sumloop:
	add rax, qword ptr [states+rcx*8]
	inc rcx
	cmp rcx, 9
	jne sumloop

return:
	mov rsp, rbp
	pop rbp
	ret
sim_state endp

END