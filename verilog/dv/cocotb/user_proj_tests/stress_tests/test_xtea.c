#include <stdint.h>
#include <stress.h>


void xtea_encipher(unsigned int num_rounds, uint32_t v[2], uint32_t const key[4]) 
{
	unsigned int i;
	uint32_t v0 = v[0], v1 = v[1], sum = 0, delta = 0x9E3779B9;
	for (i = 0; i < num_rounds; i++) 
	{
		v0 += (((v1 << 4) ^ (v1 >> 5)) + v1) ^ (sum + key[sum & 3]);
		sum += delta;
		v1 += (((v0 << 4) ^ (v0 >> 5)) + v0) ^ (sum + key[(sum >> 11) & 3]);
	}
	v[0] = v0; v[1] = v1;
}

main(){
   	stress_test_start();
	volatile unsigned int r = 0;
	volatile unsigned int key[4] = { 0xFACE, 0xDEAD, 0xBABE, 0xD00D };
    volatile unsigned int v[4]={2345, 6671, 22223, 1992};    xtea_encipher(256, v, key);
    r = v[0] + v[1] + v[2] + v[3];
    if(r == 2610330147) 
		stress_test_end();
}