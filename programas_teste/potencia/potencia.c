/*IMPLEMENTACAO DE UM ALGORITMO RECURSIVO PARA CALCULAR A ELEVADO A B*/

int exprec(int a, int b)
{
  if (b == 1)
    return(a);
  else
    return(a * exprec(a, b - 1));
}

int main()
{
  int r = exprec(3,4);
}




