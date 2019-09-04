#include <def.h>

/*****************************/
/*      tool function        */
/*****************************/

// delay for n ms
void delay_ms(uint n)
{
	while (n)
	{
		uchar i, j;
		i = 11;
		j = 190;
		do
		{
			while (--j)
				;
		} while (--i);
		n--;
	}
}

// delay for 4 ns
void delay_4us()
{
	;
	;
}

// buffer
bit buffer_empty()
{
	return buffer_rear_ptr == buffer_front_ptr;
}

bit buffer_full()
{
	return (buffer_rear_ptr + 1) % (BUFFER_SIZE) == buffer_front_ptr;
}

void buffer_enqueue(uchar dat)
{
	if (!buffer_full())
	{
		buffer[buffer_rear_ptr] = dat;
		buffer_rear_ptr = (buffer_rear_ptr + 1) % (BUFFER_SIZE);
	}
}

uchar buffer_dequeue()
{
	uchar temp;
	if (buffer_empty())
		return temp;

	temp = buffer[buffer_front_ptr];
	buffer_front_ptr = (buffer_front_ptr + 1) % (BUFFER_SIZE);
	return temp;
}


// nav
unsigned char get_adc()
{
	uchar result;
	ADC_CONTR = CST_ADC_POWER | CST_ADC_START | CST_ADC_SPEED | CST_ADC_CHS17;
	_nop_();
	_nop_();
	_nop_();
	_nop_();
	while (!(ADC_CONTR & CST_ADC_FLAG))
		;
	ADC_CONTR &= ~CST_ADC_FLAG;
	result = ADC_RES;
	return result;
}

//mem
void iic_start()
{
	SDA = 1;
	delay_4us();
	SCL = 1;
	delay_4us();
	SDA = 0;
	delay_4us();
}
void iic_stop()
{
	SDA = 0;
	delay_4us();
	SCL = 1;
	delay_4us();
	SDA = 1;
	delay_4us();
}
void iic_respons()
{
	uchar i = 0;
	SCL = 1;
	delay_4us();
	while (SDA == 1 && (i < 255))
		i++;
	SCL = 0;
	delay_4us();
}

void iic_writebyte(uchar date)
{
	uchar i, temp;
	temp = date;
	for (i = 0; i < 8; i++)
	{
		temp = temp << 1;
		SCL = 0;
		delay_4us();
		SDA = CY;
		delay_4us();
		SCL = 1;
		delay_4us();
	}
	SCL = 0;
	delay_4us();
	SDA = 1;
	delay_4us();
}

uchar iic_readbyte()
{
	uchar i, k;
	SCL = 0;
	delay_4us();
	SDA = 1;
	delay_4us();
	for (i = 0; i < 8; i++)
	{
		SCL = 1;
		delay_4us();
		k = (k << 1) | SDA;
		delay_4us();
		SCL = 0;
		delay_4us();
	}
	delay_4us();
	return k;
}

/*****************************/
/*        function         */
/*****************************/

// iniyialize the inerrupt
void inerrupt_init()
{
	// buzzer t0
	AUXR |= 0x80;
	TMOD &= 0xF0;
	TL0 = 0x5C;
	TH0 = 0xF7;
	TF0 = 0;
	TR0 = 1;

	ET0 = 1; // open ?
	buzzer = 0;


	AUXR |= 0x40;		
	TMOD &= 0x0F;	
	TL1 = 0xAE;	
	TH1 = 0xFB;	
	TF1 = 0;	
	TR1 = 1;
	ET1 = 1;
	
	
	S2CON = 0x50;  
	T2L = (65536 - (CST_FOCS / 4 / CST_BAUDL));
	T2H = (65536 - (CST_FOCS / 4 / CST_BAUDL)) >> 8;
	
	AUXR |= 0x01;
	SCON = 0x50;  
	RI = 0;
	TI = 0;
	ES = 1;
	PS = 1;
	
	rs485e = 0;
	P_SW2 |= 0x01 ;	
	IE2 = 0X01;
	
	AUXR |= 0x14;

	// the nav
	P1ASF = 0x80;
	ADC_RES = 0;
	ADC_CONTR = 0x8F;
	CLK_DIV = 0X00;
	IT1 = 0;
	
	EA = 1;

}

