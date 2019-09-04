#ifndef __def_h_
#define __def_h_

#include<STC15F2K60S2.H>
#include<stdlib.h>
#include <intrins.h>  

/*****************************/
/*         data type         */
/*****************************/
#define uchar unsigned char
#define uint unsigned int
#define ulint unsigned long

/*****************************/
/*    constant defination    */
/*****************************/
#define KEY_MAX_NUM 	250
#define NAV_MAX_NUM 	150

#define CST_FOCS     	11059200L 
#define CST_BAUDL    	9600    

#define BUFFER_SIZE 	10

#define CST_ADC_POWER 0X80    
#define CST_ADC_FLAG 0X10     
#define CST_ADC_START 0X08 
#define CST_ADC_SPEED 0X60 
#define CST_ADC_CHS17 0X07 

#define S2RI  0x01              //S2CON.0
#define S2TI  0x02              //S2CON.1
#define S2RB8 0x04              //S2CON.2
#define S2TB8 0x08              //S2CON.3

/*****************************/
/*    global variable        */
/*****************************/

// vibrate
sbit vibrate = P2^4;	
bit vibrate_flag = 0;


// buffer
uchar buffer[BUFFER_SIZE];
uchar buffer_front_ptr = 0;
uchar buffer_rear_ptr = 0;
bit sending = 0;
char temp_data = 0;

uchar BufferData;

// 485
sbit rs485e  = P3^7 ;
uchar buffer_485[BUFFER_SIZE];
uchar buffer_485_ptr = 0;

bit buffer_485_busy = 1;
bit buffer_485_pc_flag = 0;
bit buffer_485_stc_flag = 0;
uchar buffer_485_data = 0;

// buzzer
sbit buzzer = P3 ^ 4;  
bit buzzer_on = 0;
uchar buzzer_high = 0xF7;
uchar buzzer_low = 0x5C;

// keys
sbit key1 = P3 ^ 2 ;          
sbit key2 = P3 ^ 3 ;        

uchar key1_count = 0;
uchar key2_count = 0;

bit key1_down = 0;
bit key2_down = 0;

// navi
char nav_high3 = 0;
bit nav_push = 0;

// led and nixie
uchar nixie_which = 0;
uchar nixie[9] = {0x39, 0x3f, 0x37, 0x37, 0x79, 0x39, 0x07, 0x00};

uchar nixie_setting_count = 0;
uchar led = 0x80;

// mem
uchar addr = 0;
uchar info_data = 0;
sbit SDA = P4 ^ 0;     
sbit SCL = P5 ^ 5;   

bit mem_writing = 0;
bit mem_reading = 0;


// connection steps
uchar connection_step = 1;
int con_count_delay = 0;
uchar con_count = 0;

// insturction 
uchar ins_state = 1;  /* 2: NixieSetting, 3: mem writing 6: LED setting,  */
											/* 7: mem reading, 9: buzzer music */

/*****************************/
/*      tool function        */
/****************************/

void delay_ms(uint n);		// delay for n ms
void delay_4us();					// delay for 4 ns

bit buffer_empty();
bit buffer_full();
void buffer_enqueue(uchar dat);
uchar buffer_dequeue();

//void get_adc();

void dig_select();

// mem
void iic_nit();
void iic_start();
void iic_stop();
void iic_respons();
void iic_writebyte( uchar date );
uchar iic_readbyte();

/*****************************/
/*        function           */
/*****************************/

void inerrupt_init();			// iniyialize the inerrupt

void send_data_buffer(uchar dat);
void send_data();

void get_key();

//void get_nav();

/*****************************/
/*    inerrupt function      */
/*****************************/





#endif