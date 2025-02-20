#include <stdint.h>
#include <stress.h>

static uint8_t aes_sbox[256];   /** AES S-box  */
static uint8_t aes_isbox[256];  /** AES iS-box */
void AES_generateSBox(void)
{
    uint32_t t[256], i;
    uint32_t x;
    for (i = 0, x = 1; i < 256; i ++)
    {
        t[i] = x;
        x ^= (x << 1) ^ ((x >> 7) * 0x11B);
    }

    aes_sbox[0] = 0x63;
    for (i = 0; i < 255; i ++)
    {
        x = t[255 - i];
        x |= x << 8;
        x ^= (x >> 4) ^ (x >> 5) ^ (x >> 6) ^ (x >> 7);
        aes_sbox[t[i]] = (x ^ 0x63) & 0xFF;
    }
    for (i = 0; i < 256;i++)
    {
         aes_isbox[aes_sbox[i]]=i;
    }
}


main(){
    stress_test_start();
	unsigned int sum = 0;
    AES_generateSBox();
    for(int i=0; i<256; i++)
      sum += (aes_sbox[i] + aes_isbox[i]);
    if(sum == 65280) 
        stress_test_end();
}
