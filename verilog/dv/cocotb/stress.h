#ifndef STRESS_H
#define STRESS_H


#include <firmware_apis.h> // include required APIs


void stress_test_start(){
    ManagmentGpio_outputEnable();
    enableHkSpi(0);
    ManagmentGpio_write(1);
}

void stress_test_end(){
    ManagmentGpio_write(0);
}

#endif // STRESS_H