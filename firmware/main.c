#define F_CPU 1000000UL

#include <avr/io.h>
#include <util/delay.h>
#include <avr/sleep.h>
#include <avr/wdt.h>
#include <avr/interrupt.h>


void setup(void) {
  cli();
  
  // Disable Watchdog
  MCUSR &= ~(1<<WDRF);
  WDTCR |= (1<<WDCE) | (1<<WDE);
  WDTCR = 0;

  // Power Save Bits
  PRR = 0b00000000;

  
  sei();
}

int main(void) {

  while (1) { }

}
