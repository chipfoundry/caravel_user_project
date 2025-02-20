#include <stress.h>
#include <stdio.h>
#include <math.h>
#include <stdbool.h>  // For using the bool type
#include <float.h>
#include <stdint.h>


#define N 3  // Define the size of the input signal

// Function to compute the DCT-II
void dct(float input[N], float output[N]) {
    int k, n;
    float alpha;
    
    for (k = 0; k < N; k++) {
        output[k] = 0.0;
        
        for (n = 0; n < N; n++) {
            output[k] += input[n] * cosf(M_PI / N * (n + 0.5) * k);
        }
        
        // Scaling factor for normalization
        alpha = (k == 0) ? sqrtf(1.0 / N) : sqrtf(2.0 / N);
        output[k] *= alpha;

    }
}

// Function to compute the Inverse DCT (IDCT)
void idct(float input[N], float output[N]) {
    int k, n;
    float alpha;
    
    for (n = 0; n < N; n++) {
        output[n] = 0.0;
        
        for (k = 0; k < N; k++) {
            alpha = (k == 0) ? sqrtf(1.0 / N) : sqrtf(2.0 / N);
            output[n] += alpha * input[k] * cosf(M_PI / N * (n + 0.5) * k);
        }
    }
}

// Function to check if the IDCT output matches the original input within a tolerance
bool check_reconstruction(float input[N], float output[N], float tolerance) {
    for (int i = 0; i < N; i++) {
        if (fabs(input[i] - output[i]) > tolerance) {
            return false;  // Failure if the difference exceeds tolerance
        }
    }
    return true;  // Success if all values are within tolerance
}

// Main function to test DCT and IDCT implementation
int main() {
    stress_test_start();
    // float input[N] = {255, 231, 189, 165, 122, 100, 85, 52};  // Example input signal
    float input[N] = {255, 231, 189};  // Example input signal
    float dct_output[N], idct_output[N];
    float tolerance = 1e-4;  // Define an acceptable error tolerance
    bool failure;

    // Perform the DCT
    dct(input, dct_output);

    // Perform the Inverse DCT
    idct(dct_output, idct_output);

    // Check if the IDCT output matches the original input
    failure = !check_reconstruction(input, idct_output, tolerance);

    // Check if reconstruction was successful
    if (failure) {
        return 1;  // Exit with failure code
    }
    stress_test_end();
    return 0;  // Exit with success code
}

to run this linker script needs to be changed to 

    // /* INCLUDE ../../generated/output_format.ld */

    // OUTPUT_FORMAT("elf32-littleriscv")

    // ENTRY(_start)

    // __DYNAMIC = 0;

    // /* INCLUDE ../../generated/regions.ld */

    // MEMORY {
    //     vexriscv_debug : ORIGIN = 0xf00f0000, LENGTH = 0x00000100
    //     dff : ORIGIN = 0x00000000, LENGTH = 0x00000400
    //     dff2_part1 : ORIGIN = 0x00000400, LENGTH = 0x00000100
    //     dff2_part2 : ORIGIN = 0x00000500, LENGTH = 0x00000100
    //     flash : ORIGIN = 0x10000000, LENGTH = 0x01000000
    //     mprj : ORIGIN = 0x30000000, LENGTH = 0x00100000
    //     hk : ORIGIN = 0x26000000, LENGTH = 0x00100000
    //     csr : ORIGIN = 0xf0000000, LENGTH = 0x00010000
    // }

    // SECTIONS
    // {
    //     .text : {
    //         _ftext = .;
    //         *(.vectors)
    //         *(.text*)
    //         *(.rodata*)
    //         *(.srodata.cst16) 
    //         *(.srodata.cst8) 
    //         *(.srodata.cst4) 
    //         *(.srodata.cst2) 
    //         *(.srodata .srodata.*) 
    //         . = ALIGN(8);
    //         _etext = .;
    //     } > flash


    //     .data : 
    //     {
    //         _fdata = .;
    //         *(.sdata .sdata.* .gnu.linkonce.s.*)
    //         *(.data*);
    //         _edata = .;
    //     PROVIDE( __global_pointer$ = . + 0x800 );
            
    //     } > dff,dff2_part1 AT > flash

    //     .bss (NOLOAD) :
    //     {
    //         _fbss = .;
    //         *(.bss*)
    //         *(COMMON)
    //         _ebss = .;
    //         _end = .;
    //     } > dff,dff2_part1
    // }

    // PROVIDE(_fstack = ORIGIN(dff2_part2) + LENGTH(dff2_part2));

    // PROVIDE(_fdata_rom = LOADADDR(.data));
    // PROVIDE(_edata_rom = LOADADDR(.data) + SIZEOF(.data));

// and stub function also



