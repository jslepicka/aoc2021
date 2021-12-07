includelib libcmt.lib

.data
szFilename db "7.txt", 0
szReadMode db "r", 0
szPart1 db "Part 1: %llu", 10, 0
szPart2 db "Part 2: %llu", 10, 0
positions dq 1024 dup (0)
dbl_pointfive real8 0.5

.data?
min_input dq ?
max_input dq ?
input_count dq ?

.code
extern printf:near
extern fopen:near
extern fclose:near
extern fgetc:near

main proc
	sub rsp, 38h
	
	call read_input
	
	mov rcx, 0 ;linear fuel consumption
	call calc_fuel
	mov rcx, offset szPart1
	mov rdx, rax
	call printf

	mov rcx, 1 ;quadratic fuel consumption
	call calc_fuel
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

	mov qword ptr min_input, -1
	mov qword ptr max_input, 0

	xor r14, r14
	mov r15, -1	;r15 contains current int
	;read data in
read_loop:
	mov rcx, filehandle
	call fgetc
	cmp eax, -1
	je end_input
	cmp rax, 10
	je end_input
	cmp rax, ','
	je end_input
	cmp r15, -1
	jne @F
	xor r15, r15
@@:
	imul r15, 10
	sub rax, 48
	add r15, rax
	jmp read_loop
end_input:
	;r15 contains number
	mov [positions + r14*8], r15
	inc r14

	cmp r15, [min_input]
	jae notmin
	mov min_input, r15
notmin:
	cmp r15, max_input
	jle notmax
	mov max_input, r15
notmax:
	cmp eax, -1
	je eof
	mov r15, -1
	jmp read_loop
eof:
	mov rcx, filehandle
	call fclose
	mov input_count, r14
	xor rax, rax
return:
	mov rsp, rbp
	pop rbp
	ret
read_input endp

calc_fuel proc
	min_cost equ [rbp - 8]
	model equ [rbp - 16]
	push rbp
	mov rbp, rsp
	sub rsp, 48h

	mov model, rcx
	mov qword ptr min_cost, -1

	mov rsi, min_input
posloop:
	xor r8, r8 ;cost
	xor rcx, rcx ;input_pos
inputloop:
	mov rax, [positions + rcx*8]
	sub rax, rsi
	;absolute value
	mov rbx, rax
	neg rax
	cmovl rax, rbx

	cmp qword ptr model, 1
	je quadratic
	add r8, rax
	jmp continue
quadratic:
	;convert rax to double in xmm0
	cvtsi2sd xmm0, rax
	;copy to xmm1
	movaps xmm1, xmm0
	;square xmm0
	mulsd xmm0, xmm0
	;multiply xmm0 and xmm1 by .5
	mulsd xmm0, dbl_pointfive
	mulsd xmm1, dbl_pointfive
	addsd xmm0, xmm1
	cvtsd2si rax, xmm0
	add r8, rax
continue:
	inc rcx
	cmp rcx, input_count
	jne inputloop

	cmp r8, min_cost
	ja notmin
	mov min_cost, r8
notmin:

	inc rsi
	cmp rsi, max_input
	jne posloop

	mov rax, min_cost
return:
	mov rsp, rbp
	pop rbp
	ret
calc_fuel endp

END