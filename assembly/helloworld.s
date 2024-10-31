section .text align=0

global _start

helloworld_string db 'Hello World', 0x0a

len equ $$ - helloworld_string  

_start
    mov eax, 4 
    mov ebx, 1
    mov ecx, helloworld_string
    mov edx, len
    int 0x80

    mov eax, 1
    int 0x8