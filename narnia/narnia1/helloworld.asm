section .data
msg db section .text

global _start ; Data segment
"Hello, world!", 0x0a ; The string and newline char
section .text; Text segment
; Default entry point for ELF linking
_start:
