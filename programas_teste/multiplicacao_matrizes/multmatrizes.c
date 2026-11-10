
/*defines da memoria armazenada por cada vetor, cada um  pode ter no maximo 16 elementos*/
#define M_matrizA 0
#define M_matrizB 16
#define M_matrizC 32
int main()
{
  int memo[64];
  int n = 3; /* utilizando matrizes 3x3 para teste*/

  for (int k = 0; k < n * n; k++)
  {
    memo[M_matrizA + k] = k + 1;
    memo[M_matrizB + k] = (k % n) + 1;
  }

  for (int i = 0; i < n; i++)
  {
    for (int j = 0; j < n; j++)
    {
      int mult = 0;
      for (int k = 0; k < n; k++)
      {
        int a = memo[M_matrizA + i * n + k];
        int b = memo[M_matrizB + k * n + j];
        mult += a * b;
      }
      
      memo[M_matrizC + i * n + j] = mult;
    }
  }

  return(0);
}