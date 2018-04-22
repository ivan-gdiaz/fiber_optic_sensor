#include <msp430.h> 
#include <stdio.h>
#include <string.h>

void uart_c(char data);
void uart_s (char * data);
void hw_init (void);
unsigned int get_rnd (void);

char tx_buf[25];

volatile unsigned long i;
unsigned char send_cnt,button_prev, button_now,send_mode;
unsigned int var1,var2;
volatile unsigned char rcvd_ptr,rcvd_flag,rcvd_str[20];
unsigned char cmd_buf[20],cmd_valid;

volatile unsigned int adc_val1, adc_val2;
unsigned int get_adc (unsigned char chnl);
unsigned int get_adc_avg (unsigned char chnl, unsigned int reps);

#pragma vector=USCI_A1_VECTOR
__interrupt void USCI0RX_ISR(void)
{
    unsigned char temp;
   temp = UCA1RXBUF;
   if (temp<0x20)
          {
          if (rcvd_ptr>0)
              {
              rcvd_str[rcvd_ptr] = 0;
              rcvd_flag = 1;
              rcvd_ptr = 0;
              }
          }
      else
          {
          rcvd_str[rcvd_ptr++] = temp;
          }
      if (rcvd_ptr==sizeof(rcvd_str)) rcvd_ptr = 0;
}




void main(void)
{
    hw_init();
    send_mode = 1;
	while (1)
	{
	    var1 = get_adc_avg(0,777);
	    var2 = get_adc_avg(1,777);
	    if (rcvd_flag == 1)
	        {
	        rcvd_flag = 0;
	        cmd_valid = 1;
	        strcpy((char *)cmd_buf,(char *)rcvd_str);
	        }
	    if (cmd_valid == 1)
	        {
	        P4OUT ^= BIT7;
	        cmd_valid = 0;
	        if (strncmp((char *)cmd_buf,"gv",2)==0)
	            {
	            sprintf(tx_buf,"GV: %d,%d\n",var1, var2);
	            uart_s(tx_buf);
	            }
	        else if (strncmp((char *)cmd_buf,"gi",2)==0)
                {
                sprintf(tx_buf,"GI: sensor reader!\n");
                uart_s(tx_buf);
                }
	        else
                {
                sprintf(tx_buf,"wtf? gv,gi\n");
                uart_s(tx_buf);
                }
	        }
	}
}


unsigned int get_rnd (void)
{
static long rnd_var;
rnd_var = rnd_var * 1103515245;
rnd_var = rnd_var + 12345;
return ((rnd_var>>16) &0xFFFF);
}

void hw_init (void)
{
    WDTCTL = WDTPW | WDTHOLD;
    P4SEL |= BIT4+BIT5;
    UCA1CTL1 |= UCSWRST;
    UCA1CTL1 |= UCSSEL_2;
    UCA1BR0 = 27;
    UCA1BR1 = 0;
    UCA1MCTL = UCBRS_0 ;
    UCA1CTL1 &=~UCSWRST;
    UCA1IE |= UCRXIE;

    _BIS_SR(GIE);

    P1DIR = BIT0;
    P4DIR = BIT7;
    P1OUT = BIT1;   //pullup
    P1REN = BIT1;

    P6SEL |= 0x03;
    REFCTL0 &= ~REFMSTR;
    ADC12CTL0 = ADC12SHT0_9 | ADC12REFON | ADC12REF2_5V | ADC12ON;
    ADC12CTL1 = ADC12SHP;
    ADC12MCTL0 = ADC12SREF_1 + ADC12INCH_0;
    __delay_cycles(100);
    ADC12CTL0 |= ADC12ENC;


}

unsigned int get_adc_avg (unsigned char chnl, unsigned int reps)
{
unsigned int i;
unsigned long acc=0;
for (i=0;i<reps;i++)
{
    acc = acc + get_adc(chnl);
}
acc = acc / reps;
return acc;
}


unsigned int get_adc (unsigned char chnl)
{
    unsigned int retval;
    ADC12CTL0 &= ~ADC12ENC;
    ADC12MCTL0 = ADC12SREF_1 + chnl;
    ADC12CTL0 |= ADC12ENC;
    ADC12CTL0 &= ~ADC12SC;      // Clear the start bit (precautionary)
    ADC12CTL0 |= ADC12SC;       // Start the conversion
    // Poll busy bit waiting for conversion to complete
    while (ADC12CTL1 & ADC12BUSY);
    retval = ADC12MEM0 & 0x0FFF; // keep only low 12 bits
    return retval;
}


void uart_c(char data)
{
    UCA1TXBUF=data;
    while(UCA1STAT&UCBUSY);
}

void uart_s (char * data)
{
while (*data!=0)
    uart_c(*data++);
}
