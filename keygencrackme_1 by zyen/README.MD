### 题目
目标: keygencrackme
工具: Olly

### 基础分析
进行初步的分析后，发现:
1. Serial 只能输入数字，Nombre 则是能是任意数字或字母

### 过程
在 __vbaStrCmp 设置断点，输入Nombre 和 Serial 之后会断在我们刚设置的断点

```
00403A9D   . 66:8B76 34     MOV SI,WORD PTR DS:[ESI+34]
00403AA1   . 50             PUSH EAX
00403AA2   . FF15 8C104000  CALL DWORD PTR DS:[<&MSVBVM60.__vbaR8Str>;  MSVBVM60.__vbaR8Str
00403AA8   . 66:8BCE        MOV CX,SI
00403AAB   . 66:0FAFCE      IMUL CX,SI
00403AAF   . 0F80 5F010000  JO KgME.00403C14
00403AB5   . 66:6BC9 0A     IMUL CX,CX,0A
00403AB9   . 0F80 55010000  JO KgME.00403C14
00403ABF   . 0FBFD1         MOVSX EDX,CX
00403AC2   . 8995 4CFFFFFF  MOV DWORD PTR SS:[EBP-B4],EDX
00403AC8   . DB85 4CFFFFFF  FILD DWORD PTR SS:[EBP-B4]
00403ACE   . DD9D 44FFFFFF  FSTP QWORD PTR SS:[EBP-BC]
00403AD4   . DC9D 44FFFFFF  FCOMP QWORD PTR SS:[EBP-BC]
00403ADA   . DFE0           FSTSW AX
00403ADC   . F6C4 40        TEST AH,40
```
这时候EAX 等于 456, call __vbaR8Str 会返回双精度的浮点数放在 ST(0)
然后SI 刚好是 Nombre 的长度(L), 之后会有解释
总之， R = L^2 *10
ST(0) = R
ST(1) = Serial
这两个会做比较 

### 长度
至于SI 这个长度在哪里设置的
我们可以在 00403A9D Find references to -> address constant

00403EFB  |. 8B0E           MOV ECX,DWORD PTR DS:[ESI]
00403EFD  |. FF51 04        CALL DWORD PTR DS:[ECX+4]
00403F00  |. 66:8B56 34     MOV DX,WORD PTR DS:[ESI+34]
00403F04  |. 66:83C2 01     ADD DX,1
00403F08  |. 70 2A          JO SHORT KgME.00403F34
00403F0A  |. 66:8956 34     MOV WORD PTR DS:[ESI+34],DX

这是 vba 的 text change event, 每当输入一个字的时候 DX 就会+1

可以写出keygen 了
```python
def keygen(name: str) -> int:
    L = len(name)
    return L*L * 10

def main():
    name = input('Nombre: ')
    print(keygen(name))
if __name__ == '__main__':
    main()
```