.386
.model flat, stdcall
.stack 4096
includelib libcmt.lib
includelib libvcruntime.lib
includelib libucrt.lib
includelib legacy_stdio_definitions.lib

.data
szFilename db "2.txt", 0
szReadMode db "r", 0
szPart1 db "Part 1: %d", 10, 0
szPart2 db "Part 2: %d", 10, 0
szCharNum db "%c %i", 10, 0

.data?
strbuf db 16 dup (?)
filehandle dd ?
instruction_count dd ?
instructions db 1024 dup (?)
lengths db 1024 dup(?)


.code
extern printf:near
extern fopen:near
extern fclose:near
extern fgets:near

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

read_input proc
 instruction equ [ebp - 4]
 len equ [ebp - 8]
  
 push ebp
 mov ebp, esp
 sub esp, 8

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

filereadloop:
 ;fgets(mystring, len, filehandle)
 push [filehandle]
 push 16
 push offset strbuf
 call fgets
 add esp, 12
 cmp eax, 0
 je donereading

 mov bl, [strbuf]
 mov instruction, bl

 ;seek throuh strbuf until we get past space
 mov esi, offset strbuf
seekloop:
 cmp byte ptr [esi], 32
 je seekdone
 inc esi
 jmp seekloop
seekdone:
 ;past space, esi+1 points to len
 xor ebx, ebx
 mov bl, [esi+1]
 sub bl, 48 ;subtract 48 to convert ascii -> num
 mov len, ebx

  ;instruction and len contain, e.g., f 5

 ;push [len]
 ;push [instruction]
 ;push offset szCharNum
 ;call printf
 ;add esp, 12

 mov esi, [instruction_count]
 mov eax, instruction
 mov byte ptr [instructions + esi], al
 mov eax, len
 mov byte ptr [lengths + esi], al
 
 inc [instruction_count]

 jmp filereadloop
donereading:

 ;close file
 push [filehandle]
 call fclose
 add esp, 4
 
 mov eax, 0
return:
 mov esp, ebp
 pop ebp
 ret
read_input ENDP

part1 proc
 horiz equ [ebp - 4]
 depth equ [ebp - 8]
 push ebp
 mov ebp, esp
 sub esp, 8
 
 mov dword ptr horiz, 0
 mov dword ptr depth, 0

 mov esi, [instruction_count]
 mov ecx, 0
 xor eax, eax
 xor ebx, ebx
inputloop:
 mov al, [instructions + ecx]
 mov bl, [lengths + ecx]

 cmp al, 'f'
 je forward
 cmp al, 'd'
 je down
 cmp al, 'u'
 je up
 jmp done

forward:
 add horiz, ebx
 jmp continue
down:
 add depth, ebx
 jmp continue
up:
 sub depth, ebx
 jmp continue

continue:
 inc ecx
 cmp ecx, esi
 je done
 jmp inputloop
done:
 mov eax, horiz
 imul eax, depth
 mov esp, ebp
 pop ebp
 ret
part1 endp

part2 proc
 horiz equ [ebp - 4]
 depth equ [ebp - 8]
 aim equ [ebp - 12]
 push ebp
 mov ebp, esp
 sub esp, 12
 
 mov dword ptr horiz, 0
 mov dword ptr depth, 0
 mov dword ptr aim, 0

 mov esi, [instruction_count]
 mov ecx, 0
 xor eax, eax
 xor ebx, ebx
inputloop:
 mov al, [instructions + ecx]
 mov bl, [lengths + ecx]

 cmp al, 'f'
 je forward
 cmp al, 'd'
 je down
 cmp al, 'u'
 je up
 jmp done

forward:
 add horiz, ebx
 mov eax, aim
 imul eax, ebx
 add depth, eax
 jmp continue
down:
 add aim, ebx
 jmp continue
up:
 sub aim, ebx
 jmp continue

continue:
 inc ecx
 cmp ecx, esi
 je done
 jmp inputloop
done:
 mov eax, horiz
 imul eax, depth
 mov esp, ebp
 pop ebp
 ret
part2 endp

END