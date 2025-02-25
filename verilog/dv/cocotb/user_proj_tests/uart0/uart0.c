// SPDX-FileCopyrightText: 2023 Efabless Corporation

// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at

//      http://www.apache.org/licenses/LICENSE-2.0

// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.


#include <firmware_apis.h>
#include "user.h"
#include "EF_UART.c"
#include "EF_UART.h"


void main(){
    // Enable managment gpio as output to use as indicator for finishing configuration  
    ManagmentGpio_outputEnable();
    ManagmentGpio_write(0);
    enableHkSpi(0); // disable housekeeping spi
    // configure all gpios as  user out then chenge gpios from 32 to 37 before loading this configurations
    User_enableIF(); // this necessary when reading or writing between wishbone and user project if interface isn't enabled no ack would be recieve and the command will be stuck
    GPIOs_configureAll(GPIO_MODE_USER_STD_BIDIRECTIONAL);
    GPIOs_loadConfigs(); // load the configuration 
    // configure la [63:32] as output from cpu
    EF_DRIVER_STATUS status;
    status = UART_Init(UART0_USER, 2083333, 50000000, 8, true, ODD, 0x3F, 0, 10);
    ManagmentGpio_write(1); // configuration finished 

    if (status != EF_DRIVER_OK) {
        ManagmentGpio_write(0);
        return -1;
    }
    // Receive a message
    char buffer[100];
    status = EF_UART_readCharArr(UART0_USER, buffer, sizeof(buffer));
    if (status == EF_DRIVER_OK) {
        // Print received message
        // Transmit a message received
        status = EF_UART_writeCharArr(UART0_USER, buffer);
        if (status != EF_DRIVER_OK) {
            // Handle transmission error
            ManagmentGpio_write(0);
            return -1;
        }
    } else {
        // Handle reception error
        ManagmentGpio_write(0);
        return -1;
    }
    ManagmentGpio_write(0);
    return 0;

}