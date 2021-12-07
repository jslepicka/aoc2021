includelib libcmt.lib

.data
szFilename db "6.txt", 0
szReadMode db "r", 0
szPart1 db "Part 1: %llu", 10, 0
szPart2 db "Part 2: %llu", 10, 0
initial_state_counts dq 512 dup (0)

.code
extern printf:near
extern fopen:near
extern fclose:near
extern fgetc:near

main proc
	sub rsp, 38h
	
	call read_input
	
	mov rcx, 80
	call simulate
	mov rcx, offset szPart1
	mov rdx, rax
	call printf

	mov rcx, 256
	call simulate
	mov rcx, offset szPart2
	mov rdx, rax
	call printf

	add rsp, 38h
	mov rax, 0
	ret
main endp

read_input proc
	filehandle equ [rbp - 8]
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
	inc [initial_state_counts + rax*8]
	jmp read_loop
eof:
	mov rcx, filehandle
	call fclose

	mov rax, 0
return:
	mov rsp, rbp
	pop rbp
	ret
read_input endp

simulate proc
	state_counts equ [rbp - 128]
	push rbp
	mov rbp, rsp
	sub rsp, 0B8h

	mov r8, rcx

	;copy initial state to states
	xor rcx, rcx
copyloop:
	mov rax, qword ptr [initial_state_counts + rcx*8]
	mov qword ptr [state_counts + rcx*8], rax
	inc rcx
	cmp rcx, 9
	jne copyloop

	xor r9, r9
simloop:
	mov r9, state_counts

	xor rax, rax
	xor rcx, rcx
shiftloop:
	mov rax, qword ptr [state_counts + rcx*8 + 8]
	mov qword ptr [state_counts + rcx*8], rax
	inc rcx
	cmp rcx, 8
	jne shiftloop

	lea rcx, [state_counts + rcx*8]	;rcx pointing to state_counts[8]
	mov [rcx], r9
	sub rcx, 16                     ;rcx pointing to state_counts[6]
	add [rcx], r9

	dec r8
	jnz simloop

	xor rcx, rcx
	xor rax, rax
sumloop:
	add rax, qword ptr [state_counts + rcx*8]
	inc rcx
	cmp rcx, 9
	jne sumloop

return:
	mov rsp, rbp
	pop rbp
	ret
simulate endp

END