// send the data to the pc
void send_data_buffer(uchar dat)
{
	buffer_enqueue(dat);
}

void send_data()
{
	if (!buffer_empty() && sending == 0)
	{
		SBUF = buffer_dequeue();
		sending = 1;
	}
}

// key
void get_key()
{
	if (key1 == 0 && key1_down == 0)
		key1_count++;
	if (key2 == 0 && key2_down == 0)
		key2_count++;

	if (key1_count == KEY_MAX_NUM && key1_down == 0)
	{
		if (!buffer_full())
		{
			buffer[buffer_rear_ptr] = 0xb1;
			buffer_rear_ptr = (buffer_rear_ptr + 1) % (BUFFER_SIZE);
		}
		key1_down = 1;
	}
	else if (key2_count == KEY_MAX_NUM && key2_down == 0)
	{
		if (!buffer_full())
		{
			buffer[buffer_rear_ptr] = 0xb2;
			buffer_rear_ptr = (buffer_rear_ptr + 1) % (BUFFER_SIZE);
		}
		key2_down = 1;
	}
	
	if(key1_count >= KEY_MAX_NUM && key1 == 1){
		key1_count = 0;
		key2_count = 0;
		key1_down = 0;
		key2_down = 0;
	}
	else if(key2_count >= KEY_MAX_NUM && key2 == 1){
		key1_count = 0;
		key2_count = 0;
		key1_down = 0;
		key2_down = 0;
	}
}

// nav
void get_nav()
{
	uchar key;
	nav_high3 = 0x07;
	key = get_adc();
	if (key != 255)
	{
		delay_ms(5);
		key = get_adc();
		if (key != 255)
		{
			key = key & 0xE0;
			key = _cror_(key, 5);
			nav_high3 = key;
		}
	}

	if (nav_high3 == 0x07)
		nav_push = 0;

	if (nav_push == 0)
	{
		switch (nav_high3)
		{
		case 0x5: // up
			buffer_enqueue(0xa1);
			nav_push = 1;
			break;
		case 0x2: // down
			buffer_enqueue(0xa2);
			nav_push = 1;
			break;
		case 0x4: // left
			buffer_enqueue(0xa3);
			nav_push = 1;
			break;
		case 0x1: // right
			buffer_enqueue(0xa4);
			nav_push = 1;
			break;
		case 0x3:
			buffer_enqueue(0xa0);
			nav_push = 1;
			break;
		case 0x0:
			buffer_enqueue(0xb3); // key3
			nav_push = 1;
			break;
		default:
			break;
		}
	}
}

// mem

void iic_init()
{
	SCL = 1;
	delay_4us();
	SDA = 1;
	delay_4us();
}

void iic_write_add(uchar addr, uchar date)
{
	iic_start();
	iic_writebyte(0xa0);
	iic_respons();
	iic_writebyte(addr);
	iic_respons();
	iic_writebyte(date);
	iic_respons();
	iic_stop();
	
}

uchar iic_read_add(uchar addr)
{
	uchar date;
	iic_start();
	iic_writebyte(0xa0);
	iic_respons();
	iic_writebyte(addr);
	iic_respons();
	iic_start();
	iic_writebyte(0xa1);
	iic_respons();
	date = iic_readbyte();
	iic_stop();
	return date;
}

void con_init()
{
		switch(con_count_delay){
			case 1000000:
				led = _cror_(led, 1);
			  con_count_delay = 0;
				break;

			default:
				con_count_delay++;
				break;
		}

}

void vibrate_get(){
	vibrate = 1;
	if(vibrate == 0){
		if (!buffer_full())
		{
			buffer[buffer_rear_ptr] = 0xc8;
			buffer_rear_ptr = (buffer_rear_ptr + 1) % (BUFFER_SIZE);
		}
		delay_ms(40);
	}
}

void buffer_485_pc()
{
	while(buffer_485_ptr != 0){
		buffer_enqueue(buffer_485[buffer_485_ptr]);
		buffer_485_ptr--;
	}
}

void send_485_stc()
{
				rs485e = 1;
				S2BUF = buffer_485_data;
				while(buffer_485_busy);
				buffer_485_busy = 1;
				rs485e = 0;
}

