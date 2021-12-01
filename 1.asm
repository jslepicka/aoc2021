.386
.model flat, stdcall
.stack 4096
includelib libcmt.lib
includelib libvcruntime.lib
includelib libucrt.lib
includelib legacy_stdio_definitions.lib

.data
szFilename db "1.txt", 0
szReadMode db "r", 0
filehandle dd ?
strbuf db 16 dup (?)
szPart1 db "Part 1: %d", 10, 0
szPart2 db "Part 2: %d", 10, 0

measurements dd 2048 dup (?)
num_measurements dd 0

.code
extern printf:near
extern fopen:near
extern fclose:near
extern fgets:near
extern atoi:near

main PROC C
 call read_input

 cmp eax, 0
 je continue
 mov eax, -1
 ret
continue:

 call part1

 push eax
 push offset szPart1
 call printf
 add esp, 8

 call part2

 push eax
 push offset szPart2
 call printf
 add esp, 8
 
 mov eax, 0
 ret
main ENDP

read_input proc C
 push offset szReadMode
 push offset szFilename
 call fopen
 add esp, 8
 cmp eax, 0
 jne continue
 mov eax, -1
 ret
continue:
 mov [filehandle], eax

 mov ecx, 0 ;index into measurements
filereadloop:
 ;fgets(mystring, len, filehandle)
 push ecx
 push [filehandle]
 push 16
 push offset strbuf
 call fgets
 add esp, 12
 pop ecx
 cmp eax, 0
 je donereading

 ;int atoi(str)
 push ecx
 push offset strbuf
 call atoi
 add esp, 4
 pop ecx
 ;atoi return in eax

 mov [measurements + ecx*4], eax
 inc ecx
 inc num_measurements
 jmp filereadloop
donereading:

 ;close file
 push [filehandle]
 call fclose
 add esp, 4
 
 mov eax, 0
 ret
read_input ENDP

part1 proc
 depth equ [ebp - 4]
 last equ [ebp - 8]
 push ebp
 mov ebp, esp
 sub esp, 8
 mov dword ptr depth, 0
 mov dword ptr last, -1

 mov ebx, num_measurements
 mov ecx, 0
inputloop:
 cmp ecx, ebx
 je done
 mov eax, [measurements + ecx*4]
 cmp dword ptr last, -1
 je notgreater
 cmp eax, last
 jle notgreater
 inc dword ptr depth
notgreater:
 mov last, eax
 inc ecx
 jmp inputloop
done:
 mov eax, dword ptr depth
 mov esp, ebp
 pop ebp
 ret
part1 endp

part2 proc
 depth equ [ebp - 4]
 last equ [ebp - 8]
 push ebp
 mov ebp, esp
 sub esp, 8
 mov dword ptr depth, 0
 mov dword ptr last, -1

 mov ebx, num_measurements
 sub ebx, 2
 mov ecx, 0
inputloop:
 cmp ecx, ebx
 je done
 mov edx, ecx
 mov eax, [measurements + edx*4]
 add eax, [measurements + 4 + edx*4]
 add eax, [measurements + 8 + edx*4]
 cmp dword ptr last, -1
 je notgreater

 cmp eax, last
 jle notgreater
 inc dword ptr depth
notgreater:
 mov last, eax
 inc ecx
 jmp inputloop
done:
 mov eax, dword ptr depth
 mov esp, ebp
 pop ebp
 ret
part2 endp

END