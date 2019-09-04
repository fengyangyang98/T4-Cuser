#include<def.c>

void main(){
	inerrupt_init();
	
	while(connection_step != 3){
		send_data();
		con_init();
	}
	
	while(1){
		send_data();
		if( !buffer_485_pc_flag) get_nav();
		if(mem_writing == 1){
			iic_write_add(addr, info_data);
			mem_writing = 0;
		}
		if(mem_reading == 1){
			buffer_enqueue(iic_read_add(addr));
			mem_reading = 0;
		}
		if(vibrate_flag == 1)
			vibrate_get();
		if(buffer_485_pc_flag == 1){
			buffer_485_pc();
			buffer_485_pc_flag = 0;
		}
		if(buffer_485_stc_flag == 1){
			send_485_stc();
			buffer_485_stc_flag = 0;
		}
	}
	
}