/*****************************/
/*    inerrupt function      */
/*****************************/
void t0_interrupt() interrupt 1
{
	P3M1 = 0x00;
	P3M0 = 0x10;
	P0 = 0x00;
	
	if (buzzer_on)
	{
		buzzer = ~buzzer;
	}
	else
		buzzer = 0;
}

void t2_uart() interrupt 4 using 1
{
	if (RI)
	{
		RI = 0;
		temp_data = SBUF;

		if (connection_step == 3)
		{
			switch (ins_state)
			{
			case 1:
				switch (temp_data)
				{
					// LED start
					case 0x80:
						ins_state = 2;
						break;
					
					case 0x40:
						buzzer_on = 1;
						break;
					
					case 0x4f:
						buzzer_on = 0;
						break;
					
					case 0x20:
						ins_state = 3;
						break;
					
					case 0x60:
						ins_state = 7;
						break;
					
					case 0x70:
						ins_state = 6;
						break;
					
					case 0x50:
						ins_state = 9;
						break;

					case 0xc0:
						vibrate_flag = 1;
						break;

					case 0xcf:
						vibrate_flag = 0;
						break;

					case 0xe0:
						ins_state = 12;
						break;

					case 0xe8:
						buffer_485_pc_flag = 1;
						break;
					
					default:
						break;
				}
				break;
			
			case 2:
				switch(temp_data){
					case 0x8f:
						ins_state = 1;
						nixie_setting_count = 0;
						break;
					
					default:
						nixie[nixie_setting_count] = temp_data;
						nixie_setting_count++;
						if (nixie_setting_count == 8)
						{
							ins_state = 1;
							nixie_setting_count = 0;
						}
						break;
				}
				break;

			case 3:
				addr = temp_data;
				ins_state++;
				break;

			case 4:
				info_data = temp_data;
				ins_state++;
				break;

			case 5:
				if (temp_data == 0x2f)
				{
					mem_writing = 1;
				}
				ins_state = 1;
				break;
				
			case 6:
			led = temp_data;
				ins_state = 1;
				break;
			
			case 7:
				addr = temp_data;
				ins_state++;
				break;
			
			case 8:
				if (temp_data == 0x6f)
				{
					mem_reading = 1;
				}
				ins_state = 1;
				break;
				
			case 9:
				buzzer_high = temp_data;
				ins_state++;
				break;
			
			case 10:
				buzzer_low = temp_data;
				ins_state++;
				break;
			
			case 11:
				if (temp_data == 0x5f){
					TR0 = 0;
					TH0 = buzzer_high;
					TL0 = buzzer_low;
					TR0 = 1;
				}
				ins_state = 1;
				break;

			case 12:
				buffer_485_data = SBUF;
				buffer_485_stc_flag = 1;
				break;

			default:
				break;
				
			}
		}
		else{
			switch(temp_data){
				case 0xff:
					connection_step = 2;
					SBUF = 0xf0;
					break;
				case 0xf1:
					switch(connection_step){
						case 2:
							connection_step = 3;
							break;
						default:
							connection_step = 1;
							break;
					}
				default:
					break;
			}
		}
	}
	if (TI)
	{
		TI = 0;
		sending = 0;
	}
}


void t2_485() interrupt 8 using 1
{
	if(S2CON&S2RI)
	{	
		S2CON&=~S2RI;	
		buffer_485_ptr++;
		if(buffer_485_ptr < BUFFER_SIZE){
			buffer_485[buffer_485_ptr] = S2BUF;
		}
		else buffer_485_ptr = BUFFER_SIZE - 1;
			
		
	}

	if(S2CON&S2TI)
	{
		S2CON&=~S2TI;		
	 	buffer_485_busy  = 0 ;			
	}
}

void t1_interrupt() interrupt 3 using 1
{
	P2M0 = 0xff;
	P2M1 = 0x00;
	P0M0 = 0xff;
	P0M1 = 0x00;
	P0 = 0;
	P23 = ~P23;
	if (P23 == 0)
	{
		P2 = nixie_which;
		P0 = nixie[nixie_which];

		if (++nixie_which == 8)
			nixie_which = 0;
	}
	else
		P0 = led;
	
	if( !buffer_485_pc_flag) get_key();
}