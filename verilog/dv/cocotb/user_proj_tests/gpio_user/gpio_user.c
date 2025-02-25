#include <firmware_apis.h>
#include "user.h"
#include "EF_GPIO8.c"
#include "EF_GPIO8.h"


void main(){
    // Enable managment gpio as output to use as indicator for finishing configuration  
    ManagmentGpio_outputEnable();
    ManagmentGpio_write(0);
    enableHkSpi(0); // disable housekeeping spi
    User_enableIF(); // this necessary when reading or writing between wishbone and user project if interface isn't enabled no ack would be recieve and the command will be stuck
    // configure all gpios as  user out then chenge gpios from 32 to 37 before loading this configurations
    GPIOs_configureAll(GPIO_MODE_USER_STD_BIDIRECTIONAL);
    GPIOs_loadConfigs(); // load the configuration 
    ManagmentGpio_write(1); // configuration finished 

    // output
    EF_GPIO8_writeAllDirection(GPIO_USER,0xFF);

    EF_GPIO8_writeData(GPIO_USER,0X55);
    send_update();
    EF_GPIO8_writeData(GPIO_USER,0XAA);
    send_update();

    // input
    EF_GPIO8_writeAllDirection(GPIO_USER,0x00);
    // configure la [63:32] as output from cpu
    ManagmentGpio_write(1); 
    EF_GPIO8_waitInput(GPIO_USER, 0xAA);
    send_update();
    EF_GPIO8_waitInput(GPIO_USER, 0x55);
    send_update();
    EF_GPIO8_waitInput(GPIO_USER, 0xFF);
    send_update();
    EF_GPIO8_wait_InputPin(GPIO_USER, 2,0);
    send_update();
    EF_GPIO8_wait_InputPin(GPIO_USER, 3,0);
    send_update();


}

void send_update(){
    ManagmentGpio_write(1); 
    ManagmentGpio_write(0); 
}
